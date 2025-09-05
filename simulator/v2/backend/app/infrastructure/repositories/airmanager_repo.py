from typing import List
from simulator.v2.backend.app.domain.models.airmanager_models import AirManagerModel
import logging

airmanager_logger = logging.getLogger(__name__)

class AirManagerRepository:
    """
    Repository to get and manage air manager data.

    Insert DataModel Example:  
    {
      "firmware_version": "string",
      "filter_age": 0,
      "filter_max_age": 0,
      "filter_status": "unknown",
      "status": "error",
      "fan_speed": 0
    }
    """
    def __init__(self) -> None:
        self.air_manager_info = AirManagerModel(
            firmware_version="string",
            filter_age=0,
            filter_max_age=0,
            filter_status="unknown",
            status="error",
            fan_speed=0
        )

    async def get_airmanager(self) -> AirManagerModel:
        airmanager_logger.debug("Retrieving air manager information.")
        return self.air_manager_info