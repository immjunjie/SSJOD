from fastapi import APIRouter, Depends
from starlette.testclient import TestClient
from backend.simulator.swagger.services.printer_service import PrinterService

router = APIRouter()

def get_printer_service():
    return PrinterService()

@router.get("/printer", tags=["Printer"])
def get_printer(service: PrinterService = Depends(get_printer_service)):
    return service.get_printer_info()

@router.get("/printer/status", tags=["Printer"])
def get_printer_status(service: PrinterService = Depends(get_printer_service)):
    return service.get_printer_status()

@router.get("/printer/bed", tags=["Printer"])
def get_printer_bed(service: PrinterService = Depends(get_printer_service)):
    return service.get_bed_status()

@router.get("/printer/bed/temperature", tags=["Printer"])
def get_printer_bed_temperature(service: PrinterService = Depends(get_printer_service)):
    bed_status = service.get_bed_status()
    return bed_status.get("temperature", {})

@router.get("/printer/heads", tags=["Printer"])
def get_printer_heads(service: PrinterService = Depends(get_printer_service)):
    return service.get_head_statuses()

@router.get("/printer/led", tags=["Printer"])
def get_printer_led(service: PrinterService = Depends(get_printer_service)):
    return service.get_led_status()

@router.get("/printer/network_status", tags=["Printer"])
def get_printer_network_status(service: PrinterService = Depends(get_printer_service)):
    return service.get_network_status()

@router.get("/printer/serial_number", tags=["Printer"])
def get_printer_serial_number(service: PrinterService = Depends(get_printer_service)):
    return service.get_serial_number()


# ----------------------- Manual Integration Test -----------------------
def run_manual_integration_tests():
    from backend.simulator.main import app
    client = TestClient(app)

    endpoints = [
        "printer",
        "printer/status",
        "printer/bed",
        "printer/bed/temperature",
        "printer/heads",
        "printer/led",
        "printer/network_status",
        "printer/serial_number"
    ]

    for ep in endpoints:
        print(f"\n --- Test: /{ep} ---")
        try:
            response = client.get(f"/api/v1/{ep}")
            print(f"Code: {response.status_code}, Response: {response.json()}")
        except Exception as e:
            print(f"Error testing /api/v1/{ep}: {e}")

if __name__ == "__main__":
    run_manual_integration_tests()