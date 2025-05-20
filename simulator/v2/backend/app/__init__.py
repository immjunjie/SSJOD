from fastapi import FastAPI
from simulator.v2.backend.app.api.v1.endpoints import printers

app = FastAPI(title="Printer Simulator API")
app.include_router(printers.router, prefix="/api/v1")