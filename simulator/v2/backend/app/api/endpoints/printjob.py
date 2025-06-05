from fastapi import APIRouter, Depends, HTTPException
from simulator.v2.backend.app.domain.models.printjob_models import PrintJobModel
from simulator.v2.backend.app.infrastructure.repositories.printjob_repo import PrintJobRepo
from simulator.v2.backend.app.services.printjob_service import PrintJobService
import logging

printjob_logger = logging.getLogger(__name__)
router = APIRouter()


# material_repository = PrintJobRepo()
# material_service = MaterialsService(material_repository=material_repository)

printjob_repository = PrintJobRepo()
printjob_service = PrintJobService(printjob_repository=printjob_repository)

def get_printjob_repo():
    printjob_logger.debug("Get the PrintJobRepo instance.")
    return printjob_repository

def get_printjob_service():
    printjob_logger.debug("Get the PrintJobService instance.")
    return PrintJobService(printjob_repository=get_printjob_repo())

@router.get("/printjob", response_model=list[PrintJobModel], tags=["PrintJob"])
async def get_printjobs(service: PrintJobService = Depends(get_printjob_service)):
    """
    Retrieve all print jobs.

    Returns:
        list[PrintJobModel]: A list of print jobs.

    Raises:
        HTTPException: If an error occurs while fetching the print jobs.
    """
    try:
        printjob_logger.debug("Request received to fetch print jobs.")
        printjobs = await service.get_printjobs()
        printjob_logger.debug("Print jobs fetched successfully: %s", printjobs)
        return printjobs
    except Exception as e:
        printjob_logger.error("Error fetching print jobs: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Create a new print job
@router.post("/printjob", response_model=PrintJobModel, tags=["PrintJob"])
async def create_print_job(
    job: PrintJobModel, service: PrintJobService = Depends(get_printjob_service)
):
    """
    Create a new print job.

    Args:
        job (PrintJobModel): The print job to be created.

    Returns:
        PrintJobModel: The created print job.

    Raises:
        HTTPException: If an error occurs while creating the print job.
    """
    try:
        printjob_logger.debug("Request received to create a new print job: %s", job)
        created_job = await service.create_print_job(job)
        printjob_logger.debug("Print job created successfully: %s", created_job)
        return created_job
    except Exception as e:
        printjob_logger.error("Error creating print job: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")