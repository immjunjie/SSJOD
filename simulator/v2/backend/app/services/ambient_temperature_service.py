from simulator.v2.backend.app.domain.models.ambient_temperature_models import AmbientTemperatureModel
from simulator.v2.backend.app.infrastructure.repositories.ambient_temperature_repo import AmbientTemperatureRepository
import logging

ambient_temperature_logger = logging.getLogger(__name__)

class AmbientTemperatureService:
    """
    Service for handling ambient temperature operations.
    """
    def __init__(self, ambient_temperature_repository: AmbientTemperatureRepository):
        """
        Initializes the AmbientTemperatureService with a repository.
        """
        self.ambient_temperature_repository = ambient_temperature_repository
        ambient_temperature_logger.debug("AmbientTemperatureService initialized with repository: %s", ambient_temperature_repository)

    async def get_ambient_temperature(self) -> AmbientTemperatureModel:
        """
        Retrieves the ambient temperature information.
        """

        ambient_temperature_logger.debug("AmbientTemperatureService retrieving ambient temperature info")
        ambient_temperature = await self.ambient_temperature_repository.get_ambient_temperature()
        ambient_temperature_logger.debug("Ambient temperature retrieved: %s", ambient_temperature)
        return ambient_temperature