from fastapi import APIRouter
from uuid import uuid4
import socket
from pkg_resources import get_platform
from starlette.testclient import TestClient

router = APIRouter()

def get_hostname():
    return socket.gethostname()

def get_firmware():
    return "8.2.0"

def get_memory():
    return {
        "total": 1053614080,
        "used": 647606272
    }

def get_time():
    return {
        "utc": 1746534976.721057
    }

def get_log():
    return [
        "May 06 10:38:39 mjpg-streamer[566]: serving client: 143.239.72.224",
        "May 06 10:58:52 StardustService[1850]: WebSocket connection opened"
    ]

def get_name():
    return "Ultimaker-2aac63"

def get_country():
    return ""

def get_is_country_locked():
    return False

def get_language():
    return "en"

def get_uptime():
    return 8543798

def get_type():
    return "3D printer"

def get_variant():
    return "Ultimaker S5"

def get_hardware():
    return {
        "revision": 2,
        "typeid": 214476
    }

def get_guid():
    return str(uuid4())

def get_display_message():
    return {}

# --- Combined System Info ---
@router.get("/system", tags=["System"])
async def get_system_status():
    return {
        "country": get_country(),
        "display_message": get_display_message(),
        "firmware": get_firmware(),
        "guid": get_guid(),
        "hardware": get_hardware(),
        "hostname": get_hostname(),
        "is_country_locked": get_is_country_locked(),
        "language": get_language(),
        "log": get_log(),
        "memory": get_memory(),
        "name": get_name(),
        "platform": get_platform(),
        "time": get_time(),
        "type": get_type(),
        "uptime": get_uptime(),
        "variant": get_variant()
    }

# --- Individual Routes (same order) ---
@router.get("/system/country", tags=["System"])
async def system_country():
    return get_country()

@router.get("/system/display_message", tags=["System"])
async def system_display_message():
    return get_display_message()

@router.get("/system/firmware", tags=["System"])
async def system_firmware():
    return get_firmware()

@router.get("/system/guid", tags=["System"])
async def system_guid():
    return get_guid()

@router.get("/system/hardware", tags=["System"])
async def system_hardware():
    return get_hardware()

@router.get("/system/hostname", tags=["System"])
async def system_hostname():
    return get_hostname()

@router.get("/system/is_country_locked", tags=["System"])
async def system_is_country_locked():
    return get_is_country_locked()

@router.get("/system/language", tags=["System"])
async def system_language():
    return get_language()

@router.get("/system/log", tags=["System"])
async def system_log():
    return get_log()

@router.get("/system/memory", tags=["System"])
async def system_memory():
    return get_memory()

@router.get("/system/name", tags=["System"])
async def system_name():
    return get_name()

@router.get("/system/platform", tags=["System"])
async def system_platform():
    return get_platform()

@router.get("/system/time", tags=["System"])
async def system_time():
    return get_time()

@router.get("/system/type", tags=["System"])
async def system_type():
    return get_type()

@router.get("/system/uptime", tags=["System"])
async def system_uptime():
    return get_uptime()

@router.get("/system/variant", tags=["System"])
async def system_variant():
    return get_variant()

# Test the /system route
if __name__ == "__main__":
    from backend.simulator.main import app
    client = TestClient(app)
    response = client.get("/docs/system")
    print(response.status_code)
    print(response.json())