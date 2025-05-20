# simulator.v2.backend.app/api/v1/endpoints/printers.py
from fastapi import APIRouter, Depends, HTTPException
from simulator.v2.backend.app.services.printer_service import PrinterService
from simulator.v2.backend.app.api.v1.schemas import PrinterStatusResponse

router = APIRouter()

async def get_printer_service():
    return PrinterService()

@router.get("/{printer_id}/status", response_model=PrinterStatusResponse)
async def get_printer_status(printer_id: str, printer_service: PrinterService = Depends(get_printer_service)):
    try:
        printer = await printer_service.get_printer_status(printer_id)
        return PrinterStatusResponse(
            printer_id=printer.printer_id,
            status=printer.status,
            temperature=printer.temperature
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))