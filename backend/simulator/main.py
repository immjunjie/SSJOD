from fastapi import FastAPI, APIRouter
from fastapi.responses import RedirectResponse
from .routers.cluster import cloud, debug, materials, print_jobs, printers, setting, system
from .routers.swagger import air_manager,ambient_temperature,authentication,camera,history,materials,network,print_job,printer,system

# ========================================================
# How to Run this?
# --------------------------------------------------------
# pip install pipenv
# pipenv install
# pipenv run uvicorn backend.simulator.main:app --reload
# --------------------------------------------------------

# ===================== Cluster API =====================
cluster_tags_metadata = [
    {"name": "debug", "description": "Debug tools"},
    {"name": "print_jobs", "description": "Print job queue"},
    {"name": "printers", "description": "Printer interfaces"},
    {"name": "cloud", "description": "OAuth2 flow"},
    {"name": "setting", "description": "Runtime configuration"},
    {"name": "system", "description": "System configuration"},
    {"name": "materials", "description": "Materials interaction"},
]

cluster_app = FastAPI(
    docs_url="/docs",
    redoc_url=None,
    title="Ultimaker - Connect API - Simulator",
    openapi_tags=cluster_tags_metadata
)

# route register
cluster_app.include_router(cloud.route)
cluster_app.include_router(debug.router)
cluster_app.include_router(materials.router)
cluster_app.include_router(print_jobs.router)
cluster_app.include_router(printers.router)
cluster_app.include_router(setting.router)
cluster_app.include_router(system.router)


# ===================== Swagger API =====================
swagger_tags_metadata = [
    {"name": "Authentication", "description": "Auth system"},
    {"name": "Materials", "description": "Known materials"},
    {"name": "Printer", "description": "Printer state"},
    {"name": "Network", "description": "Network state"},
    {"name": "PrintJob", "description": "Current job"},
    {"name": "System", "description": "Device info"},
    {"name": "History", "description": "Print history"},
    {"name": "Camera", "description": "Camera feeds"},
    {"name": "AirManager", "description": "Air manager"},
    {"name": "Ambient_temperature", "description": ""},
]

swagger_app = FastAPI(
    docs_url="/api",
    redoc_url=None,
    title="Ultimaker API - Swagger - Simulator",
    openapi_tags=swagger_tags_metadata
)
# route register
swagger_app.include_router(air_manager.router)
swagger_app.include_router(ambient_temperature.router)
swagger_app.include_router(authentication.route)
swagger_app.include_router(camera.router)
swagger_app.include_router(history.router)
swagger_app.include_router(materials.router)
swagger_app.include_router(network.router)
swagger_app.include_router(print_job.router)
swagger_app.include_router(printer.router)
swagger_app.include_router(system.router)


# ===================== Main app =====================
app = FastAPI(docs_url=None)

# !!mount order matters!!
app.mount("/docs", swagger_app)
app.mount("/cluster-api/v1", cluster_app)

@app.get("/")
def root_redirect():
    return RedirectResponse(url="/docs/api")