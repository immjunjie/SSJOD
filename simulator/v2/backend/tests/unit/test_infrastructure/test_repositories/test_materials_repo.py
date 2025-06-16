import pytest
from simulator.v2.backend.app.infrastructure.repositories.materials_repo import MaterialRepository
from simulator.v2.backend.app.domain.models.materials_models import MaterialsModel

@pytest.mark.asyncio
async def test_get_materials() -> None:
    # Arrange
    repo = MaterialRepository()

    # Act
    result = await repo.get_materials()

    # Assert
    assert isinstance(result, MaterialsModel)
    assert result is not None