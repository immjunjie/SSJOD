from flask import Flask, render_template, redirect, url_for
import threading
import logger  # This will be your modified logger script

app = Flask(__name__)
log_thread = None
is_logging = False

def start_logging():
    global is_logging
    is_logging = True
    logger.run_logger('print_details.hdf5', 'http://143.239.73.224/api/v1/printer', '/Users/sb36/CS3300-Project/backend/extractor/merged/_3DBenchy.stl', '/Users/sb36/CS3300-Project/backend/extractor/merged/UMS5__3DBenchy.gcode', 0.01)  # This function should contain your while loop logic

@app.route("/")
def index():
    return render_template("index.html", logging=is_logging)

@app.route("/start")
def start():
    global log_thread, is_logging
    if not is_logging:
        log_thread = threading.Thread(target=start_logging)
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

if __name__ == "__main__":
    app.run(debug=True)