from simulator.v2.backend.app.domain.models.printjob_models import PrintJobModel
from simulator.v2.backend.app.infrastructure.repositories.printjob_repo import PrintJobRepo, printjob_logger
import logging

printjob_logger = logging.getLogger(__name__)

class PrintJobService:
    """
    Service for handling print job operations.
    """
    def __init__(self, printjob_repository: PrintJobRepo):
        self.printjob_repository = printjob_repository
        printjob_logger.debug("PrintJobService initialized with repository: %s", printjob_repository)

    async def get_printjobs(self) -> list[PrintJobModel]:
        """
        Retrieves all print jobs from the repository.
        """
        printjob_logger.debug("Retrieving all print jobs")
        printjobs = await self.printjob_repository.get_printjobs()
        printjob_logger.debug("Retrieved print jobs: %s", printjobs)
        return printjobs

    async def create_print_job(self, job: PrintJobModel) -> PrintJobModel:
        """
        Creates a new print job in the repository.
        """
        printjob_logger.debug("Creating new print job: %s", job)
        created_job = await self.printjob_repository.create_print_job(job)
        printjob_logger.debug("Print job created successfully: %s", created_job)
        return created_job