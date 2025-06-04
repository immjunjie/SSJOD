import webview
import threading
import time
import os
import sys
import traceback

#error log
LOG_FILE = os.path.expanduser("~/Desktop/3d_printer_logger_error.log")
sys.stdout = open(LOG_FILE, 'w')
sys.stderr = sys.stdout

def log_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr)

# Catch all unhandled exceptions
sys.excepthook = log_exception



# For PyInstaller, we need to handle the frozen state
if getattr(sys, 'frozen', False):
    # Running in a PyInstaller bundle
    bundle_dir = sys._MEIPASS
    # Add bundle directory to path
    sys.path.insert(0, bundle_dir)
    # Change working directory to bundle directory
    os.chdir(bundle_dir)
else:
    # Add the current directory to Python path for imports
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

from flask import Flask

try:
    from backend.app import app, socketio
    print("Successfully imported backend modules")
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Python path: {sys.path}")
    print(f"Current directory: {os.getcwd()}")
    
    # Debug: check if backend directory exists
    if os.path.exists('backend'):
        print("Backend directory found")
        print(f"Backend contents: {os.listdir('backend')}")
    else:
        print("Backend directory NOT found")
        print(f"Available directories: {[d for d in os.listdir('.') if os.path.isdir(d)]}")
    
    sys.exit(1)

class DesktopPrinterApp:
    def __init__(self):
        self.flask_thread = None
        self.flask_port = 5000
        
    def start_flask_server(self):
        """Start the Flask server in a separate thread"""
        def run_server():
            # Disable Flask's reloader and debug output for desktop use
            socketio.run(app, host='127.0.0.1', port=self.flask_port, debug=False, use_reloader=False, allow_unsafe_werkzeug=True)
        
        self.flask_thread = threading.Thread(target=run_server, daemon=True)
        self.flask_thread.start()
        
        # Wait a moment for the server to start
        time.sleep(2)
    
    def create_desktop_window(self):
        """Create the desktop window with the web interface"""
        # Start Flask server
        self.start_flask_server()
        
        # Create webview window
        webview.create_window(
            title='3D Printer Monitor',
            url=f'http://127.0.0.1:{self.flask_port}',
            width=1200,
            height=800,
            min_size=(800, 600),
            resizable=True,
            maximized=False,
            on_top=False
        )
        
        # Start the webview (this will block until window is closed)
        webview.start(debug=False)

def main():
    app_instance = DesktopPrinterApp()
    app_instance.create_desktop_window()

if __name__ == "__main__":
    main()