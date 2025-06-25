from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from simulator.v2.backend.app.api.swagger_api import SwaggerAPI
import logging
import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Configure basic logging settings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize main FastAPI application with no docs at root
app = FastAPI(docs_url=None, redoc_url=None, debug = True)

try:
    # Initialize SwaggerAPI for endpoints (no docs)
    swagger_api = SwaggerAPI(docs_url=None, redoc_url=None)
    app.mount("/api/v1", swagger_api.app)
    logger.info("SwaggerAPI endpoints mounted successfully at /api/v1")

    # Initialize SwaggerAPI for documentation only
    swagger_docs = SwaggerAPI(docs_url="/", redoc_url="/redoc")
    app.mount("/docs/api", swagger_docs.app)
    logger.info("SwaggerAPI documentation mounted successfully at /docs/api")

except Exception as e:
    logger.error(f"API mounting failed: {e}")
    raise

# Mount frontend UI under /ui
frontend_path = Path(__file__).resolve().parents[2] / "frontend"
if frontend_path.exists():
    app.mount("/ui", StaticFiles(directory=str(frontend_path), html=True), name="ui")
    logger.info(f"Frontend mounted at /ui from {frontend_path}")

@app.get("/", include_in_schema=False)
async def root_redirect():
    """
    Root endpoint that redirects to the API documentation
    """
    redirect_url = "/docs/printer"
    logger.info(f"Root access detected, redirecting to {redirect_url}")
    return RedirectResponse(url=redirect_url)

@app.get("/docs/printer", include_in_schema=False)
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
            <p>Access the API documentation at <a href="/docs/api">/docs/api</a></p>
            <p>Test the API at <a href="/api/v1/printer">/api/v1/printer</a></p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html, status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "simulator.v2.backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )