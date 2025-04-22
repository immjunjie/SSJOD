from fastapi import APIRouter

router = APIRouter()

@router.get("/printer/network", tags=["Network"])
def get_printer_network():
    return {"Message": "mySuccessful"}

@router.get("/printer/network/wifi_networks", tags=["Network"])
def get_printer_network_wifi_networks():
    return {"Message": "mySuccessful"}