import webview
import threading
import time
import os
import sys
from flask import Flask
from backend.app import app, socketio

class DesktopPrinterApp:
    def __init__(self):
        self.flask_thread = None
        self.flask_port = 5000
        
    def start_flask_server(self):
        """Start the Flask server in a separate thread"""
        def run_server():
            # Disable Flask's reloader and debug output for desktop use
            socketio.run(app, host='127.0.0.1', port=self.flask_port, debug=False, use_reloader=False)
        
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