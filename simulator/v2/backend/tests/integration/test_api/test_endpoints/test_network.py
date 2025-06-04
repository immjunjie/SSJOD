import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI

from simulator.v2.backend.app.api.endpoints import network

app = FastAPI()
app.include_router(network.router, tags=["network"])

@pytest.mark.asyncio
async def test_get_network():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/network")

    print("Status code:", response.status_code)
    print("Response text:", response.text)

    assert response.status_code == 200

    data = response.json()
    assert "wifi" in data
    assert "ethernet" in data
    assert isinstance(data.get("wifi_networks", []), list)