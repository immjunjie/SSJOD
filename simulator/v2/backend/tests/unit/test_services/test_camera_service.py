import pytest
from simulator.v2.backend.app.domain.models.camera_models import CameraModel
from simulator.v2.backend.app.infrastructure.repositories.camera_repo import CameraRepository
from simulator.v2.backend.app.services.camera_service import CameraService

@pytest.mark.asyncio
async def test_camera_service():
    # Arrange
    camera_service = CameraService(CameraRepository())

    # Act
    result = await camera_service.get_camera_feed()

    # Assert
    assert isinstance(result, CameraModel)