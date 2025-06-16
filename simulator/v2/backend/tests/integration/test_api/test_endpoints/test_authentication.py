import pytest
from simulator.v2.backend.app.api.endpoints.authentication import router
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI


app = FastAPI()
app.include_router(router, tags=["authentication"])

@pytest.mark.asyncio
async def test_auth_verify_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/auth/verify")

    assert response.status_code == 200
    # message == ok
    assert response.json()["message"] == "ok"