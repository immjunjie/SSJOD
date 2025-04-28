from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from flask_socketio import SocketIO, emit
import threading
import logger
from filter_endpoints import filterMask
import requests
import os

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
app.secret_key = 'dojossjos'
socketio = SocketIO(app)

log_thread = None
is_logging = False
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def start_logging(sequence, uploaded_paths, printer_ip):
    gcode_path = next((p for n, p in uploaded_paths.items() if n.endswith('.gcode')), None)
    stl_path = next((p for n, p in uploaded_paths.items() if n.endswith('.stl')), None)

    if not (gcode_path and stl_path and printer_ip):
        print("Missing G-code, STL file, or printer IP.")
        return


    #test_url = f"http://{printer_ip}/docs/printer" <----- for simulator only
    test_url = f"http://{printer_ip}/api/v1/printer"# <--- for actual printer
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
        hdf5_filename='print_details.hdf5',
        #base_url = f"http://{printer_ip}/docs/printer" <----- for simulator only
        base_url=f'http://{printer_ip}/api/v1/printer', # <--- for actual printer
        interval_time=0.0001,
        endpoints=filterMask(sequence),
        sequence=sequence,
        stl_path=stl_path,
        gcode_path=gcode_path)

@app.route("/")
def index():
    filenames = list(session.get('uploaded_paths', {}).keys())
    printer_ip = session.get('printer_ip')
    printer_error = session.pop('printer_error', '')
    return render_template("index.html", logging=is_logging, filenames=filenames, printer_ip=printer_ip, printer_error=printer_error, listOfEndpoints=listOfEndpoints, sequence=current_sequence)

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

    sequence = ""
    for i in range(len(listOfEndpoints)):
        checkbox_name = f"ep{i}"
        sequence += '1' if checkbox_name in request.form else '0'

    current_sequence = sequence

    uploaded_paths = session.get('uploaded_paths', {})

    gcode_exists = any(n.endswith('.gcode') for n in uploaded_paths)
    stl_exists = any(n.endswith('.stl') for n in uploaded_paths)
    print(gcode_exists)
    print(stl_exists)

    if not is_logging and gcode_exists and stl_exists:
        printer_ip = session.get('printer_ip')
        log_thread = threading.Thread(target=start_logging, args=(sequence, uploaded_paths, printer_ip))
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

if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)