from typing import List, Any, Coroutine
from simulator.v2.backend.app.domain.models.history_models import HistoryModel, HistoriesModel
import logging

system_logger = logging.getLogger(__name__)

class HistoryRepo:
    """
    Repository for managing system information.

    Insert DataModel Example:

    [
      {
        "time_elapsed": 0,
        "time_estimated": 0,
        "time_total": 0,
        "datetime_started": "2025-06-09T12:17:59.120Z",
        "datetime_finished": "2025-06-09T12:17:59.120Z",
        "datetime_cleaned": "2025-06-09T12:17:59.120Z",
        "result": "Finished",
        "source": "string",
        "reprint_original_uuid": "string",
        "name": "string",
        "uuid": "string"
      }
    ]
    """
    def __init__(self) -> None:
        self.history: HistoryModel = HistoryModel(
            time_elapsed=0,
            time_estimated=0,
            time_total=0,
            datetime_started="2025-06-09T12:17:59.120Z",
            datetime_finished="2025-06-09T12:17:59.120Z",
            datetime_cleaned="2025-06-09T12:17:59.120Z",
            result="Finished",
            source="string",
            reprint_original_uuid="string",
            name="string",
            uuid="string"
        )
        self.histories: HistoriesModel = HistoriesModel(history=[self.history])

    async def get_histories(self) -> HistoriesModel:
        """
        Retrieve all system histories.

        Returns:
            InlineModel: A model containing a list of system histories.
        """
        system_logger.debug("Retrieving all system histories.")
        return self.histories

    # async def insert_history(self, history: History) -> Histories:
    async def insert_history(self, history: HistoryModel) -> HistoriesModel:
        """
        Insert a new system history.

        Args:
            history (InlineModel1): The history to be inserted.

        Returns:
            InlineModel: A model containing the updated list of system histories.
        """
        system_logger.debug(f"Inserting new system history: {history}")
        self.histories.inline_model_1.append(history)
        return self.histories