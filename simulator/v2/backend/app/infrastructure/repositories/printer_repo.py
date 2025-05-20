# simulator.v2.backend.app/infrastructure/repositories/printer_repo.py
from simulator.v2.backend.app.domain.models import Printer

class InMemoryPrinterRepository:
    def __init__(self):
        self._printers = {
            "printer_1": Printer(printer_id="printer_1", status="idle", temperature=20.0)
        }

    async def get(self, printer_id: str) -> Printer:
        printer = self._printers.get(printer_id)
        if not printer:
            raise ValueError(f"Printer {printer_id} not found")
        return printer