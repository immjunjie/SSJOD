from fastapi import APIRouter, Depends, HTTPException
from simulator.v2.backend.app.domain.models.ambient_temperature_models import AmbientTemperatureModel
from simulator.v2.backend.app.infrastructure.repositories.ambient_temperature_repo import AmbientTemperatureRepository
from simulator.v2.backend.app.services.ambient_temperature_service import AmbientTemperatureService
import logging

ambient_temperature_logger = logging.getLogger(__name__)
router = APIRouter()

ambient_temperature_repository = AmbientTemperatureRepository()
ambient_temperature_service = AmbientTemperatureService(ambient_temperature_repository=ambient_temperature_repository)

def get_ambient_temperature():
    """
    Get the AmbientTemperatureRepository instance.
    """
    ambient_temperature_logger.debug("Get the AmbientTemperatureRepository instance.")
    return ambient_temperature_repository

def get_ambient_temperature_service():
    """
    Get the AmbientTemperatureService instance.
    """
    ambient_temperature_logger.debug("Get the AmbientTemperatureService instance.")
    return ambient_temperature_service

@router.get("/ambient_temperature", response_model=AmbientTemperatureModel, tags=["Ambient_temperature"])
async def get_ambient_temperature(service: AmbientTemperatureService = Depends(get_ambient_temperature_service)):
    """
    Retrieve ambient temperature information.

    Returns:
            An AmbientTemperatureModel containing ambient temperature information.

    Raises:
        HTTPException: If an error occurs while fetching ambient temperature information.
    """
    try:
        ambient_temperature_logger.debug("Request received to fetch ambient temperature information.")
        temperature_info = await service.get_ambient_temperature()
        ambient_temperature_logger.debug("Ambient temperature information fetched successfully: %s", temperature_info)
        return temperature_info
    except Exception as e:
        ambient_temperature_logger.error("Error fetching ambient temperature information: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

