from fastapi import APIRouter

router = APIRouter()

@router.get("/system", tags=["System"])
def get_system():
    return {"Message": "mySuccessful"}

@router.get("/system/platform", tags=["System"])
def get_system_platform():
    return {"Message": "mySuccessful"}
