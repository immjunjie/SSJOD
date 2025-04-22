from fastapi import APIRouter, Depends
from backend.simulator.services.swagger.printer_service import PrinterService

router = APIRouter()

def get_printer_service():
    return PrinterService()

@router.get("/printer", tags=["Printer"])
def get_printer(service: PrinterService = Depends(get_printer_service)):
    return service.gen_basic_info()

@router.get("/printer/status", tags=["Printer"])
def get_printer_status(service: PrinterService = Depends(get_printer_service)):
    return service.get_printer_status()
