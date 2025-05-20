from fastapi import APIRouter
from starlette.testclient import TestClient
from datetime import datetime

router = APIRouter()

def get_current_iso_timestamp():
    return datetime.utcnow().isoformat() + "Z"

def get_history_print_job():
    current_time = get_current_iso_timestamp()
    return {
        "time_elapsed": 0,
        "time_estimated": 0,
        "time_total": 0,
        "datetime_started": current_time,
        "datetime_finished": current_time,
        "datetime_cleaned": current_time,
        "result": "Finished",
        "source": "string",
        "reprint_original_uuid": "string",
        "name": "string",
        "uuid": "string"
    }

def get_history_event():
    return {
        "time": get_current_iso_timestamp(),
        "type_id": 0,
        "message": "string",
        "parameters": [
            "string"
        ]
    }

# --- Combined System Info ---
@router.get("/history/print_jobs", tags=["History"])
async def history_print_jobs():
    return [get_history_print_job()]

# --- Individual Routes (same order) ---
@router.get("/history/print_job", tags=["History"])
async def history_print_job_uuid():
    return get_history_print_job()

@router.get("/history/events", tags=["History"])
async def history_events():
    return get_history_event()

# Test the /history routes
if __name__ == "__main__":
    from backend.simulator.main import app
    client = TestClient(app)

    response = client.get("/docs/history/print_jobs")
    print(response.status_code)
    print(response.json())

    response = client.get("/docs/history/events")
    print(response.status_code)
    print(response.json())