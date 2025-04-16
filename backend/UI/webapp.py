from flask import Flask, render_template, redirect, url_for, request, jsonify, session
import threading
import logger  # This will be your modified logger script
from filter_endpoints import filterMask
import os

app = Flask(__name__)
app.secret_key = 'dojossjos'

skip_cleanup = False
log_thread = None
is_logging = False
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def start_logging(sequence, uploaded_paths):
    gcode_path = next((p for n, p in uploaded_paths.items() if n.endswith('.gcode')), None)
    stl_path = next((p for n, p in uploaded_paths.items() if n.endswith('.stl')), None)
    print(gcode_path)
    print(stl_path)
    if gcode_path and stl_path:
        global is_logging
        is_logging = True
        logger.run_logger('print_details.hdf5', 'http://143.239.73.224/api/v1/printer', 0.01, filterMask(sequence), sequence, stl_path=stl_path, gcode_path=gcode_path)  # This function should contain your while loop logic
    else:
        print("Missing G-code or STL file.")

@app.route("/", methods=["GET"])
def index():
    filenames = list(session.get('uploaded_paths', {}).keys())
    return render_template("index.html", logging=is_logging, filenames=filenames)

@app.route("/start")
def start():
    global log_thread, is_logging
    sequence = "100010000000"
    uploaded_paths = session.get('uploaded_paths', {})
    print("Session contents:", uploaded_paths)

    if not is_logging:
        log_thread = threading.Thread(target=start_logging, args=(sequence, uploaded_paths))
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
    app.run(debug=True)