from flask import Flask, render_template, redirect, url_for, request, jsonify, session, send_file  # Web framework and utilities
from flask_socketio import SocketIO  # WebSocket support for real-time updates
import threading  # Background threads for non-blocking logging
import logger  # Custom logger module (see logger.py below)
from filter_endpoints import filterMask  # Function to filter endpoints based on user selection
import requests  # HTTP client for printer API
import os  # Filesystem operations
import re

# List of telemetry endpoints to choose from
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

# Bitstring representing which endpoints are currently enabled (default: all on)
current_sequence = "1" * len(listOfEndpoints)

# Initialize Flask app and SocketIO
app = Flask(__name__)
app.secret_key = 'dojossjod'  # Session encryption key
socketio = SocketIO(app)

# Global variables for logging thread control
log_thread = None
is_logging = False

# Configure upload and detail storage folders
UPLOAD_FOLDER = 'uploads'
DETAILS_FOLDER = 'Print_details_folder'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DETAILS_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def start_logging(sequence, uploaded_paths, printer_ip, selected_filename, duration_seconds=10):
    # Prepare file paths and HDF5 filename
    gcode_path = next((p for n, p in uploaded_paths.items() if n.endswith('.gcode')), None)
    stl_path = next((p for n, p in uploaded_paths.items() if n.endswith('.stl')), None)

    if not (gcode_path and stl_path and printer_ip):
        print("Missing G-code, STL file, or printer IP.")
        return

    # Determine HDF5 filename (either selected or auto-incremented)
    if selected_filename and selected_filename != "New":
        hdf5_filename = os.path.join(DETAILS_FOLDER, selected_filename)
    else:
        existing = [f for f in os.listdir(DETAILS_FOLDER) if f.startswith("print_details_") and f.endswith(".hdf5")]
        # Extract indices to auto-increment
        indices = [int(f.split("_")[-1].split(".")[0]) for f in existing if f.split("_")[-1].split(".")[0].isdigit()]
        next_index = max(indices) + 1 if indices else 0
        hdf5_filename = os.path.join(DETAILS_FOLDER, f"print_details_{next_index}.hdf5")

    # Verify printer connectivity
    test_url = f"http://{printer_ip}/api/v1/printer"
    try:
        response = requests.get(test_url, timeout=2)
        if response.status_code != 200:
            print(f"Printer at {printer_ip} responded with status {response.status_code}. Aborting logger.")
            return
    except requests.RequestException as e:
        print(f"Could not reach printer at {printer_ip}: {e}")
        return

    # Launch logger in current thread (logger handles its own loop)
    global is_logging
    is_logging = True
    # Pass the duration limit to the logger
    logger.run_logger_with_socket(
        socketio=socketio,
        hdf5_filename=hdf5_filename,
        base_url=test_url,
        endpoints=filterMask(sequence),
        sequence=sequence,
        stl_path=stl_path,
        gcode_path=gcode_path,
        max_duration=duration_seconds
    )


# Define Flask routes for UI and control
@app.route("/")
def index():
    # Display main page with current state, uploaded files, and saved logs
    filenames = list(session.get('uploaded_paths', {}).keys())
    
    printer_ip = session.get('printer_ip')
    printer_error = session.pop('printer_error', '')

    existing_files = ["New"] + sorted(f for f in os.listdir(DETAILS_FOLDER) if f.endswith('.hdf5'))
    selected_file = session.get('selected_hdf5_file', 'New')

    return render_template(
        "index.html",
        logging=is_logging,
        filenames=filenames,
        printer_ip=printer_ip,
        printer_error=printer_error,
        listOfEndpoints=listOfEndpoints,
        sequence=current_sequence,
        existing_files=existing_files,
        selected_file=selected_file
    )

@app.route("/set-printer", methods=["POST"])
def set_printer():
    # Save printer IP after validating printer API docs endpoint
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
    # Parse form, start background logging thread if not already running
    global log_thread, is_logging, current_sequence
    uploaded_paths = session.get('uploaded_paths', {})

    selected_filename = request.form.get('existing_file', 'New')
    session['selected_hdf5_file'] = selected_filename

    # Build bitstring for enabled endpoints
    sequence = "".join(
        '1' if f"ep{i}" in request.form else '0'
        for i in range(len(listOfEndpoints))
    )
    current_sequence = sequence

    gcode_exists = any(n.endswith('.gcode') for n in uploaded_paths)
    stl_exists = any(n.endswith('.stl') for n in uploaded_paths)

    if not is_logging and gcode_exists and stl_exists:
        printer_ip = session.get('printer_ip')
        if request.form.get("unlimited_duration"):
            duration_seconds = None  # or some sentinel like 0
        else:
            h = int(request.form.get("hours", 0))
            m = int(request.form.get("minutes", 0))
            s = int(request.form.get("seconds", 0))
            duration_seconds = h * 3600 + m * 60 + s

        def run_and_reset():
            global is_logging
            try:
                start_logging(sequence, uploaded_paths, printer_ip, selected_filename, duration_seconds)
            finally:
                is_logging = False
                logger.stop_logger()
                socketio.emit('logging_stopped')
        if duration_seconds and duration_seconds <= 0:
            session['printer_error'] = "Logging duration must be greater than zero."
            return redirect(url_for("index"))
        log_thread = threading.Thread(target=run_and_reset)
        log_thread.start()
        is_logging = True

    return redirect(url_for("index"))

@app.route("/stop")
def stop():
    # Stop logging and join thread
    global is_logging, log_thread
    is_logging = False
    logger.stop_logger()
    if log_thread:
        log_thread.join()
    return redirect(url_for("index"))

@app.route('/upload', methods=['POST'])
def upload():
    # Handle G-code/STL file uploads via AJAX
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
    # Return JSON of currently uploaded filenames
    uploaded_paths = session.get('uploaded_paths', {})
    return jsonify(files=list(uploaded_paths.keys()))

@app.route('/delete-file/<filename>', methods=['POST'])
def delete_file(filename):
    # Remove file from session and filesystem
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
    # Run the SocketIO app for real-time updates, debug enabled 1
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)