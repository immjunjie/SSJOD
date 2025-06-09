from fastapi import APIRouter, Depends, HTTPException
from simulator.v2.backend.app.domain.models.history_models import HistoryModel, HistoriesModel
from simulator.v2.backend.app.infrastructure.repositories.history_repo import HistoryRepo
from simulator.v2.backend.app.services.history_service import HistoryService
from typing import List, Annotated
import logging

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

def get_history_repo() -> HistoryRepo:
    """
    Provide a HistoryRepo instance for dependency injection.
    """
    logger.debug("Creating HistoryRepo instance.")
    return HistoryRepo()

def get_history_service(history_repo: HistoryRepo = Depends(get_history_repo)) -> HistoryService:
    """
    Provide a HistoryService instance for dependency injection.
    """
    logger.debug("Creating HistoryService instance.")
    return HistoryService(history_repository=history_repo)

@router.get("/history", response_model=List[HistoryModel], tags=["History"])
async def get_history(service: Annotated[HistoryService, Depends(get_history_service)]):
    """
    Retrieve all history records.

    Returns:
        List[HistoryModel]: A list of history records.
    """
    try:
        logger.debug("Fetching all history records.")
        histories = await service.get_histories()
        logger.info("Successfully fetched %d history records.", len(histories.history))
        return histories.history  # Return the history list directly
    except Exception as e:
        logger.exception("Error fetching history: records %s", str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve history records")

@router.post("/history", response_model=List[HistoryModel], tags=["History"])
async def insert_history(history: HistoryModel, service: Annotated[HistoryService, Depends(get_history_service)]):
    """
    Insert a new history record.

    Returns:
        List[HistoryModel]: The updated list of history records.
    """
    try:
        logger.debug("Inserting history record: %s", history)
        histories = await service.history_repository.insert_history(history)
        logger.info("Successfully inserted history record with UUID: %s", history.uuid)
        return histories.history  # Return the history list directly
    except Exception as e:
        logger.exception("Error inserting history: record %s", str(e))
        raise HTTPException(status_code=500, detail="Failed to insert history record")