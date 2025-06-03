from fastapi import APIRouter, Depends, HTTPException
from simulator.v2.backend.app.api.schemas.materials_schemas import MaterialListResponse
from simulator.v2.backend.app.services.materials_service import MaterialsService
from simulator.v2.backend.app.infrastructure.repositories.materials_repo import MaterialRepository
import logging

material_logger = logging.getLogger(__name__)
router = APIRouter()

material_repository = MaterialRepository()
material_service = MaterialsService(material_repository=material_repository)

def get_material_service():
    return material_service

@router.get("/materials", response_model=MaterialListResponse, tags=["Materials"])
async def list_materials(service: MaterialsService = Depends(get_material_service)):
    """
    Retrieve a list of materials.
    """
    try:
        material_list = await service.list_materials()
        return MaterialListResponse(materials=material_list.materials)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")