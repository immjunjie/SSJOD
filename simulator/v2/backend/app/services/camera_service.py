from simulator.v2.backend.app.domain.models.camera_models import CameraModel
from simulator.v2.backend.app.infrastructure.repositories.camera_repo import CameraRepository
import logging

camera_logger = logging.getLogger(__name__)

class CameraService:
    """
    Service to get camera information.
    """
    def __init__(self, camera_repository: CameraRepository):
        """
        Initializes the CameraService with a camera repository.
        """
        self.camera_repository = camera_repository
        camera_logger.debug("CameraService initialized with repository: %s", camera_repository)

    async def get_camera_feed(self) -> CameraModel:
        """
        Retrieves the camera feed information.
        """
        camera_logger.debug("Retrieving camera feed information")
        camera_feed = await self.camera_repository.get_camera_feed()
        camera_logger.debug("Retrieved camera feed information: %s", camera_feed)
        return camera_feed