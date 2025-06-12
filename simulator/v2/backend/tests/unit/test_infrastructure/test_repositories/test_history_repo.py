import pytest
from simulator.v2.backend.app.infrastructure.repositories.history_repo import HistoryRepo
from simulator.v2.backend.app.domain.models.history_models import HistoryModel, HistoriesModel

@pytest.mark.asyncio
async def test_get_history():

    repo = HistoryRepo()
    result = await repo.get_histories()
    assert isinstance(result, HistoriesModel)