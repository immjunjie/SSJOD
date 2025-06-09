import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI

from simulator.v2.backend.app.api.endpoints import history

app = FastAPI()
app.include_router(history.router, tags=["History"])

@pytest.mark.asyncio
async def test_get_history():
    """
    Test the /history endpoint to ensure it returns a list of history records.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/history")

    import logging
    logging.info("Status code: %s", response.status_code)
    logging.debug("Response text: %s", response.text)

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
