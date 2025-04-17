from flask import Flask, render_template, redirect, url_for, request, jsonify, session
import threading
import logger  # Your modified logger script
from filter_endpoints import filterMask
import requests
import os

app = Flask(__name__)
app.secret_key = 'dojossjos'

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
    logger.run_logger('print_details.hdf5', test_url, 0.01,
                      filterMask(sequence), sequence, stl_path=stl_path, gcode_path=gcode_path)

@app.route("/", methods=["GET"])
def index():
    filenames = list(session.get('uploaded_paths', {}).keys())
    printer_ip = session.get('printer_ip')
    printer_error = session.pop('printer_error', '')
    return render_template("index.html", logging=is_logging, filenames=filenames, printer_ip=printer_ip, printer_error=printer_error)

@app.route("/set-printer", methods=["POST"])
def set_printer():
    ip = request.form.get('printer_ip')
    if ip:
        try:
            resp = requests.get(f"http://{ip}/api/v1/printer", timeout=2)
            if resp.status_code == 200:
                session['printer_ip'] = ip
                session['printer_error'] = ''
            else:
                session['printer_error'] = "Printer did not respond correctly."
        except requests.RequestException:
            session['printer_error'] = "Failed to connect to printer."
    return redirect(url_for('index'))

@app.route("/start")
def start():
    global log_thread, is_logging
    sequence = "100010000000"
    uploaded_paths = session.get('uploaded_paths', {})

    gcode_exists = any(n.endswith('.gcode') for n in uploaded_paths)
    stl_exists = any(n.endswith('.stl') for n in uploaded_paths)

    if not is_logging and gcode_exists and stl_exists:
        printer_ip = session.get('printer_ip')
        log_thread = threading.Thread(target=start_logging, args=(sequence, uploaded_paths, printer_ip))
        log_thread.start()
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
    app.run(debug=True)