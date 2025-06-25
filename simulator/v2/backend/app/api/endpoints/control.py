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
    # reset head position.x to 0 when starting
    try:
        printer = await printer_service.get_printer()
        if printer.heads:
            head = printer.heads[0]
            if head.position is None:
                head.position = {"x": 0.0, "y": 0.0, "z": 0.0}
            else:
                head.position["x"] = 0.0
            if hasattr(printer_service.printer_repo, "save_printer"):
                await printer_service.printer_repo.save_printer(printer)
    except Exception as e:
        logger.warning(f"failed to reset head position on start: {e}")
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
                printer = await printer_service.get_printer()
                # increment head position.x from 0 to 355 then loop every second
                if printer.heads:
                    head = printer.heads[0]
                    if head.position is None:
                        head.position = {"x": 0.0, "y": 0.0, "z": 0.0}
                    x_val = head.position.get("x", 0.0) or 0.0
                    x_val = float(x_val)
                    x_val = 0.0 if x_val >= 355.0 else x_val + 1.0
                    head.position["x"] = x_val
                    if hasattr(printer_service.printer_repo, "save_printer"):
                        await printer_service.printer_repo.save_printer(printer)
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

