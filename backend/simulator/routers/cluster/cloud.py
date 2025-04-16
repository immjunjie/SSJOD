from fastapi import APIRouter

router = APIRouter()

@router.get("/cloud/authentication.py", tags=["cloud"])
def get_cloud_authentication():
    """myDescription"""
    return {"Message": "mySuccessful"}

@router.get("/cloud/cloud_connect_flow", tags=["cloud"])
def get_cloud_cloud_connect_flow():
    """myDescription"""
    return {"Message": "mySuccessful"}

@router.get("/cloud/redirect", tags=["cloud"])
def get_cloud_redirect():
    """myDescription"""
    return {"Message": "mySuccessful"}