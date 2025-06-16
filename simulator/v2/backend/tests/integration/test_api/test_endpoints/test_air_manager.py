import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI

from simulator.v2.backend.app.api.endpoints.air_manager import router

app = FastAPI()
app.include_router(router, tags=["AirManager"])

@pytest.mark.asyncio
async def test_get_airmanager():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/airmanager")

    assert response.status_code == 200
    # isInstance check for the response data
    assert isinstance(response.json(), dict)