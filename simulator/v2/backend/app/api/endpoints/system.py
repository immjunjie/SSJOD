from fastapi import APIRouter, Depends, HTTPException
from simulator.v2.backend.app.domain.models.system_models import SystemModel
from simulator.v2.backend.app.infrastructure.repositories.system_repo import SystemRepo
from simulator.v2.backend.app.services.system_service import SystemService
import logging

system_logger = logging.getLogger(__name__)
router = APIRouter()

system_repository = SystemRepo()
system_service = SystemService(system_repository=system_repository)

def get_system_repo():
    """
    Get the SystemRepo instance.
    """
    system_logger.debug("Get the SystemRepo instance.")
    return system_repository

def get_system_service():
    """
    Get the SystemService instance.
    """
    system_logger.debug("Get the SystemService instance.")
    return system_service

@router.get("/system", response_model=SystemModel, tags=["System"])
async def get_system(service: SystemService = Depends(get_system_service)):
    """
    Retrieve system information.

    Returns:
            A SystemModel containing system information.

    Raises:
        HTTPException: If an error occurs while fetching system information.
    """
    try:
        system_logger.debug("Request received to fetch system information.")
        system_info = await service.get_system()
        system_logger.debug("System information fetched successfully: %s", system_info)
        return system_info
    except Exception as e:
        system_logger.error("Error fetching system information: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")