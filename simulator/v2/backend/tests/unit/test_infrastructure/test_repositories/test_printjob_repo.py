import pytest
from simulator.v2.backend.app.infrastructure.repositories.printjob_repo import PrintJobRepo
from simulator.v2.backend.app.domain.models.printjob_models import PrintJobModel

@pytest.mark.asyncio
async def test_printjobs():

    repo = PrintJobRepo()
    repo.printjobs.append(PrintJobModel(time_elapsed=10, time_total=20, uuid="123e4567-e89b-12d3-a456-426614174000"))

    result = await repo.get_printjobs()

    assert isinstance(repo, PrintJobRepo)
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(item, PrintJobModel) for item in result)