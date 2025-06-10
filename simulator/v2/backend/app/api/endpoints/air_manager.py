from fastapi import APIRouter, Depends, HTTPException
from simulator.v2.backend.app.domain.models.airmanager_models import AirManagerModel
from simulator.v2.backend.app.infrastructure.repositories.airmanager_repo import AirManagerRepository
from simulator.v2.backend.app.services.airmanager_service import AirManagerService
import logging

airmanager_logger = logging.getLogger(__name__)
router = APIRouter()

airmanager_repository = AirManagerRepository()
airmanager_service = AirManagerService(airmanager_repository=airmanager_repository)

def get_airmanager_repository():
    """
    Get the AirManagerRepository instance.
    """
    airmanager_logger.debug("Get the AirManagerRepository instance.")
    return airmanager_repository

def get_airmanager_service():
    """
    Get the AirManagerService instance.
    """
    airmanager_logger.debug("Get the AirManagerService instance.")
    return airmanager_service

@router.get("/airmanager", response_model=AirManagerModel,tags=["AirManager"])
async def get_airmanager(service: AirManagerService = Depends(get_airmanager_service)):
    """
    Retrieve the AirManager information.
    """
    try:
        airmanager_logger.debug("Handling /airmanager request")
        airmanager_info = await service.get_airmanager()
        airmanager_logger.debug("AirManager information retrieved successfully")
        return airmanager_info
    except Exception as e:
        airmanager_logger.error("Error fetching AirManager information: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")