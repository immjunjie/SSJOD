from fastapi import APIRouter

router = APIRouter()

@router.get("/ambient_temperature", tags=["Ambient_temperature"])
def get_camera():
    return {"Message": "mySuccessful"}
