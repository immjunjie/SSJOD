from fastapi import FastAPI, APIRouter
from fastapi.responses import RedirectResponse

# -----------------------------------------------------------------------------
# How to Run this?
# -----------------------------------------------------------------------------
# Commands:
# pip install pipenv
# pipenv install
# pipenv run uvicorn backend.simulator.api:app --reload
# -----------------------------------------------------------------------------

# =============================================================================
# Cluster API
# =============================================================================
cluster_tags_metadata = [
    {
        "name": "debug",
        "description": "Endpoint for interaction with the print job queue",
    },
    {
        "name": "print_jobs",
        "description": "Endpoint for interaction with the print job queue or with specific jobs in it.",
    },
    {
        "name": "printers",
        "description": "Endpoint for interaction with the printers",
    },
    {
        "name": "cloud",
        "description": "Endpoint for part of the Cloud/OAuth2 authentication.py process",
    },
    {
        "name": "setting",
        "description": "Endpoint for at runtime configuration",
    },
    {
        "name": "system",
        "description": "System configuration",
    },
    {
        "name": "materials",
        "description": " Endpoint for interaction with the materials",
    },
]

# Cluster Application
cluster_app = FastAPI(
    docs_url="/docs",
    redoc_url=None,
    title="Ultimaker - Connect API - Simulator",
    openapi_tags=cluster_tags_metadata
)

# Cluster route definitions
cluster_router = APIRouter()

# Debug endpoints
@cluster_router.get("/debug/match_matrix/{nr}", tags=["debug"], summary="Shows a list of all the last job <-> printer matcher from the scheduler")
def get_debug_match_matrix():
    """myDescription"""
    return {"Message": "mySuccessful"}

@cluster_router.get("/debug/schedule/{nr}", tags=["debug"], summary="Shows a list of all the last job <-> printer matcher from the scheduler")
def get_debug_schedule():
    """myDescription"""
    return {"Message": "mySuccessful"}

# Print jobs endpoints
@cluster_router.get("/print_jobs", tags=["print_jobs"], summary="Return a list of all current print jobs in the queuue")
def get_print_jobs():
    """myDescription"""
    return {"jobs": ["Job1", "Job2"]}

@cluster_router.get("/print_jobs/history/recently_completed", tags=["print_jobs"])
def get_print_jobs_history_recently_completed():
    """myDescription"""
    return {"Message": "mySuccessful"}

@cluster_router.get("/print_jobs/printing", tags=["print_jobs"], summary="Return a list of all started print jobs")
def get_print_jobs_printing():
    """myDescription"""
    return {"Message": "mySuccessful"}

@cluster_router.get("/print_jobs/queued", tags=["print_jobs"], summary="Return a list of all queued print jobs")
def get_print_jobs_queued():
    """myDescription"""
    return {"Message": "mySuccessful"}

# Printers endpoints
@cluster_router.get("/printers", tags=["printers"], summary="Return a list of all the connected printers")
def get_a_list_of_all_the_connected_printers():
    """myDescription"""
    return {"Message": "mySuccessful"}

# Cloud endpoints
@cluster_router.get("/cloud/authentication.py", tags=["cloud"])
def get_cloud_authentication():
    """myDescription"""
    return {"Message": "mySuccessful"}

@cluster_router.get("/cloud/cloud_connect_flow", tags=["cloud"])
def get_cloud_cloud_connect_flow():
    """myDescription"""
    return {"Message": "mySuccessful"}

@cluster_router.get("/cloud/redirect", tags=["cloud"])
def get_cloud_redirect():
    """myDescription"""
    return {"Message": "mySuccessful"}

# Setting endpoints
@cluster_router.get("/setting/{identifier}", tags=["setting"])
def get_setting_identifier():
    """myDescription"""
    return {"Message": "mySuccessful"}

# System endpoints
@cluster_router.get("/system/authentication_mode", tags=["system"])
def get_system_authentication_mode():
    """myDescription"""
    return {"Message": "mySuccessful"}

@cluster_router.get("/system/current_user", tags=["system"])
def get_system_current_user():
    """myDescription"""
    return {"Message": "mySuccessful"}

@cluster_router.get("/system/host_name", tags=["system"], summary="Get the friendly name of the group host printer which this printer belongs to")
def get_system_host_name():
    """myDescription"""
    return {"Message": "mySuccessful"}

@cluster_router.get("/system/host_unique_name", tags=["system"], summary="Get the friendly name of the group host printer which this printer belongs to")
def get_system_host_unique_name():
    """myDescription"""
    return {"Message": "mySuccessful"}

@cluster_router.get("/system/lastest_firmware_versions", tags=["system"])
def get_system_lastest_firmware_versions():
    """myDescription"""
    return {"Message": "mySuccessful"}

# Materials endpoints
@cluster_router.get("/materials", tags=["materials"], summary="Return a list of all the materials")
def get_materials():
    """Description"""
    return {"Message": "mySuccessful"}

# =============================================================================
# Swagger API (Main Application)
# =============================================================================
swagger_tags_metadata = [
    {
        "name": "Default",
        "description": "myDefault for redirection configuration",
    },
    {
        "name": "Authentication",
        "description": "Request and check authorization keys",
    },
    {
        "name": "Materials",
        "description": "All materials known by the printer",
    },
    {
        "name": "Printer",
        "description": "Printer state",
    },
    {
        "name": "Network",
        "description": "Network state",
    },
    {
        "name": "PrintJob",
        "description": "Currently running print",
    },
    {
        "name": "System",
        "description": "Device information",
    },
    {
        "name": "History",
        "description": "History of this printer",
    },
    {
        "name": "Camera",
        "description": "Camera image and video",
    },
    {
        "name": "AirManager",
        "description": "Air-manager peripheral",
    },
    {
        "name": "Ambient_temperature",
        "description": "",
    },
]

# Main Application - Swagger
app = FastAPI(
    docs_url="/docs/api",
    redoc_url=None,
    title="Ultimaker API - Swagger - Simulator",
    openapi_tags=swagger_tags_metadata
)

# Main application route definitions
main_router = APIRouter()

# Root path redirection
@app.get("/", tags=["Default"])
def redirect_to_docs():
    """Redirect to cluster API documentation"""
    return RedirectResponse(url="/cluster-api/v1/docs")

# Authentication endpoints
@main_router.get("/auth/check/{id}", tags=["Authentication"])
def get_auth_check_by_id():
    """myDescription"""
    return {"Message": "mySuccessful"}

@main_router.get("/auth/verify", tags=["Authentication"])
def get_auth_verify():
    """myDescription"""
    return {"Message": "mySuccessful"}

# Materials endpoints
@main_router.get("/materials", tags=["Materials"])
def get_materials():
    """myDescription"""
    return {"Message": "mySuccessful"}

@main_router.get("/materials/{materials_guid}", tags=["Materials"])
def get_materials_by_matirials_guid():
    """myDescription"""
    return {"Message": "mySuccessful"}

# Printer endpoints
@main_router.get("/printer", tags=["Printer"])
def get_printer():
    return {"Message": "mySuccessful"}

@main_router.get("/printer/status", tags=["Printer"])
def get_printer_status():
    return {"Message": "mySuccessful"}

# Network endpoints
@main_router.get("/printer/network", tags=["Network"])
def get_printer_network():
    return {"Message": "mySuccessful"}

@main_router.get("/printer/network/wifi_networks", tags=["Network"])
def get_printer_network_wifi_networks():
    return {"Message": "mySuccessful"}

# PrintJob endpoints
@main_router.get("/print_job", tags=["PrintJob"])
def get_print_job():
    status = True
    if status != True:
        return []
    return {"Message": "mySuccessful"}

# System endpoints
@main_router.get("/system", tags=["System"])
def get_system():
    return {"Message": "mySuccessful"}

@main_router.get("/system/platform", tags=["System"])
def get_system_platform():
    return {"Message": "mySuccessful"}

# History endpoints
@main_router.get("/history/print_jobs", tags=["History"])
def get_history_print_jobs():
    return {"Message": "mySuccessful"}

# Camera endpoints
@main_router.get("/camera", tags=["Camera"])
def get_camera():
    return {"Message": "mySuccessful"}

@main_router.get("/camera/feed", tags=["Camera"])
def get_camera_feed():
    return {"Message": "mySuccessful"}

@main_router.get("/camera/{index}/stream", tags=["Camera"])
def get_camera_steam_by_index():
    return {"Message": "mySuccessful"}

@main_router.get("/camera/{index}/snapshot", tags=["Camera"])
def get_camera_snapshot_by_index():
    return {"Message": "mySuccessful"}

# AirManager endpoints
@main_router.get("/airmanager", tags=["AirManager"])
def get_airmanager():
    return {"Message": "mySuccessful"}

# Ambient temperature endpoints
@main_router.get("/ambient_temperature", tags=["Ambient_temperature"])
def get_ambient_temperature():
    return {"Message": "mySuccessful"}

# =============================================================================
# Application Assembly
# =============================================================================
# Load the cluster routes into cluster app
cluster_app.include_router(cluster_router)

# Mount cluster app under /cluster-api/v1 path
app.mount("/cluster-api/v1", cluster_app)

# Include main router in the main app
app.include_router(main_router)