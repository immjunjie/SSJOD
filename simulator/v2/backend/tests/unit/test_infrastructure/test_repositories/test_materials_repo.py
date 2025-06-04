import pytest
from simulator.v2.backend.app.infrastructure.repositories.materials_repo import MaterialRepository
from simulator.v2.backend.app.domain.models.materials_models import MaterialList

@pytest.mark.asyncio
async def test_get_materials() -> None:
    repo = MaterialRepository()
    result = await repo.list_materials()
    assert isinstance(result, MaterialList)
    assert result is not None