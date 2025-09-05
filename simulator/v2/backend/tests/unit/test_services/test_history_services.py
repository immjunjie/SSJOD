import pytest
from simulator.v2.backend.app.domain.models.history_models import HistoryModel, HistoriesModel
from simulator.v2.backend.app.infrastructure.repositories.history_repo import HistoryRepo
from simulator.v2.backend.app.services.history_service import HistoryService

@pytest.mark.asyncio
async def test_get_histories():
    """
    Test the get_histories method of HistoryService.
    """

    # Arrange
    history_repo = HistoryRepo()
    history_service = HistoryService(history_repo)

    # Act
    result = await history_service.get_histories()

    # Assert
    assert isinstance(result, HistoriesModel)