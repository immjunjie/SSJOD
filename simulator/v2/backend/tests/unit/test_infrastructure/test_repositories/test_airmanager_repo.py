import pytest
from simulator.v2.backend.app.infrastructure.repositories.airmanager_repo import AirManagerRepository
from simulator.v2.backend.app.domain.models.airmanager_models import AirManagerModel

@pytest.mark.asyncio
async def test_airmanager_repo():

    repo = AirManagerRepository()
    result = await repo.get_airmanager()
    assert isinstance(result, AirManagerModel)