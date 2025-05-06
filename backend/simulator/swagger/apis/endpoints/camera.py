from fastapi import APIRouter
from starlette.testclient import TestClient

router = APIRouter()

def get_camera():
    return {
     "feed": "http://143.239.73.224:8080/?action=stream"
    }

def get_camera_feed():
    return "http://143.239.73.224:8080/?action=stream"

def get_camera_stream_by_index():
    return "http://143.239.73.224/api/v1/camera/0/stream"

def get_camera_snapshot_by_index():
    return "http://143.239.73.224/api/v1/camera/0/snapshot"



@router.get("/camera", tags=["Camera"])
def camera():
    return get_camera()

@router.get("/camera/feed", tags=["Camera"])
def camera_feed():
    return get_camera_feed()

@router.get("/camera/{index}/stream", tags=["Camera"])
def camera_steam_by_index():
    return get_camera_stream_by_index()

@router.get("/camera/{index}/snapshot", tags=["Camera"])
def camera_snapshot_by_index():
    return get_camera_snapshot_by_index()

# Test the route
if __name__ == "__main__":
    from backend.simulator.main import app
    client = TestClient(app)
    response = client.get("/docs/camera")
    print(response.status_code)
    print(response.json())