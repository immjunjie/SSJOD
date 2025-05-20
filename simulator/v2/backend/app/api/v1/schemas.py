# simulator.v2.backend.app.api.v1.schemas
from pydantic import BaseModel

class PrinterStatusResponse(BaseModel):
    printer_id: str
    status: str
    temperature: float