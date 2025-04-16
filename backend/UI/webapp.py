from flask import Flask, render_template, redirect, url_for, request
import threading
import logger
from filter_endpoints import filterMask



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
log_thread = None
is_logging = False

def start_logging(sequence):
    global is_logging
    is_logging = True
    logger.run_logger('print_details.hdf5','http://143.239.73.224/api/v1/printer','backend/UI/_3DBenchy.stl','backend/UI/UMS5__3DBenchy.gcode',0.01,filterMask(sequence), sequence)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", logging=is_logging, listOfEndpoints=listOfEndpoints, sequence=current_sequence)

@app.route("/start", methods=["POST"])
def start():
    global log_thread, is_logging, current_sequence

    sequence = ""
    for i in range(len(listOfEndpoints)):
        checkbox_name = f"ep{i}"
        sequence += '1' if checkbox_name in request.form else '0'

    current_sequence = sequence  

    if not is_logging:
        log_thread = threading.Thread(target=start_logging, args=(sequence,))
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

if __name__ == "__main__":
    app.run(debug=True)