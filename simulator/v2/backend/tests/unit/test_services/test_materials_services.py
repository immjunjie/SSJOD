import pytest
from simulator.v2.backend.app.domain.models.materials_models import MaterialList
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
    result = await materials_service.list_materials()

    # Assert
    assert isinstance(result, MaterialList)
    assert result.materials is not None