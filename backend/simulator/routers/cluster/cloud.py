from fastapi import APIRouter

route = APIRouter()

@route.get("/cloud/authentication.py", tags=["cloud"])
def get_cloud_authentication():
    """myDescription"""
    return {"Message": "mySuccessful"}

@route.get("/cloud/cloud_connect_flow", tags=["cloud"])
def get_cloud_cloud_connect_flow():
    """myDescription"""
    return {"Message": "mySuccessful"}

@route.get("/cloud/redirect", tags=["cloud"])
def get_cloud_redirect():
    """myDescription"""
    return {"Message": "mySuccessful"}