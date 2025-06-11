import pytest
from simulator.v2.backend.app.infrastructure.repositories.ambient_temperature_repo import AmbientTemperatureRepository
from simulator.v2.backend.app.domain.models.ambient_temperature_models import AmbientTemperatureModel

@pytest.mark.asyncio
async def test_get_ambient_temperature():

    repo = AmbientTemperatureRepository()

    result = await repo.get_ambient_temperature()

    assert isinstance(result, AmbientTemperatureModel)
    assert isinstance(result.current, float)