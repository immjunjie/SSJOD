from fastapi import APIRouter

router = APIRouter()

@router.get("/setting/{identifier}", tags=["setting"])
def get_setting_identifier():
    """myDescription"""
    return {"Message": "mySuccessful"}