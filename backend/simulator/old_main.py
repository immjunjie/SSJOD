from fastapi import FastAPI, APIRouter
from fastapi.responses import RedirectResponse
from .routers.cluster import cloud, debug, materials, print_jobs, printers, setting, system
from .routers.swagger import air_manager,ambient_temperature,authentication,camera,history,materials,network,print_job,printer,system

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






# ===================== Cluster API =====================
# cluster_tags_metadata = [
#     {"name": "debug", "description": "Debug tools"},
#     {"name": "print_jobs", "description": "Print job queue"},
#     {"name": "printers", "description": "Printer interfaces"},
#     {"name": "cloud", "description": "OAuth2 flow"},
#     {"name": "setting", "description": "Runtime configuration"},
#     {"name": "system", "description": "System configuration"},
#     {"name": "materials", "description": "Materials interaction"},
# ]
#
# cluster_app = FastAPI(
#     docs_url="/",
#     redoc_url="/redocs",
#     openapi_tags=cluster_tags_metadata,
#     title="Ultimaker - Connect API - Simulator",
#     description="""This API exposes endpoints to interact with the Ultimaker Digital Factory software""",
# )
#
# # route register
# cluster_app.include_router(cloud.route)
# cluster_app.include_router(debug.router)
# cluster_app.include_router(materials.router)
# cluster_app.include_router(print_jobs.router)
# cluster_app.include_router(printers.router)
# cluster_app.include_router(setting.router)
# cluster_app.include_router(system.router)


# ===================== Swagger API =====================
# swagger_tags_metadata = [
#     {"name": "Authentication", "description": "Auth system"},
#     {"name": "Materials", "description": "Known materials"},
#     {"name": "Printer", "description": "Printer state"},
#     {"name": "Network", "description": "Network state"},
#     {"name": "PrintJob", "description": "Current job"},
#     {"name": "System", "description": "Device info"},
#     {"name": "History", "description": "Print history"},
#     {"name": "Camera", "description": "Camera feeds"},
#     {"name": "AirManager", "description": "Air manager"},
#     {"name": "Ambient_temperature", "description": ""},
# ]

# swagger_app = FastAPI(
#     docs_url="/api",
#     redoc_url="/api/redoc",
#     title="Ultimaker API - Swagger - Simulator",
#     openapi_tags=swagger_tags_metadata,
#     description="""REST API for the Ultimaker 3D printer.
#
# Authentication: Any PUT/POST/DELETE api requires authentication before it can be used. Authentication is done with http digest (RFC 2617) without fallback to basic authentication.
#
# To get a valid username/password combination, the following process can/should be followed.
#
# 1) POST /auth/request with 'application' and 'user' as parameters. The application name and user name will be shown to the user on the printer. The reply body will contain a json reply with an 'id' and 'key' part.
#
# 2) Repeatedly GET /auth/check/ until it reports 'authorized' or 'unauthorized'. This will be reported back once the end user selects if the application is allowed to use the API.
#
# 3) [optional] test the authentication, the earlier given 'id' is the username, the 'key' is the password. Use digest authentication on GET /auth/verify to test this."""
# )

# route register
# swagger_app.include_router(air_manager.router)
# swagger_app.include_router(ambient_temperature.router)
# swagger_app.include_router(authentication.route)
# swagger_app.include_router(camera.router)
# swagger_app.include_router(history.router)
# swagger_app.include_router(materials.router)
# swagger_app.include_router(network.router)
# swagger_app.include_router(print_job.router)
# swagger_app.include_router(printer.router)
# swagger_app.include_router(system.router)


# ===================== Main app =====================
# app = FastAPI(docs_url=None)

# !!mount order matters!!
# app.mount("/docs", swagger_app)
# app.mount("/cluster-api/v1", cluster_app)

# @app.get("/")
# def root_redirect():
#     return RedirectResponse(url="/docs/api")