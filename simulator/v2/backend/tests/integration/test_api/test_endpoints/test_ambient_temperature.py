import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI

from simulator.v2.backend.app.api.endpoints import ambient_temperature

app = FastAPI()
app.include_router(ambient_temperature.router, tags=["ambient_temperature"])

@pytest.mark.asyncio
async def test_get_ambient_temperature():
    """
    Test the /ambient-temperature endpoint to ensure it returns ambient temperature information.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/ambient_temperature")

    import logging
    logging.info("Status code: %s", response.status_code)
    logging.debug("Response text: %s", response.text)

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict), "Response should be a dictionary representing the system information"