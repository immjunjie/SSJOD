import pytest
from simulator.v2.backend.app.domain.models.system_models import SystemModel
from simulator.v2.backend.app.infrastructure.repositories.system_repo import SystemRepo
from simulator.v2.backend.app.services.system_service import SystemService

@pytest.mark.asyncio
async def test_get_system():
    """
    Test the get_system method of SystemService.
    This test checks if the method returns a SystemModel instance.
    """

    # Arrange
    system_service = SystemService(SystemRepo())

    # Act
    result = await system_service.get_system()

    # Assert
    assert isinstance(result, SystemModel)