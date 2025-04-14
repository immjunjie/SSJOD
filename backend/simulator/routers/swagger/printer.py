from fastapi import APIRouter

router = APIRouter()

@router.get("/printer", tags=["Printer"])
def get_printer():
    return {"Message": "mySuccessful"}

@router.get("/printer/status", tags=["Printer"])
def get_printer_status():
    return {"Message": "mySuccessful"}
