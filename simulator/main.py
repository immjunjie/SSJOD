from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.responses import HTMLResponse

from simulator.cluster.apis.cluster_api import ClusterAPI
from simulator.swagger.apis.swagger_api import SwaggerAPI
import logging
import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))


# ========================================================
# How to Run this?
# --------------------------------------------------------
'''UltiMaker Printer - Official Cura API URLs of WGB'''
# http://143.239.73.224/docs/api/
# http://143.239.73.224/cluster-api/v1/
# --------------------------------------------------------
'''method1 - docker'''
# 1. download docker and install it into the documents/applications directory
# 2. run the docker application at the background
# 3. docker build -t simulator .
# 4. docker run -p 8000:8000 simulator uvicorn backend.simulator.main:app --host 0.0.0.0 --port 8000
# 5. visit 'http://localhost:8000/docs/api'
# 6. visit 'http://localhost:8000/cluster-api/v1/'
# --------------------------------------------------------
# Optional (with the local machine ip addresses)
# 4. ifconfig | grep "inet " | grep -v 127.0.0.1
# 5. docker run -p <ip address>:8000:8000 simulator
#    docker run -p 10.241.186.77:8000:8000 simulator
# 6. visit 'http://10.241.186.77:8000/docs/api'
# 7. visit 'http://10.241.186.77:8000/cluster-api/v1/'
# --------------------------------------------------------
'''method2 - pipenv'''
# 1. pip install pipenv
# or "pip3 install pipenv"
# 2. python3 -m site --user-base
# 3. which pipenv
# 4. export PATH="$HOME/Library/Python/3.11/bin:$PATH"
# 5. pipenv --version
# 6. pipenv install
# 7. pipenv run uvicorn backend.simulator.main:app --reload
# --------------------------------------------------------
# Optional (config the shell with path export)
# echo 'export PATH="$HOME/Library/Python/3.11/bin:$PATH"' >> ~/.zshrc
# source ~/.zshrc
# --------------------------------------------------------
# If needed:
# export LANG=en_US.UTF-8
# --------------------------------------------------------


# Configure basic logging settings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize main FastAPI application with docs disabled at root
app = FastAPI(docs_url=None, redoc_url=None)

try:
    # Initialize and mount Cluster API
    cluster_api = ClusterAPI()
    app.mount("/cluster-api/v1", cluster_api.app)
    logger.info("ClusterAPI mounted successfully at /cluster-api/v1")

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
            <h1>Welcome to the Ultimaker Printer Simulator</h1>
            <p>This simulator mimics the behavior of an Ultimaker printer.</p>
            <p>You can access the API documentation at <a href="/docs/api">/docs/api</a></p>
            <p>For more information, visit the <a href="/cluster-api/v1">Cluster API</a>.</p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html, status_code=200)



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "simulator.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )