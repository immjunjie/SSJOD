from fastapi import APIRouter

route = APIRouter()

@route.get("/auth/check/{id}", tags=["Authentication"])
def get_auth_check_by_id():
    """myDescription"""
    return {"Message": "mySuccessful"}

@route.get("/auth/verify", tags=["Authentication"])
def get_auth_verify():
    """myDescription"""
    return {"Message": "mySuccessful"}