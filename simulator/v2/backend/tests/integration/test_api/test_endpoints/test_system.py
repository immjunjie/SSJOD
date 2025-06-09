import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI

from simulator.v2.backend.app.api.endpoints import system

app = FastAPI()
app.include_router(system.router, tags=["System"])

@pytest.mark.asyncio
async def test_get_system():
    """
    Test the /system endpoint to ensure it returns system information.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/system")

    import logging
    logging.info("Status code: %s", response.status_code)
    logging.debug("Response text: %s", response.text)

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict), "Response should be a dictionary representing the system information"