import pytest
from simulator.v2.backend.app.infrastructure.repositories.system_repo import SystemRepo
from simulator.v2.backend.app.domain.models.system_models import SystemModel

@pytest.mark.asyncio
async def test_system_repo():

    repo = SystemRepo()
    result = await repo.get_system()
    assert isinstance(result, SystemModel)