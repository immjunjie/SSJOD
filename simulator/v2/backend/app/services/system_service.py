from simulator.v2.backend.app.domain.models.system_models import SystemModel
from simulator.v2.backend.app.infrastructure.repositories.system_repo import SystemRepo
import logging

system_logger = logging.getLogger(__name__)

class SystemService:
    """
    Service for handling system-related operations.
    """
    def __init__(self, system_repository: SystemRepo):
        """
        Initializes the SystemService with a repository for system operations.
        """
        self.system_repository = system_repository
        system_logger.debug("SystemService initialized with repository: %s", system_repository)

    async def get_system(self) -> SystemModel:
        """
        Retrieves the system information from the repository.
        """
        system_logger.debug("Retrieving system information")
        system = await self.system_repository.get_system()
        system_logger.debug("Retrieved system information: %s", system)
        return system