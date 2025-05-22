from fastapi import FastAPI
from simulator.v2.backend.app.api.endpoints import printer

app = FastAPI(title="Printer Simulator API")
app.include_router(printer.router, prefix="/api/v1")