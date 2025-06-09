from simulator.v2.backend.app.domain.models.history_models import HistoryModel, HistoriesModel
from simulator.v2.backend.app.infrastructure.repositories.history_repo import HistoryRepo
import logging

history_logger = logging.getLogger(__name__)

class HistoryService:
    """
    Service for handling history operations.
    """
    def __init__(self, history_repository: HistoryRepo):
        """
        Initializes the history service with a repository.

        Args:
            history_repository (HistoryRepo): The history repository instance.
        """
        self.history_repository = history_repository
        history_logger.debug("HistoryService initialized with repository: %s", history_repository)

    async def get_histories(self) -> HistoriesModel:
        """
        Retrieves the list of histories.

        Returns:
            HistoriesModel: A model containing a list of system histories.
        """
        histories = await self.history_repository.get_histories()
        history_logger.debug("Retrieved %d histories", len(histories.history))
        return histories
