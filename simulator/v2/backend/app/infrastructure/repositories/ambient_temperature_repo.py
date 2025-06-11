from simulator.v2.backend.app.domain.models.ambient_temperature_models import AmbientTemperatureModel
import logging

ambient_temperature_logger = logging.getLogger(__name__)

class AmbientTemperatureRepository:
    """
    Repository for getting and setting ambient temperature data.
    """
    def __init__(self) -> None:
        self._ambient_temperature = AmbientTemperatureModel(current=20.0)  # Default temperature

    async def get_ambient_temperature(self) -> AmbientTemperatureModel:
        ambient_temperature_logger.debug(self._ambient_temperature)
        return self._ambient_temperature