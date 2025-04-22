from fastapi import APIRouter

router = APIRouter()

@router.get("/materials", tags=["materials"], summary="Return a list of all the materials")
def get_materials():
    """Description"""
    return {"Message": "mySuccessful"}


