from fastapi import FastAPI
from simulator.v2.backend.app.api.endpoints import printer
import logging

logger = logging.getLogger(__name__)


class SwaggerAPI:
    """Swagger API Implementation for Ultimaker Printer Simulator v2"""

    def __init__(self, docs_url=None, redoc_url=None, prefix_paths=True):
        self.tags_metadata = [
            {"name": "Printer", "description": "Printer state and operations"},
        ]
        self.app = FastAPI(
            title="Ultimaker API - Swagger - Simulator v2",
            description="""REST API for the Ultimaker 3D printer simulator (v2).
            This API simulates the behavior of an Ultimaker printer, providing endpoints to manage printer state, status, and other functionalities.""",
            openapi_tags=self.tags_metadata,
            docs_url=docs_url,
            redoc_url=redoc_url
        )
        self.prefix_paths = prefix_paths
        self.register_routers()

        # Customize OpenAPI schema if prefix_paths is True
        if self.prefix_paths:
            original_openapi = self.app.openapi()
            modified_openapi = {
                **original_openapi,
                "paths": {
                    f"/api/v1{path}": details for path, details in original_openapi["paths"].items()
                }
            }
            self.app.openapi = lambda: modified_openapi

        logger.info(f"SwaggerAPI initialized with routes: {[route.path for route in self.app.routes]}")

    def register_routers(self):
        """Register all endpoint routers for the SwaggerAPI"""
        logger.info("Registering routers for SwaggerAPI")
        self.app.include_router(printer.router)
        logger.info("All routers registered")