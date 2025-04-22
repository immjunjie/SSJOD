from fastapi import APIRouter

router = APIRouter()

@router.get("/air_manager", tags=["AirManager"])
def get_camera():
    return {"Message": "mySuccessful"}