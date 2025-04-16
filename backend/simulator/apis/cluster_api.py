from .base_api import BaseAPI
from ..routers.cluster import (
    cloud, debug, materials,
    print_jobs, printers, setting, system
)

class ClusterAPI(BaseAPI):
    """Cluster API Implementation"""
    def __init__(self):
        self.tags_metadata = [
            {"name": "debug", "description": "Endpoint for interaction with the print job queue"},
            {"name": "print_jobs", "description": "Endpoint for interaction with the print job queue or with specific jobs in it."},
            {"name": "printers", "description": "Endpoint for interaction with the printers"},
            {"name": "cloud", "description": "Endpoint for part of the Cloud/OAuth2 authentication process"},
            {"name": "setting", "description": "Endpoint for at runtime configuration"},
            {"name": "system", "description": "System configuration"},
            {"name": "materials", "description": "Endpoint for interaction with the materials"},
        ]
        super().__init__(
            docs_url="/",
            redoc_url="/redocs",
            title="Ultimaker - Connect API - Simulator",
            openapi_tags=self.tags_metadata,
            description="""This API exposes endpoints to interact with the Ultimaker Digital Factory software""",
        )
        self.register_routers()

    def register_routers(self):
        self.app.include_router(cloud.router)
        self.app.include_router(debug.router)
        self.app.include_router(materials.router)
        self.app.include_router(print_jobs.router)
        self.app.include_router(printers.router)
        self.app.include_router(setting.router)
        self.app.include_router(system.router)