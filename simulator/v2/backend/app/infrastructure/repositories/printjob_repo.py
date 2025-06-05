from typing import List
from simulator.v2.backend.app.domain.models.printjob_models import PrintJobModel
import logging

printjob_logger = logging.getLogger(__name__)

class PrintJobRepo:
    """
    Repository for managing print jobs.
    """

    """
    Insert DataModel Example:  
    {
      "datetime_cleaned": "",
      "datetime_finished": "2025-06-04T13:28:41",
      "datetime_started": "2025-06-04T10:38:07",
      "name": "UMS5_SSJOD Update",
      "pause_source": "",
      "progress": 1,
      "reprint_original_uuid": "",
      "result": "Finished",
      "source": "WEB_API",
      "source_application": "Ultimaker Connect",
      "source_user": "",
      "state": "wait_cleanup",
      "time_elapsed": 9803,
      "time_total": 9796,
      "uuid": "ab476aa2-d234-42e1-9618-df6e250ab9c1"
    }
    """
    def __init__(self) -> None:
        self.printjobs: List[PrintJobModel] = [
            PrintJobModel(
                datetime_cleaned="",
                datetime_finished="2025-06-04T13:28:41",
                datetime_started="2025-06-04T10:38:07",
                name="UMS5_SSJOD Update",
                source="WEB_API",
                source_application="Ultimaker Connect",
                source_user="",
                pause_source="",
                progress=1,
                reprint_original_uuid="",
                result="Finished",
                state="wait_cleanup",
                time_elapsed=9803,
                time_total=9796,
                uuid="ab476aa2-d234-42e1-9618-df6e250ab9c1"
            )
        ]

    async def get_printjobs(self) -> List[PrintJobModel]:
        printjob_logger.debug("Retrieving all print jobs.")
        return self.printjobs

    async def create_print_job(self, job: PrintJobModel) -> PrintJobModel:
        printjob_logger.debug("Creating print job: %s", job)
        self.printjobs.append(job)
        printjob_logger.debug("Print job created successfully: %s", job)
        return job