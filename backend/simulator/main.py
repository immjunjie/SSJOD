from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from backend.simulator.cluster.apis.cluster_api import ClusterAPI
from backend.simulator.swagger.apis.swagger_api import SwaggerAPI
import logging
import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.append(str(Path(__file__).parent))

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