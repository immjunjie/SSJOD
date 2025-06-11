from typing import List

from fastapi import APIRouter, Depends, HTTPException
from simulator.v2.backend.app.domain.models.materials_models import MaterialsModel
from simulator.v2.backend.app.services.materials_service import MaterialsService
from simulator.v2.backend.app.infrastructure.repositories.materials_repo import MaterialRepository
import logging

materials_logger = logging.getLogger(__name__)
router = APIRouter()

material_repository = MaterialRepository()
material_service = MaterialsService(material_repository=material_repository)

def get_material_repo():
    """
    Get the MaterialRepository instance.
    """
    materials_logger.debug("Get the MaterialRepository instance.")
    return material_repository

def get_material_service():
    """
    Get the MaterialsService instance.
    """
    return material_service


@router.get("/materials", response_model=List[str], tags=["Materials"])
async def get_materials(service: MaterialsService = Depends(get_material_service)):
    """
    Retrieve a list of materials.
    """
    try:
        materials_logger.debug("Request received to fetch materials.")
        result: MaterialsModel = await service.get_materials()
        materials_logger.debug("Materials fetched successfully: %s", result)
        return result.materials  # 只返回 list
    except Exception as e:
        materials_logger.error("Error fetching materials: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")