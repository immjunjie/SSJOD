import pytest
from simulator.v2.backend.app.infrastructure.repositories.network_repo import NetworkRepo
from simulator.v2.backend.app.domain.models.network_models import Network

@pytest.mark.asyncio
async def test_get_network():
    """
    Test the get_network method of NetworkRepo to ensure it returns a Network instance.
    """
    repo = NetworkRepo()
    result = await repo.get_network()
    assert isinstance(result, Network)
    assert result is not None