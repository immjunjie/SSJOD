import subprocess
import time
import signal
import sys

from backend.app import socketio, app


def start_simulator():
    """
    Launch the FastAPI-based simulator service on port 9000.
    Uses uvicorn in a subprocess to run concurrently with the Flask server.
    """
    print("[Main] Starting simulator service on port 9000...")
    return subprocess.Popen([
        sys.executable, "-m", "uvicorn",
        "simulator.v1.backend.main:app",
        "--host", "127.0.0.1",
        "--port", "9000",
        "--reload"
    ])


def start_backend():
    """
    Launch the Flask + SocketIO backend service on port 5000.
    """
    print("[Main] Starting backend Flask service on port 5000...")
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)


def main():
    # Start the simulator subprocess
    sim_process = start_simulator()

    try:
        # Optional: wait briefly to ensure simulator is ready
        time.sleep(2)

        # Start the backend Flask service
        start_backend()

    except KeyboardInterrupt:
        print("\n[Main] KeyboardInterrupt received. Shutting down...")

    finally:
        # Gracefully terminate the simulator subprocess
        print("[Main] Terminating simulator service...")
        sim_process.send_signal(signal.SIGINT)
        sim_process.wait()
        print("[Main] Shutdown complete.")


if __name__ == "__main__":
    main()