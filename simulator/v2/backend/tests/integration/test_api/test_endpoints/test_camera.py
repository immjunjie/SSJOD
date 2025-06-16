import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI

from simulator.v2.backend.app.api.endpoints import camera

app = FastAPI()
app.include_router(camera.router, tags=["camera"])

@pytest.mark.asyncio
async def test_get_camera_feed():
    """
    Test the /camera endpoint to ensure it returns the camera feed correctly.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/camera")

    import logging
    logging.info("Status code: %s", response.status_code)
    logging.debug("Response text: %s", response.text)

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict), "Response should be a dictionary representing the system information"