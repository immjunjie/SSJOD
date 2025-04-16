from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .apis.cluster_api import ClusterAPI
from .apis.swagger_api import SwaggerAPI
import logging

# Configure basic logging settings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize main FastAPI application with docs disabled at root
app = FastAPI(docs_url=None)

try:
    # Initialize and mount Cluster API
    cluster_api = ClusterAPI()
    app.mount("/cluster-api/v1", cluster_api.app)
    logger.info("ClusterAPI mounted successfully at /cluster-api/v1")

    # Initialize and mount Swagger API
    swagger_api = SwaggerAPI()
    app.mount("/docs", swagger_api.app)
    logger.info("SwaggerAPI mounted successfully at /docs")

except Exception as e:
    logger.error(f"API mounting failed: {e}")
    raise


@app.get("/")
async def root_redirect():
    """
    Root endpoint that redirects to the API documentation

    Returns:
        RedirectResponse: HTTP redirect to the Swagger UI documentation
    """
    redirect_url = "/docs/api"  # Default redirect to Swagger UI
    logger.info(f"Root access detected, redirecting to {redirect_url}")
    return RedirectResponse(url=redirect_url)