import pytest
from simulator.v2.backend.app.infrastructure.repositories.materials_repo import MaterialsRepository
from simulator.v2.backend.app.domain.models.materials_models import MaterialsModels

@pytest.mark.asyncio
async def test_get_materials() -> None:
    repo = MaterialsRepository()
    result = await repo.get_materials()
    assert isinstance(result, MaterialsModels)
    assert result is not None