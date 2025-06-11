import pytest
from simulator.v2.backend.app.domain.models.materials_models import MaterialsModel
from simulator.v2.backend.app.infrastructure.repositories.materials_repo import MaterialRepository
from simulator.v2.backend.app.services.materials_service import MaterialsService

@pytest.mark.asyncio
async def test_list_materials_returns_material_list():
    """
    Test that the MaterialsService's list_materials method returns a MaterialList object
    """

    # Arrange
    materials_service = MaterialsService(MaterialRepository())

    # Act
    result = await materials_service.get_materials()

    # Assert
    assert isinstance(result, MaterialsModel)
    assert result.materials is not None