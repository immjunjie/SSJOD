import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI

from simulator.v2.backend.app.api.endpoints import printjob

app = FastAPI()
app.include_router(printjob.router, tags=["printjob"])

@pytest.mark.asyncio
async def test_get_printjob():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/printjob")

    import logging
    logging.info("Status code: %s", response.status_code)
    logging.debug("Response text: %s", response.text)

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list), "Response should be a list of print jobs"


@pytest.mark.asyncio
async def test_create_print_job():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        """
        DataModel for a print job.
        
        class PrintJobModel(BaseModel):
            time_elapsed: int
            time_total: int
            datetime_started: str = None
            datetime_finished: str = None
            datetime_cleaned: str = None
            source: str = None
            source_user: str = None
            source_application: str = None
            name: str = None
            uuid: str
            reprint_original_uuid: str = None
            progress: float = 0.0
            state: str = 'none'  # Possible states: 'none', 'printing', 'pausing', 'paused', 'resuming', 'pre_print', 'post_print', 'wait_cleanup', 'wait_user_action'
            result: str = 'Failed'  # Possible results: 'Failed', 'Aborted', 'Finished'
        """
        job_data = {
            "time_elapsed": 0,
            "time_total": 100,
            "datetime_started": None,
            "datetime_finished": None,
            "datetime_cleaned": None,
            "source": "test_source",
            "source_user": "test_user",
            "pause_source": None,
            "source_application": "test_app",
            "name": "Test Print Job",
            "uuid": "123e4567-e89b-12d3-a456-426614174000",
            "reprint_original_uuid": None,
            "progress": 0.0,
            "state": "none",
            "result": "Failed"
        }

        response = await ac.post("/printjob", json=job_data)
        logger.debug("Status code: %s", response.status_code)
        logger.debug("Response text: %s", response.text)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict), "Response should be a dictionary representing the print job"
        assert data["uuid"] == job_data["uuid"], "UUID of the created print job should match the input"
