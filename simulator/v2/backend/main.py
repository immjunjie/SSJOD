from fastapi import FastAPI
from starlette.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from simulator.v2.backend.app.api.v1.endpoints import printer
import logging
import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Configure basic logging settings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Ultimaker Printer Simulator", docs_url="/docs/api", redoc_url=None)

try:
    # Mount API endpoints with /api/v1 prefix
    app.include_router(printer.router, prefix="/api/v1")
    logger.info(f"API endpoints mounted successfully at /api/v1: {[route.path for route in app.routes if '/api/v1' in route.path]}")

except Exception as e:
    logger.error(f"API mounting failed: {e}")
    raise

@app.get("/")
async def root_redirect():
    """
    Root endpoint that redirects to the API documentation
    """
    redirect_url = "/docs/printer"
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