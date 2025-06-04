from simulator.v2.backend.app.domain.models.network_models import Network
from simulator.v2.backend.app.infrastructure.repositories.network_repo import NetworkRepo
import logging

network_logger = logging.getLogger(__name__)

class NetworkService:
    """
    Service for handling network-related operations.
    """
    def __init__(self, network_repository: NetworkRepo):
        self.network_repository = network_repository
        network_logger.debug("NetworkService initialized with repository: %s", network_repository)

    async def get_network(self) -> Network:
        """
        Fetches the current network configuration from the repository.
        """
        network_logger.debug("Fetching network configuration from repository.")
        network = await self.network_repository.get_network()
        network_logger.debug("Network configuration fetched successfully: %s", network)
        return network

    async def update_network(self, network: Network) -> Network:
        """
        Updates the network configuration in the repository.
        """
        network_logger.debug("Updating network configuration: %s", network)
        updated_network = await self.network_repository.update_network(network)
        network_logger.debug("Network configuration updated successfully: %s", updated_network)
        return updated_network