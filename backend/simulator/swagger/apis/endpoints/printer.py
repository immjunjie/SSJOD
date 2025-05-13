from fastapi import APIRouter, Depends
from starlette.testclient import TestClient
from backend.simulator.swagger.services.printer_service import PrinterService

router = APIRouter()

def get_printer_service():
    return PrinterService()

# ----------------------- Printer Integration -----------------------

@router.get("/printer", tags=["Printer"])
def get_printer(service: PrinterService = Depends(get_printer_service)):
    return service.get_printer_info()

@router.get("/printer/status", tags=["Printer"])
def get_printer_status(service: PrinterService = Depends(get_printer_service)):
    return service.get_printer_status()

# ----------------------- Bed Integration -----------------------

@router.get("/printer/bed", tags=["Printer"])
def get_printer_bed(service: PrinterService = Depends(get_printer_service)):
    info = service.get_printer_info()
    bed_status = info.get("bed", {})
    return bed_status

@router.get("/printer/bed/temperature", tags=["Printer"])
def get_printer_bed_temperature(service: PrinterService = Depends(get_printer_service)):
    bed_status = service.get_bed_status()
    return bed_status.get("temperature", {})

# ----------------------- Head Integration -----------------------

@router.get("/printer/heads", tags=["Printer"])
def get_printer_heads(service: PrinterService = Depends(get_printer_service)):
    heads = service.get_head_statuses()
    return heads

@router.get("/printer/heads/{head_id}", tags=["Printer"])
def get_printer_head_by_id(head_id: int, service: PrinterService = Depends(get_printer_service)):
    heads = service.get_head_statuses()
    for i in range(len(heads)):
        if i == head_id:
            return heads[i]
    return {"error": "Head ID not found"}

@router.get("/printer/heads/{head_id}/position", tags=["Printer"])
def get_printer_head_position_by_id(head_id: int, service: PrinterService = Depends(get_printer_service)):
    heads = service.get_head_statuses()
    for i in range(len(heads)):
        if i == head_id:
            return heads[i].get("position", {})
    return {"error": "Head ID not found"}

@router.get("/printer/heads/{head_id}/extruders", tags=["Printer"])
def get_printer_head_extruders_by_id(head_id: int, service: PrinterService = Depends(get_printer_service)):
    heads = service.get_head_statuses()
    for i in range(len(heads)):
        if i == head_id:
            return heads[i].get("extruders", {})
    return {"error": "Head ID not found"}

@router.get("/printer/heads/{head_id}/extruders/{extruder_id}", tags=["Printer"])
def get_printer_head_extruder_by_id(head_id: int, extruder_id: int, service: PrinterService = Depends(get_printer_service)):
    heads = service.get_head_statuses()
    for i in range(len(heads)):
        if i == head_id:
            extruders = heads[i].get("extruders", [])
            for j in range(len(extruders)):
                if j == extruder_id:
                    return extruders[j]
    return {"error": "Head ID or Extruder ID not found"}

@router.get("/printer/heads/{head_id}/extruders/{extruder_id}/hotend", tags=["Printer"])
def get_printer_head_extruder_hotend(head_id: int, extruder_id: int, service: PrinterService = Depends(get_printer_service)):
    heads = service.get_head_statuses()
    for i in range(len(heads)):
        if i == head_id:
            extruders = heads[i].get("extruders", [])
            for j in range(len(extruders)):
                if j == extruder_id:
                    return extruders[j].get("hotend", {})
    return {"error": "Head ID or Extruder ID not found"}

@router.get("/printer/heads/{head_id}/extruders/{extruder_id}/hotend/temperature", tags=["Printer"])
def get_printer_head_extruder_hotend_temperature(head_id: int, extruder_id: int, service: PrinterService = Depends(get_printer_service)):
    heads = service.get_head_statuses()
    for i in range(len(heads)):
        if i == head_id:
            extruders = heads[i].get("extruders", [])
            for j in range(len(extruders)):
                if j == extruder_id:
                    return extruders[j].get("hotend", {}).get("temperature", {})
    return {"error": "Head ID or Extruder ID not found"}

@router.get("/printer/heads/{head_id}/extruders/{extruder_id}/hotend/temperature/current", tags=["Printer"])
def get_printer_head_extruder_hotend_temperature_current(head_id: int, extruder_id: int, service: PrinterService = Depends(get_printer_service)):
    heads = service.get_head_statuses()
    for i in range(len(heads)):
        if i == head_id:
            extruders = heads[i].get("extruders", [])
            for j in range(len(extruders)):
                if j == extruder_id:
                    return extruders[j].get("hotend", {}).get("temperature", {}).get("current", {})
    return {"error": "Head ID or Extruder ID not found"}

@router.get("/printer/heads/{head_id}/extruders/{extruder_id}/hotend/temperature/target", tags=["Printer"])
def get_printer_head_extruder_hotend_temperature_target(head_id: int, extruder_id: int, service: PrinterService = Depends(get_printer_service)):
    heads = service.get_head_statuses()
    for i in range(len(heads)):
        if i == head_id:
            extruders = heads[i].get("extruders", [])
            for j in range(len(extruders)):
                if j == extruder_id:
                    return extruders[j].get("hotend", {}).get("temperature", {}).get("target", {})
    return {"error": "Head ID or Extruder ID not found"}


@router.get("/printer/heads/{head_id}/extruders/{extruder_id}/hotend/statistics", tags=["Printer"])
def get_printer_head_extruder_hotend_statistics(head_id: int, extruder_id: int, service: PrinterService = Depends(get_printer_service)):
    heads = service.get_head_statuses()
    for i in range(len(heads)):
        if i == head_id:
            extruders = heads[i].get("extruders", [])
            for j in range(len(extruders)):
                if j == extruder_id:
                    return extruders[j].get("hotend", {}).get("statistics", {})
    return {"error": "Head ID or Extruder ID not found"}

@router.get("/printer/heads/{head_id}/extruders/{extruder_id}/hotend/statistics/time_spent_hot", tags=["Printer"])
def get_printer_head_extruder_hotend_statistics_time_spent_hot(head_id: int, extruder_id: int, service: PrinterService = Depends(get_printer_service)):
    heads = service.get_head_statuses()
    for i in range(len(heads)):
        if i == head_id:
            extruders = heads[i].get("extruders", [])
            for j in range(len(extruders)):
                if j == extruder_id:
                    return extruders[j].get("hotend", {}).get("statistics", {}).get("time_spent_hot", {})
    return {"error": "Head ID or Extruder ID not found"}

@router.get("/printer/heads/{head_id}/extruders/{extruder_id}/hotend/statistics/material_extruded", tags=["Printer"])
def get_printer_head_extruder_hotend_statistics_material_extruded(head_id: int, extruder_id: int, service: PrinterService = Depends(get_printer_service)):
    heads = service.get_head_statuses()
    for i in range(len(heads)):
        if i == head_id:
            extruders = heads[i].get("extruders", [])
            for j in range(len(extruders)):
                if j == extruder_id:
                    return extruders[j].get("hotend", {}).get("statistics", {}).get("material_extruded", {})
    return {"error": "Head ID or Extruder ID not found"}

@router.get("/printer/heads/{head_id}/extruders/{extruder_id}/feeder", tags=["Printer"])
def get_printer_head_extruder_feeder(head_id: int, extruder_id: int, service: PrinterService = Depends(get_printer_service)):
    heads = service.get_head_statuses()
    for i in range(len(heads)):
        if i == head_id:
            extruders = heads[i].get("extruders", [])
            for j in range(len(extruders)):
                if j == extruder_id:
                    return extruders[j].get("feeder", {})
    return {"error": "Head ID or Extruder ID not found"}

@router.get("/printer/heads/{head_id}/extruders/{extruder_id}/feeder/max_speed", tags=["Printer"])
def get_printer_head_extruder_feeder_max_speed(head_id: int, extruder_id: int, service: PrinterService = Depends(get_printer_service)):
    heads = service.get_head_statuses()
    for i in range(len(heads)):
        if i == head_id:
            extruders = heads[i].get("extruders", [])
            for j in range(len(extruders)):
                if j == extruder_id:
                    return extruders[j].get("feeder", {}).get("max_speed", {})
    return {"error": "Head ID or Extruder ID not found"}

@router.get("/printer/heads/{head_id}/extruders/{extruder_id}/active_material", tags=["Printer"])
def get_printer_head_extruder_active_material(head_id: int, extruder_id: int, service: PrinterService = Depends(get_printer_service)):
    heads = service.get_head_statuses()
    for i in range(len(heads)):
        if i == head_id:
            extruders = heads[i].get("extruders", [])
            for j in range(len(extruders)):
                if j == extruder_id:
                    return extruders[j].get("active_material", {})
    return {"error": "Head ID or Extruder ID not found"}

@router.get("/printer/heads/{head_id}/extruders/{extruder_id}/active_material/length_remaining", tags=["Printer"])
def get_printer_head_extruder_active_material_length_remaining(head_id: int, extruder_id: int, service: PrinterService = Depends(get_printer_service)):
    heads = service.get_head_statuses()
    for i in range(len(heads)):
        if i == head_id:
            extruders = heads[i].get("extruders", [])
            for j in range(len(extruders)):
                if j == extruder_id:
                    return extruders[j].get("active_material", {}).get("length_remaining", {})
    return {"error": "Head ID or Extruder ID not found"}


# ----------------------- LED Integration -----------------------

@router.get("/printer/led", tags=["Printer"])
def get_printer_led(service: PrinterService = Depends(get_printer_service)):
    info = service.get_printer_info()
    led_status = info.get("led", {})
    return led_status

# ----------------------- Network Integration -----------------------

@router.get("/printer/network_status", tags=["Printer"])
def get_printer_network_status(service: PrinterService = Depends(get_printer_service)):
    return service.get_network_status()

# ----------------------- Serial Number Integration -----------------------

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
        "printer/heads/0",
        "printer/heads/0/position",
        "printer/heads/0/extruders",
        "printer/heads/0/extruders/0",
        "printer/heads/0/extruders/0/hotend",
        "printer/heads/0/extruders/0/hotend/temperature",
        "printer/heads/0/extruders/0/hotend/temperature/current",
        "printer/heads/0/extruders/0/hotend/temperature/target",
        "printer/heads/0/extruders/0/hotend/statistics",
        "printer/heads/0/extruders/0/hotend/statistics/time_spent_hot",
        "printer/heads/0/extruders/0/hotend/statistics/material_extruded",
        "printer/heads/0/extruders/0/feeder",
        "printer/heads/0/extruders/0/feeder/max_speed",
        "printer/heads/0/extruders/0/active_material",
        "printer/heads/0/extruders/0/active_material/length_remaining",
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