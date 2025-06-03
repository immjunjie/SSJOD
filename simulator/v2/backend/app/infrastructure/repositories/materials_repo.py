from typing import Dict, Any
import logging
from simulator.v2.backend.app.domain.models.materials_models import MaterialList

material_logger = logging.getLogger(__name__)

class MaterialRepository:
    def __init__(self):
        self.data: Dict[str, Any] = {
            "materials": MaterialList(materials=["PLA", "ABS", "PETG", "TPU", "Nylon"])
        }

    async def list_materials(self) -> MaterialList:
        """
        Retrieve all materials.
        """
        material_logger.debug("Retrieving all materials")
        return self.data["materials"]