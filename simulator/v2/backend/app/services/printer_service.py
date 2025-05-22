from simulator.v2.backend.app.domain.models import Printer
from simulator.v2.backend.app.infrastructure.repositories.printer_repo import InMemoryPrinterRepository
from simulator.v2.backend.app.infrastructure.simulators.print_head import PrintHeadSimulator

class PrinterService:
    def __init__(self):
        self.repository = InMemoryPrinterRepository()
        self.print_head = PrintHeadSimulator()

    async def get_printer(self) -> Printer:
        printer = await self.repository.get()
        for head in printer.heads:
            for extruder in head.extruders:
                extruder.hotend.temperature.current = await self.print_head.get_temperature()
        return printer