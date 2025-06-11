import pytest
from simulator.v2.backend.app.domain.models.ambient_temperature_models import AmbientTemperatureModel
from simulator.v2.backend.app.infrastructure.repositories.ambient_temperature_repo import AmbientTemperatureRepository
from simulator.v2.backend.app.services.ambient_temperature_service import AmbientTemperatureService

@pytest.mark.asyncio
async def test_get_ambient_temperature():
    # Arrange
    ambient_temperature_service = AmbientTemperatureService(AmbientTemperatureRepository())

    # Act
    result = await ambient_temperature_service.get_ambient_temperature()

    # Assert
    assert isinstance(result, AmbientTemperatureModel), "Result should be an instance of AmbientTemperatureModel"