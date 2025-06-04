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

    print("Status code:", response.status_code)
    print("Response text:", response.text)

    assert response.status_code == 200
    assert isinstance(response.json()["materials"], list)