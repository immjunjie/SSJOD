from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from simulator.v2.backend.app.services.printer_service import PrinterService
import asyncio
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

_printer_service = PrinterService()
_printing_flag = False
_broadcaster_task = None


async def get_printer_service():
    return _printer_service


@router.get("/control/status", tags=["Printer"])
async def get_status():
    return {"printing": _printing_flag}


@router.post("/control/start", tags=["Printer"])
async def start(printer_service: PrinterService = Depends(get_printer_service)):
    global _printing_flag, _broadcaster_task
    if _printing_flag:
        return {"ok": True, "printing": True}
    _printing_flag = True
    await printer_service.set_printer_status("printing")
    if _broadcaster_task is None or _broadcaster_task.done():
        _broadcaster_task = asyncio.create_task(_background_tick(printer_service))
    return {"ok": True, "printing": True}


@router.post("/control/stop", tags=["Printer"])
async def stop(printer_service: PrinterService = Depends(get_printer_service)):
    global _printing_flag
    _printing_flag = False
    await printer_service.set_printer_status("idle")
    return {"ok": True, "printing": False}


async def _background_tick(printer_service: PrinterService):
    try:
        while _printing_flag:
            # Touch the service to evolve temperature and persist if enabled
            try:
                await printer_service.get_printer()
            except Exception as e:
                logger.warning(f"tick failed: {e}")
            await asyncio.sleep(1.0)
    except Exception as e:
        logger.error(f"background tick error: {e}")


@router.websocket("/ws/printer")
async def ws_printer(ws: WebSocket, printer_service: PrinterService = Depends(get_printer_service)):
    await ws.accept()
    try:
        while True:
            # push current snapshot periodically
            try:
                printer = await printer_service.get_printer()
                await ws.send_json(printer.model_dump())
            except Exception as e:
                await ws.send_json({"error": str(e)})
            await asyncio.sleep(1.0)
    except WebSocketDisconnect:
        logger.info("WS disconnected")
    except Exception as e:
        logger.error(f"WS error: {e}")

