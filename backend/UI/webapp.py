from flask import Flask, render_template, redirect, url_for, request, jsonify, session, send_file
from flask_socketio import SocketIO
import threading
import logger
from filter_endpoints import filterMask
import requests
import os
import re

listOfEndpoints = [
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
    "Max Speed"
]

current_sequence = "1" * len(listOfEndpoints)

app = Flask(__name__)
app.secret_key = 'dojossjod'
socketio = SocketIO(app)

log_thread = None
is_logging = False
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DETAILS_FOLDER = 'Print_details_folder'
os.makedirs(DETAILS_FOLDER, exist_ok=True)


def start_logging(sequence, uploaded_paths, printer_ip, use_same_file, selected_filename):
    gcode_path = next((p for n, p in uploaded_paths.items() if n.endswith('.gcode')), None)
    stl_path = next((p for n, p in uploaded_paths.items() if n.endswith('.stl')), None)

    if not (gcode_path and stl_path and printer_ip):
        print("Missing G-code, STL file, or printer IP.")
        return

    if selected_filename and selected_filename != "New":
        hdf5_filename = os.path.join(DETAILS_FOLDER, selected_filename)
    else:
        # Auto-increment file name
        existing_files = [f for f in os.listdir(DETAILS_FOLDER) if f.startswith("print_details_") and f.endswith(".hdf5")]
        indices = [int(f.split("_")[-1].split(".")[0]) for f in existing_files if f.split("_")[-1].split(".")[0].isdigit()]
        next_index = max(indices) + 1 if indices else 0
        hdf5_filename = os.path.join(DETAILS_FOLDER, f"print_details_{next_index}.hdf5")

    test_url = f"http://{printer_ip}/api/v1/printer"
    try:
        response = requests.get(test_url, timeout=2)
        if response.status_code != 200:
            print(f"Printer at {printer_ip} responded with status {response.status_code}. Aborting logger.")
            return
    except requests.RequestException as e:
        print(f"Could not reach printer at {printer_ip}: {e}")
        return

    global is_logging
    is_logging = True
    logger.run_logger_with_socket(
        socketio=socketio,
        hdf5_filename=hdf5_filename,
        base_url=test_url,
        interval_time=0.0001,
        endpoints=filterMask(sequence),
        sequence=sequence,
        stl_path=stl_path,
        gcode_path=gcode_path
    )

@app.route("/")
def index():
    filenames = list(session.get('uploaded_paths', {}).keys())
    use_same_file = session.get('use_same_file', False)
    printer_ip = session.get('printer_ip')
    printer_error = session.pop('printer_error', '')
    
    existing_files = ["New"] + sorted(f for f in os.listdir(DETAILS_FOLDER) if f.endswith('.hdf5'))
    selected_file = session.get('selected_hdf5_file', 'New')

    return render_template("index.html", 
                        logging=is_logging, 
                        filenames=filenames, 
                        printer_ip=printer_ip,
                        printer_error=printer_error, 
                        listOfEndpoints=listOfEndpoints, 
                        sequence=current_sequence, 
                        use_same_file=use_same_file,
                        existing_files=existing_files,
                        selected_file=selected_file)

@app.route("/set-printer", methods=["POST"])
def set_printer():
    ip = request.form.get('printer_ip')
    if ip:
        try:
            resp = requests.get(f"http://{ip}/docs/printer", timeout=2)
            if resp.status_code == 200:
                session['printer_ip'] = ip
                session['printer_error'] = ''
            else:
                session['printer_error'] = "Printer did not respond correctly."
        except requests.RequestException:
            session['printer_error'] = "Failed to connect to printer."
    return redirect(url_for('index'))

@app.route("/start", methods=['GET', 'POST'])
def start():
    global log_thread, is_logging, current_sequence
    uploaded_paths = session.get('uploaded_paths', {})

    use_same_file = 'same_file' in request.form  # still preserved if needed
    session['use_same_file'] = use_same_file
    selected_filename = request.form.get('existing_file', 'New')
    session['selected_hdf5_file'] = selected_filename

    sequence = "".join(
        '1' if f"ep{i}" in request.form else '0'
        for i in range(len(listOfEndpoints))
    )
    current_sequence = sequence

    gcode_exists = any(n.endswith('.gcode') for n in uploaded_paths)
    stl_exists = any(n.endswith('.stl') for n in uploaded_paths)

    if not is_logging and gcode_exists and stl_exists:
        printer_ip = session.get('printer_ip')
        log_thread = threading.Thread(
            target=start_logging,
            args=(sequence, uploaded_paths, printer_ip, use_same_file, selected_filename)
        )
        log_thread.start()
        is_logging = True

    return redirect(url_for("index"))

@app.route("/stop")
def stop():
    global is_logging, log_thread
    is_logging = False
    logger.stop_logger()
    if log_thread:
        log_thread.join()
    return redirect(url_for("index"))

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_paths = session.get('uploaded_paths', {})
    responses = {}

    for filename in request.files:
        file = request.files[filename]
        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            uploaded_paths[filename] = file_path
            responses[filename] = "uploaded"

    session['uploaded_paths'] = uploaded_paths
    return jsonify(status="success", files=responses)

@app.route("/uploaded-files")
def get_uploaded_files():
    uploaded_paths = session.get('uploaded_paths', {})
    return jsonify(files=list(uploaded_paths.keys()))

@app.route('/delete-file/<filename>', methods=['POST'])
def delete_file(filename):
    uploaded_paths = session.get('uploaded_paths', {})
    if filename in uploaded_paths:
        file_path = uploaded_paths.pop(filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    session['uploaded_paths'] = uploaded_paths
    return jsonify(success=True)

@app.route('/download', methods=['POST'])
def download_hdf5():
    selected_file = request.form.get("selected_file", "").strip()
    custom_name = request.form.get("custom_name", "").strip()

    if not selected_file or not custom_name:
        return render_template("index.html", downloadBoxError="Please select a file and enter a name.")

    selected_file = re.sub(r'[^\w\-_.]', '_', selected_file)
    custom_name = re.sub(r'[^\w\-_.]', '_', custom_name)

    if not custom_name.endswith(".hdf5"):
        custom_name += ".hdf5"

    hdf5_path = os.path.abspath(os.path.join(DETAILS_FOLDER, selected_file))

    if not os.path.exists(hdf5_path):
        return render_template("index.html", downloadBoxError="Selected HDF5 file does not exist.")

    return send_file(
        hdf5_path,
        as_attachment=True,
        download_name=custom_name,
        mimetype='application/octet-stream',
        max_age=0
    )

if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)