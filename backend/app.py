import os
import threading
import requests
from dotenv import load_dotenv
load_dotenv() 
from flask import (
    Flask, render_template, redirect,
    url_for, request, jsonify, session, send_file, flash
)
from flask_socketio import SocketIO

from backend.extractor import run_extraction  # <-- your standalone extractor CLI logic
from backend.upload_to_invenio import create_record, upload_file

# —————————————————————————————————————————————————————————————
# Configuration & Flask app init
# —————————————————————————————————————————————————————————————

BASE_DIR     = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'frontend', 'templates')
STATIC_DIR   = os.path.join(BASE_DIR, 'frontend', 'static')

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
    static_url_path='/static'
)
app.secret_key = os.getenv("SECRET_KEY")
socketio = SocketIO(app, cors_allowed_origins="*")

# Ensure these folders exist
UPLOAD_FOLDER  = os.path.abspath(os.getenv("UPLOAD_FOLDER"))
DETAILS_FOLDER = os.path.abspath(os.getenv("DETAILS_FOLDER"))
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
            resp = requests.get(f"http://{ip}/docs/printer", timeout=float(os.getenv("PRINTER_API_TIMEOUT")))
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
        existing = [
            f for f in os.listdir(DETAILS_FOLDER)
            if f.startswith("print_details_") and f.endswith(".hdf5")
        ]
        idxs = [int(f.split("_")[-1].split(".")[0]) for f in existing]
        nxt = max(idxs)+1 if idxs else 0
        hdf5_fn = os.path.join(DETAILS_FOLDER, f"print_details_{nxt}.hdf5")

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
    # signal cancellation
    from backend.extractor import stop_extraction
    stop_extraction()
    # give the background job a moment to exit cleanly
    if log_thread:
        log_thread.join(timeout=2)
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


@app.route('/download', methods=['POST'])
def download():
    sel = request.form.get("selected_file","")
    custom = request.form.get("custom_name","")
    if not sel or not custom:
        return render_template("index.html", downloadBoxError="Select file + name")
    # sanitize …
    src = os.path.join(DETAILS_FOLDER, sel)
    return send_file(src, as_attachment=True, download_name=custom, mimetype='application/octet-stream')




# —————————————————————————————————————————————————————————————
# VVV TO BE CONTINUED... (NEEDS TESTING AND FURTHER DEVELOPMENT) VVV
# —————————————————————————————————————————————————————————————
@app.route('/upload-to-invenio', methods=['POST'])
def upload_to_invenio():

    selected_file = request.form.get('invenio_selected_file')
    meta_title = request.form.get('meta_title')
    meta_creators = request.form.get('meta_creators')
    meta_description = request.form.get('meta_description')
    meta_pub_date = request.form.get('meta_pub_date')
 
    metadata = {
        'title': meta_title,
        'creators': [ {'name': name.strip()} for name in meta_creators.split(',') ],
        'description': meta_description,
        'publication_date': meta_pub_date
    }

    file_path = os.path.join(os.getcwd(), 'Print_details_folder', selected_file)

    try:  
        record_id = create_record(metadata)
        upload_resp = upload_file(record_id, file_path)
        flash(f'Invenio upload successful: record {record_id}', 'success')
    except Exception as e:
        flash(f'Upload to Invenio failed: {e}', 'error')

    return redirect(url_for('index'))



