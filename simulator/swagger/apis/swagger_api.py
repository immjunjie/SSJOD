from fastapi import APIRouter, FastAPI
from simulator.base.apis.base_api import BaseAPI
from simulator.swagger.apis.endpoints import (
    air_manager, ambient_temperature, camera, network, printer, system, authentication, materials, print_job, history
)
import logging

logger = logging.getLogger(__name__)

class SwaggerAPI(BaseAPI):
    """Swagger API Implementation"""
    def __init__(self, docs_url=None, redoc_url=None):
        self.tags_metadata = [
            {"name": "Authentication", "description": "Request and check authorization keys"},
            {"name": "Materials", "description": "All materials known by the printer"},
            {"name": "Printer", "description": "Printer state"},
            {"name": "Network", "description": "Network state"},
            {"name": "PrintJob", "description": "Currently running print"},
            {"name": "System", "description": "Device information"},
            {"name": "History", "description": "History of this printer"},
            {"name": "Camera", "description": "Camera image and video"},
            {"name": "AirManager", "description": "Air-manager peripheral"},
            {"name": "Ambient_temperature", "description": ""},
        ]
        super().__init__(
            docs_url=docs_url,
            redoc_url=redoc_url,
            title="Ultimaker API - Swagger - Simulator",
            openapi_tags=self.tags_metadata,
            description="""REST API for the Ultimaker 3D printer.

        Authentication: Any PUT/POST/DELETE api requires authentication before it can be used. Authentication is done with http digest (RFC 2617) without fallback to basic authentication.

        To get a valid username/password combination, the following process can/should be followed.

        1) POST /auth/request with 'application' and 'user' as parameters. The application name and user name will be shown to the user on the printer. The reply body will contain a json reply with an 'id' and 'key' part.

        2) Repeatedly GET /auth/check/ until it reports 'authorized' or 'unauthorized'. This will be reported back once the end user selects if the application is allowed to use the API.

        3) [optional] test the authentication, the earlier given 'id' is the username, the 'key' is the password. Use digest authentication on GET /auth/verify to test this."""
        )
        self.register_routers()
        # Log registered routes after initialization
        logger.info(f"SwaggerAPI initialized with routes: {[route.path for route in self.app.routes]}")

    def register_routers(self):
        logger.info("Registering routers for SwaggerAPI")
        self.app.include_router(air_manager.router)
        self.app.include_router(ambient_temperature.router)
        self.app.include_router(authentication.router)
        self.app.include_router(camera.router)
        self.app.include_router(history.router)
        self.app.include_router(materials.router)
        self.app.include_router(network.router)
        self.app.include_router(print_job.router)
        self.app.include_router(printer.router)
        self.app.include_router(system.router)
        logger.info("All routers registered")