import pytest
from simulator.v2.backend.app.domain.models.materials_models import MaterialsModels
from simulator.v2.backend.app.infrastructure.repositories.materials_repo import MaterialsRepository
from simulator.v2.backend.app.services.materials_service import MaterialsService

@pytest.mark.asyncio
async def test_get_materials_returns_materials_models():
    # Arrange
    materials_service = MaterialsService(MaterialsRepository())

    # Act
    result = await materials_service.get_materials()

    # Assert
    assert isinstance(result, MaterialsModels)
    assert result.materials is not None