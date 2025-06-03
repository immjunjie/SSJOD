from simulator.v2.backend.app.domain.models.materials_models import MaterialList
from simulator.v2.backend.app.infrastructure.repositories.materials_repo import MaterialRepository
import logging

material_logger = logging.getLogger(__name__)

class MaterialsService:
    """
    Service for handling materials-related operations.
    """
    def __init__(self, material_repository: MaterialRepository):
        self.material_repository = material_repository
        material_logger.debug("MaterialsService initialized with repository: %s", material_repository)

    async def list_materials(self) -> MaterialList:
        """
        Fetches the list of materials from the repository.
        """
        material_logger.debug("Fetching materials from repository.")
        material_list = await self.material_repository.list_materials()
        material_logger.debug("Materials fetched successfully: %s", material_list)
        return material_list