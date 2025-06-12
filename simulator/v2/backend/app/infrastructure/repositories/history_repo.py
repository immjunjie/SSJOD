import uuid
from typing import List, Any, Coroutine
from simulator.v2.backend.app.domain.models.history_models import HistoryModel, HistoriesModel
import logging

system_logger = logging.getLogger(__name__)

class HistoryRepo:
    """
    Repository for managing system history information.

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
        self.histories: HistoriesModel = HistoriesModel(history=[])
        sample_history = HistoryModel(
            time_elapsed=0,
            time_estimated=0,
            time_total=0,
            datetime_started="2025-06-09T12:17:59.120Z",
            datetime_finished="2025-06-09T12:17:59.120Z",
            datetime_cleaned="2025-06-09T12:17:59.120Z",
            result="Finished",
            source="string",
            reprint_original_uuid=str(uuid.uuid4()),
            name="string",
            uuid=str(uuid.uuid4())
        )
        self.histories.history.append(sample_history)
        system_logger.debug("HistoryRepo initialized with sample history: %s", sample_history)

    async def get_histories(self) -> HistoriesModel:
        """
        Retrieve all system histories.

        Returns:
            HistoriesModel: A model containing a list of system histories.
        """
        system_logger.debug("Retrieving all system histories. Count: %d", len(self.histories.history))
        return self.histories

    async def insert_history(self, history: HistoryModel) -> HistoriesModel:
        """
        Insert a new system history.

        Args:
            history (HistoryModel): The history to be inserted.

        Returns:
            HistoriesModel: A model containing the updated list of system histories.
        """
        system_logger.debug("Inserting new system history: %s", history)
        self.histories.history.append(history)
        system_logger.info("Inserted history with UUID: %s", history.uuid)
        return self.histories