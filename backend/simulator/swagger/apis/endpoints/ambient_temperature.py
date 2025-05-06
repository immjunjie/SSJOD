from fastapi import APIRouter
from starlette.testclient import TestClient

router = APIRouter()

def get_ambient_temperature():
    return {
     "current": 29.36
    }

# --- Combined Info ---
@router.get("/ambient_temperature", tags=["Ambient_temperature"])
async def ambient_temperature():
    return get_ambient_temperature()

# Test the /ambient_temperature route
if __name__ == "__main__":
    from backend.simulator.main import app
    client = TestClient(app)
    response = client.get("/docs/ambient_temperature")
    print(response.status_code)
    print(response.json())