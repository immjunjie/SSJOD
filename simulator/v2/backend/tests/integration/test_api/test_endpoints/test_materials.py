import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
import traceback

from simulator.v2.backend.app.api.endpoints import materials

app = FastAPI()
app.include_router(materials.router, tags=["materials"])

@pytest.mark.asyncio
async def test_get_materials():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/materials")

    print("\nStatus code:", response.status_code)
    print("Response text:", response.text)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_materials_response_type():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/materials")

    print("\nResponse type:", type(response.json()))
    assert isinstance(response.json(), list)
