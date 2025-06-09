import pytest
from simulator.v2.backend.app.domain.models.printjob_models import PrintJobModel
from simulator.v2.backend.app.infrastructure.repositories.printjob_repo import PrintJobRepo
from simulator.v2.backend.app.services.printjob_service import PrintJobService

@pytest.mark.asyncio
async def test_get_printjobs_returns_list_of_printjob_models():
    """
    Test that the PrintJobService's get_printjobs method returns a list of PrintJobModel objects
    """

    # Arrange
    printjob_service = PrintJobService(PrintJobRepo())

    # Act
    result = await printjob_service.get_printjobs()

    # Assert
    assert isinstance(result, list)
    if result:
        assert isinstance(result[0], PrintJobModel)


@pytest.mark.asyncio
async def test_create_print_job_creates_and_returns_printjob_model():
    """
    Test that the PrintJobService's create_print_job method creates and returns a PrintJobModel object
    """

    # Arrange
    printjob_service = PrintJobService(PrintJobRepo())
    new_job = PrintJobModel(
        time_elapsed=0,
        time_total=100,
        uuid="123e4567-e89b-12d3-a456-426614174000",
        name="Test Print Job"
    )

    # Act
    created_job = await printjob_service.create_print_job(new_job)

    # Assert
    assert isinstance(created_job, PrintJobModel)
    assert created_job.uuid == new_job.uuid
    assert created_job.name == new_job.name
