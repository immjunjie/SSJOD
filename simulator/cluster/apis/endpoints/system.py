from fastapi import APIRouter

router = APIRouter()

@router.get("/system/authentication_mode", tags=["system"])
def get_system_authentication_mode():
    """myDescription"""
    return {"Message": "mySuccessful"}

@router.get("/system/current_user", tags=["system"])
def get_system_current_user():
    """myDescription"""
    return {"Message": "mySuccessful"}

@router.get("/system/host_name", tags=["system"], summary="Get the friendly name of the group host printer which this printer belongs to")
def get_system_host_name():
    """myDescription"""
    return {"Message": "mySuccessful"}

@router.get("/system/host_unique_name", tags=["system"], summary="Get the friendly name of the group host printer which this printer belongs to")
def get_system_host_unique_name():
    """myDescription"""
    return {"Message": "mySuccessful"}

@router.get("/system/lastest_firmware_versions", tags=["system"])
def get_system_lastest_firmware_versions():
    """myDescription"""
    return {"Message": "mySuccessful"}
