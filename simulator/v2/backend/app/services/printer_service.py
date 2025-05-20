# simulator.v2.backend.app/services/printer_service.py
from simulator.v2.backend.app.domain.models import Printer
from simulator.v2.backend.app.infrastructure.repositories.printer_repo import InMemoryPrinterRepository
from simulator.v2.backend.app.infrastructure.simulators.print_head import PrintHeadSimulator


class PrinterService:
    def __init__(self):
        self.repository = InMemoryPrinterRepository()
        self.print_head = PrintHeadSimulator()

    async def get_printer_status(self, printer_id: str) -> Printer:
        printer = await self.repository.get(printer_id)
        printer.temperature = await self.print_head.get_temperature()
        return printer