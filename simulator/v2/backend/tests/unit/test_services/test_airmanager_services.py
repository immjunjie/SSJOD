import pytest
from simulator.v2.backend.app.domain.models.airmanager_models import AirManagerModel
from simulator.v2.backend.app.infrastructure.repositories.airmanager_repo import AirManagerRepository
from simulator.v2.backend.app.services.airmanager_service import AirManagerService

@pytest.mark.asyncio
async def test_get_air_manager():
    """
    Test the get_air_manager method of AirManagerService.
    """

    # Arrange
    airmanager_service = AirManagerService(AirManagerRepository())

    # Act
    result = await airmanager_service.get_airmanager()

    # Assert
    assert isinstance(result, AirManagerModel)