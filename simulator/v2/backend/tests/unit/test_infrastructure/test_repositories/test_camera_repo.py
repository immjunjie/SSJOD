import pytest
from simulator.v2.backend.app.infrastructure.repositories.camera_repo import CameraRepository
from simulator.v2.backend.app.domain.models.camera_models import CameraModel

@pytest.mark.asyncio
async def test_camera_repo_get_camera():

    repo = CameraRepository()
    result = await repo.get_camera_feed()
    assert isinstance(result, CameraModel)