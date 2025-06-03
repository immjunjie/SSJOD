import pytest
from httpx import AsyncClient, ASGITransport
from simulator.v2.backend.main import app

@pytest.mark.asyncio
async def test_get_printer():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/printer")
        assert response.status_code == 200
        assert response.json()["status"] == "idle"
        assert response.json()["bed"]["temperature"]["current"] == 24.7

@pytest.mark.asyncio
async def test_set_printer_status():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Test setting to printing
        response = await client.post("/api/v1/printer/status", json={"status": "printing"})
        assert response.status_code == 200
        assert response.json()["status"] == "printing"

        # Test setting to idle
        response = await client.post("/api/v1/printer/status", json={"status": "idle"})
        assert response.status_code == 200
        assert response.json()["status"] == "idle"

        # Test invalid status
        response = await client.post("/api/v1/printer/status", json={"status": "invalid"})
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_printer_status():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Set status to printing
        await client.post("/api/v1/printer/status", json={"status": "printing"})
        response = await client.get("/api/v1/printer/status")
        assert response.status_code == 200
        assert response.json()["status"] == "printing"

        # Set status to idle
        await client.post("/api/v1/printer/status", json={"status": "idle"})
        response = await client.get("/api/v1/printer/status")
        assert response.status_code == 200
        assert response.json()["status"] == "idle"

if __name__ == "__main__":
    import asyncio

    asyncio.run(test_get_printer())
    asyncio.run(test_set_printer_status())
    asyncio.run(test_get_printer_status())