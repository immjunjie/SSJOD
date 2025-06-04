from simulator.v2.backend.app.domain.models.network_models import Network, InlineModel, InlineModel0
from typing import Dict
import logging

network_logger = logging.getLogger(__name__)

class NetworkRepo:
    """
    Repository for managing network-related operations using in-memory storage.
    """
    def __init__(self) -> None:
        self.networks: Dict[str, Network] = {
            "current_network": Network(
                ethernet=InlineModel0(connected=True, enabled=True),
                wifi=InlineModel(
                    connected=False,
                    enabled=False,
                    mode="CABLE",
                    ssid="UM-NO-HOTSPOT-NAME-SET"
                ),
                wifi_networks=[]
            )
        }
        network_logger.debug("Network repository initialized with default configuration.")

    async def get_network(self) -> Network:
        """
        Retrieves the current network configuration.
        """
        network_logger.debug("Retrieving current network configuration.")
        return self.networks.get("current_network", Network(ethernet=InlineModel0(), wifi=InlineModel()))

    async def update_network(self, network: Network) -> Network:
        """
        Updates the current network configuration.
        """
        network_logger.debug("Updating network configuration: %s", network)
        self.networks["current_network"] = network
        return self.networks["current_network"]