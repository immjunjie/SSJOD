from fastapi import APIRouter

router = APIRouter()

@router.get("/camera", tags=["Camera"])
def get_camera():
    return {"Message": "mySuccessful"}

@router.get("/camera/feed", tags=["Camera"])
def get_camera_feed():
    return {"Message": "mySuccessful"}

@router.get("/camera/{index}/stream", tags=["Camera"])
def get_camera_steam_by_index():
    return {"Message": "mySuccessful"}

@router.get("/camera/{index}/snapshot", tags=["Camera"])
def get_camera_snapshot_by_index():
    return {"Message": "mySuccessful"}