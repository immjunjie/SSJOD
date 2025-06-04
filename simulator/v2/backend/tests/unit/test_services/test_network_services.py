import pytest
from simulator.v2.backend.app.domain.models.network_models import Network
from simulator.v2.backend.app.infrastructure.repositories.network_repo import NetworkRepo
from simulator.v2.backend.app.services.network_service import NetworkService

@pytest.mark.asyncio
async def test_get_network_returns_network():
    """
    Test that the NetworkService's get_network method returns a Network object
    """

    # Arrange
    network_service = NetworkService(NetworkRepo())

    # Act
    result = await network_service.get_network()

    # Assert
    assert isinstance(result, Network)
    assert hasattr(result, "wifi")
    assert hasattr(result, "ethernet")