# app/domain/models.py
from dataclasses import dataclass

@dataclass
class Printer:
    printer_id: str
    status: str
    temperature: float