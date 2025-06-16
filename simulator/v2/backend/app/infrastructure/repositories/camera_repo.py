from simulator.v2.backend.app.domain.models.camera_models import CameraModel
import logging

camara_logger = logging.getLogger(__name__)

class CameraRepository:
    """
    Repository for the camera feed.
    """
    def __init__(self) -> None:
        self.camera_feed: CameraModel = CameraModel(
            feed="http://example:8080/video_feed"
        )

    async def get_camera_feed(self) -> CameraModel:
        """
        Get the camera feed.
        """
        camara_logger.info("Getting camera feed")
        return self.camera_feed