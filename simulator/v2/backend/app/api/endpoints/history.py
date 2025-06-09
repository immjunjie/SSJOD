from fastapi import APIRouter, Depends, HTTPException
from simulator.v2.backend.app.domain.models.history_models import HistoriesModel
from simulator.v2.backend.app.infrastructure.repositories.history_repo import HistoryRepo
from simulator.v2.backend.app.services.history_service import HistoryService
import logging
from typing import Annotated

history_logger = logging.getLogger(__name__)
router = APIRouter()

def get_history_repo() -> HistoryRepo:
    """
    Provide a HistoryRepo instance for dependency injection.

    Returns:
        HistoryRepo: A new HistoryRepo instance.
    """
    history_logger.debug("Creating HistoryRepo instance.")
    return HistoryRepo()

def get_history_service(history_repo: HistoryRepo = Depends(get_history_repo)) -> HistoryService:
    """
    Provide a HistoryService instance for dependency injection.

    Args:
        history_repo (HistoryRepo): The history repository instance.

    Returns:
        HistoryService: A new HistoryService instance.
    """
    history_logger.debug("Creating HistoryService instance.")
    return HistoryService(history_repository=history_repo)

@router.get("/history", response_model=HistoriesModel, tags=["History"])
async def get_history(service: Annotated[HistoryService, Depends(get_history_service)]):
    """
    Retrieve all history records.

    Returns:
        HistoriesModel: A model containing a list of history records.

    Raises:
        HTTPException: If an error occurs while fetching the history (500 for server errors).
    """
    try:
        history_logger.debug("Fetching all history records.")
        histories = await service.get_histories()
        history_logger.info("Successfully fetched %d history records.", len(histories.history))
        return histories
    except Exception as e:
        history_logger.exception("Error fetching history records: %s", str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch history records")