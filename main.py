# /main.py
from backend.app import socketio, app


if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
