from simulator.v2.backend.app.domain.models.airmanager_models import AirManagerModel
from simulator.v2.backend.app.infrastructure.repositories.airmanager_repo import AirManagerRepository
import logging

airmanager_logger = logging.getLogger(__name__)

class AirManagerService:
    """
    Service for handling operations related to AirManager.
    """
    def __init__(self, airmanager_repository: AirManagerRepository):
        """
        Initializes the  AirManagerService with a repository for AirManager operations.
        """
        self.airmanager_repository = airmanager_repository
        airmanager_logger.debug("AirManagerService initialized with repository: %s", airmanager_repository)

    async def get_airmanager(self) -> AirManagerModel:
        """
        Retrieves the airmanager information from the repository.
        """
        airmanager_logger.debug("Retrieving AirManager information")
        airmanager = await self.airmanager_repository.get_airmanager()
        airmanager_logger.debug("Retrieved AirManager information: %s", airmanager)
        return airmanager