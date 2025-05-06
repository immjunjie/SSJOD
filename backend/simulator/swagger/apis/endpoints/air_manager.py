from fastapi import APIRouter
from starlette.testclient import TestClient

router = APIRouter()

def get_air_manager():
    return {
      "ambient_temperature": 23,
      "exhaust_temperature": 26,
      "fan_speed": 2405,
      "filter_age": 83,
      "filter_max_age": 1500,
      "filter_status": "peak_performance",
      "firmware_version": "1639647304",
      "status": "available"
    }

@router.get("/air_manager", tags=["AirManager"])
def air_manager():
    return get_air_manager()

# Test the /air_manager route
if __name__ == "__main__":
    from backend.simulator.main import app
    client = TestClient(app)
    response = client.get("/docs/air_manager")
    print(response.status_code)
    print(response.json())