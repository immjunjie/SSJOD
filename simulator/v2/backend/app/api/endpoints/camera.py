from fastapi import APIRouter, Depends, HTTPException
from simulator.v2.backend.app.domain.models.camera_models import CameraModel
from simulator.v2.backend.app.infrastructure.repositories.camera_repo import CameraRepository
from simulator.v2.backend.app.services.camera_service import CameraService
from typing import List, Annotated
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

camera_repo = CameraRepository()
camera_service = CameraService(camera_repository=camera_repo)

def get_camera_service():
    """
    Provide a CameraService instance for dependency injection.
    """
    logger.debug("Creating CameraService instance.")
    return camera_service

def get_camera_repo():
    """
    Provide a CameraRepository instance for dependency injection.
    """
    logger.debug("Creating CameraRepository instance.")
    return camera_repo

# @router.get("/history", response_model=List[HistoryModel], tags=["History"])
# async def get_history(service: Annotated[HistoryService, Depends(get_history_service)]):
#     """
#     Retrieve all history records.
#
#     Returns:
#         List[HistoryModel]: A list of history records.
#     """
#     try:
#         logger.debug("Fetching all history records.")
#         histories = await service.get_histories()
#         logger.info("Successfully fetched %d history records.", len(histories.history))
#         return histories.history  # Return the history list directly
#     except Exception as e:
#         logger.exception("Error fetching history: records %s", str(e))
#         raise HTTPException(status_code=500, detail="Failed to retrieve history records")

@router.get("/camera", response_model=CameraModel, tags=["Camera"])
async def get_camera_feed(
    service: Annotated[CameraService, Depends(get_camera_service)]
):
    """
    Retrieve the camera feed.

    Returns:
        CameraModel: The camera feed data.
    """
    try:
        logger.debug("Fetching camera feed.")
        camera_feed = await service.get_camera_feed()
        logger.info("Successfully fetched camera feed.")
        return camera_feed
    except Exception as e:
        logger.exception("Error fetching camera feed: %s", str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve camera feed")