from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.responses import HTMLResponse

from simulator.backend.app.api.v1.swagger_api import SwaggerAPI
import logging
import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))


# Configure basic logging settings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize main FastAPI application with docs disabled at root
app = FastAPI(docs_url=None, redoc_url=None)

try:
    # Initialize Swagger API for endpoints (without docs)
    swagger_api = SwaggerAPI(docs_url=None, redoc_url=None)
    # Log registered routes for debugging
    logger.info(f"SwaggerAPI routes: {[route.path for route in swagger_api.app.routes]}")
    app.mount("/api/v1", swagger_api.app)
    logger.info("SwaggerAPI endpoints mounted successfully at /api/v1")

    # Initialize Swagger API for documentation only
    swagger_docs = FastAPI(
        title="Ultimaker API - Swagger - Simulator",
        description=swagger_api.app.description,
        openapi_tags=swagger_api.app.openapi_tags,
        docs_url="/",
        redoc_url="/redoc"
    )
    # Customize OpenAPI schema to include /api/v1/ prefix
    original_openapi = swagger_api.app.openapi()
    modified_openapi = {
        **original_openapi,
        "paths": {
            f"/api/v1{path}": details for path, details in original_openapi["paths"].items()
        }
    }
    swagger_docs.openapi = lambda: modified_openapi  # Set custom OpenAPI schema
    app.mount("/docs/api", swagger_docs)
    logger.info("SwaggerAPI documentation mounted successfully at /docs/api")

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
    redirect_url = "/docs/printer"  # Redirect to documentation path
    logger.info(f"Root access detected, redirecting to {redirect_url}")
    return RedirectResponse(url=redirect_url)

@app.get("/docs/printer")
async def printer_docs():
    """
    Welcome page for the Ultimaker Printer Simulator
    """
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ultimaker Printer Simulator</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                color: #333;
                margin: 0;
                padding: 20px;
            }
            h1 {
                color: #007BFF;
            }
            p {
                font-size: 18px;
            }
            a {
                color: #007BFF;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            .container {
                max-width: 800px;
                margin: auto;
                background: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to the Ultimaker Printer Simulator_v2</h1>
            <p>This simulator mimics the behavior of an Ultimaker printer.</p>
            <p>You can access the API documentation at <a href="/docs/api">/docs/api</a></p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html, status_code=200)



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "simulator.backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )