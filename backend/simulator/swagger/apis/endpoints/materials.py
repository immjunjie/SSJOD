from fastapi import APIRouter

router = APIRouter()

@router.get("/materials", tags=["Materials"])
def get_materials():
    """myDescription"""
    return {"Message": "mySuccessful"}

@router.get("/materials/{materials_guid}", tags=["Materials"])
def get_materials_by_materials_guid():
    """myDescription"""
    return {"Message": "mySuccessful"}
