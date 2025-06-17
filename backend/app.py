import sys
import os
import threading
import requests
from flask import (
    Flask, render_template, redirect,
    url_for, request, jsonify, session, send_file, flash
)
from flask_socketio import SocketIO

from backend.extractor import run_extraction  # <-- your standalone extractor CLI logic
import logging
# —————————————————————————————————————————————————————————————
# Configuration & Flask app init
# —————————————————————————————————————————————————————————————
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to the frontend folders (one level up, into frontend/)
STATIC_FOLDER = os.path.join(BASE_DIR, '..', 'frontend', 'static')
TEMPLATE_FOLDER = os.path.join(BASE_DIR, '..', 'frontend', 'templates')

app = Flask(__name__, static_folder=STATIC_FOLDER, template_folder=TEMPLATE_FOLDER)

print("Static folder:", STATIC_FOLDER)
print("Template folder:", TEMPLATE_FOLDER)

app = Flask(
    __name__,
    template_folder=TEMPLATE_FOLDER,
    static_folder=STATIC_FOLDER,
    static_url_path='/static'
)
app.secret_key = 'dojossjod'
socketio = SocketIO(app, cors_allowed_origins="*")

# Ensure these folders exist
UPLOAD_FOLDER  = os.path.join(BASE_DIR, 'uploads')
DETAILS_FOLDER = os.path.join(BASE_DIR, 'Print_details_folder')
os.makedirs(UPLOAD_FOLDER,  exist_ok=True)
os.makedirs(DETAILS_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Telemetry labels and default bit-mask
listOfEndpoints  = [
    "Head Position", 
    "Bed Temperature", 
    "Nozzle_temp_current", 
    "Nozzle_temp_target",
    "Time_spent_hot", 
    "Status", 
    "Material Extruded", 
    "Led",
    "Jerk", 
    "Active Material", 
    "Remaining Length", 
    "Max Speed", 
    "Screenshots"
]
current_sequence = "1" * len(listOfEndpoints)

log_thread  = None
is_logging  = False

# —————————————————————————————————————————————————————————————
# Helper to launch the extractor in a background thread
# —————————————————————————————————————————————————————————————

def _bridge_extraction(
    printer_ip: str,
    gcode_path: str,
    stl_path: str,
    hdf5_filename: str,
    sequence_bits: str,
    duration: float,
    delay: float
):
    """
    Calls your extractor.run_extraction and, as each scan is done,
    the extractor should emit `new_log` events itself (it can be passed
    the socketio object if needed).  When finished, emit `logging_stopped`.
    """
    try:
        run_extraction(
            printer_ip=printer_ip,
            stl_path=stl_path,
            gcode_path=gcode_path,
            output_hdf5=hdf5_filename,
            sequence_bits=sequence_bits,
            max_duration=duration,
            delay_sec=delay,
            socketio=socketio
        )
    finally:
        socketio.emit('logging_stopped')


# —————————————————————————————————————————————————————————————
# Flask routes
# —————————————————————————————————————————————————————————————

@app.route("/")
def index():
    filenames     = list(session.get('uploaded_paths', {}).keys())
    printer_ip    = session.get('printer_ip')
    printer_error = session.pop('printer_error', '')
    remaining     = session.get('remaining_time')

    existing = ["New"] + sorted(
        fname for fname in os.listdir(DETAILS_FOLDER) if fname.endswith(".hdf5")
    )
    selected = session.get('selected_hdf5_file', 'New')

    return render_template(
        "index.html",
        logging=is_logging,
        filenames=filenames,
        printer_ip=printer_ip,
        printer_error=printer_error,
        listOfEndpoints=listOfEndpoints,
        sequence=current_sequence,
        existing_files=existing,
        remaining_time=remaining,
        selected_file=selected,
        # persist UI fields
        hours=session.get('hours', ''),
        minutes=session.get('minutes', ''),
        seconds=session.get('seconds', ''),
        unlimited_duration=session.get('unlimited_duration', False),
        delay_seconds=session.get('delay_seconds', '')
    )


@app.route("/set-printer", methods=["POST"])
def set_printer():
    ip  = request.form.get('printer_ip')
    cam = request.form.get('camera_url')
    if ip:
        try:
            resp = requests.get(f"http://{ip}/docs/printer", timeout=2)
            if resp.status_code == 200:
                session['printer_ip']    = ip
                session['camera_url']    = cam or None
                session['printer_error'] = ''
            else:
                session['printer_error'] = "Printer did not respond correctly."
        except requests.RequestException:
            session['printer_error'] = "Failed to connect to printer."
    return redirect(url_for('index'))


@app.route("/start", methods=["POST"])
def start():
    global log_thread, is_logging, current_sequence

    # persist form fields
    session['hours']              = request.form.get('hours', '')
    session['minutes']            = request.form.get('minutes', '')
    session['seconds']            = request.form.get('seconds', '')
    session['unlimited_duration'] = bool(request.form.get('unlimited_duration'))
    session['delay_seconds']      = request.form.get('delay_seconds', '')
    session['selected_hdf5_file'] = request.form.get('existing_file', 'New')

    # assemble parameters
    uploaded = session.get('uploaded_paths', {})
    sequence_bits = "".join(
        '1' if f"ep{i}" in request.form else '0'
        for i in range(len(listOfEndpoints))
    )
    current_sequence = sequence_bits

    # ensure we have both G-code and STL
    has_g = any(name.endswith('.gcode') for name in uploaded)
    has_s = any(name.endswith('.stl')   for name in uploaded)
    if is_logging or not (has_g and has_s):
        return redirect(url_for('index'))

    ip = session.get('printer_ip')
    if not ip:
        session['printer_error'] = "Set printer IP first."
        return redirect(url_for('index'))

    # compute durations
    if request.form.get("unlimited_duration"):
        duration = None
    else:
        try:
            h = int(request.form.get("hours") or 0)
            m = int(request.form.get("minutes") or 0)
            s = int(request.form.get("seconds") or 0)
        except ValueError:
            session['printer_error'] = "Invalid time format."
            return redirect(url_for('index'))
        duration = h*3600 + m*60 + s
        if duration <= 0:
            session['printer_error'] = "Duration must be > 0."
            return redirect(url_for('index'))

    # parse delay
    try:
        delay = float(request.form.get('delay_seconds') or 0.0)
    except ValueError:
        delay = 0.0

    # choose HDF5 filename
    sel = session['selected_hdf5_file']
    if sel != "New":
        hdf5_fn = os.path.join(DETAILS_FOLDER, sel)
    else:
        from datetime import datetime
    
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        hdf5_fn = os.path.join(DETAILS_FOLDER, f"print_details_{timestamp}.hdf5")

    # pick paths
    gcode_path = next(p for n,p in uploaded.items() if n.endswith('.gcode'))
    stl_path   = next(p for n,p in uploaded.items() if n.endswith('.stl'))

    # spawn the bridge
    def runner():
        global is_logging
        try:
            _bridge_extraction(
                ip, gcode_path, stl_path, hdf5_fn,
                sequence_bits, duration, delay
            )
        finally:
            is_logging = False

    log_thread = threading.Thread(target=runner, daemon=True)
    log_thread.start()
    is_logging = True
    session['remaining_time'] = duration

    return redirect(url_for('index'))


@app.route("/stop")
def stop():
    global is_logging, log_thread
    is_logging = False
    # tell extractor to die
    from backend.extractor import stop_extraction
    stop_extraction()
    if log_thread:
        log_thread.join(timeout=1)
    return redirect(url_for('index'))


@app.route('/upload', methods=['POST'])
def upload():
    uploaded = session.get('uploaded_paths', {})
    resp = {}
    for fn, file in request.files.items():
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        uploaded[fn] = path
        resp[fn] = "uploaded"
    session['uploaded_paths'] = uploaded
    return jsonify(status="success", files=resp)


@app.route("/uploaded-files")
def uploaded_files():
    return jsonify(files=list(session.get('uploaded_paths', {}).keys()))


@app.route('/delete-file/<filename>', methods=['POST'])
def delete_file(filename):
    uploaded = session.get('uploaded_paths', {})
    if filename in uploaded:
        try:
            os.remove(uploaded.pop(filename))
        except OSError:
            pass
    session['uploaded_paths'] = uploaded
    return jsonify(success=True)

@app.route('/download', methods=['GET'])
def download():
    logging.debug("/download did run")

    sel = request.args.get("selected_file", "")
    custom = request.args.get("custom_name", "")
    logging.debug(f"Form values - selected_file: {sel}, custom_name: {custom}")

    if not sel or not custom:
        logging.debug("Missing form fields")
        flash("Please select a file and enter a download name", "error")
        return redirect(url_for('index'))

    src = os.path.join(DETAILS_FOLDER, sel)
    logging.debug(f"Resolved source file path: {src}")

    if not os.path.exists(src):
        logging.debug(f"Source file does not exist: {src}")
        flash(f"File not found: {sel}", "error")
        return redirect(url_for('index'))

    if not custom.endswith('.hdf5'):
        custom += '.hdf5'
        logging.debug(f"Appended .hdf5 to custom filename: {custom}")

    try:
        import shutil
        import platform
        
        # Get the user's Downloads folder
        if platform.system() == "Windows":
            downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        elif platform.system() == "Darwin":  # macOS
            downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        else:  # Linux
            downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        
        dest_path = os.path.join(downloads_folder, custom)
        
        # Handle duplicate filenames
        counter = 1
        original_dest = dest_path
        while os.path.exists(dest_path):
            name, ext = os.path.splitext(original_dest)
            dest_path = f"{name}_{counter}{ext}"
            counter += 1
        
        shutil.copy2(src, dest_path)
        logging.debug(f"File copied to: {dest_path}")
        flash(f"File downloaded to: {dest_path}", "success")
        
    except Exception as e:
        logging.exception("Download error occurred")
        flash(f"Download error: {str(e)}", "error")
    
    return redirect(url_for('index'))