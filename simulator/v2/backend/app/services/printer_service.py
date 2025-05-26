from simulator.v2.backend.app.domain.models.printer_models import Printer
from simulator.v2.backend.app.infrastructure.repositories.printer_repo import PrinterRepository
import logging

logger = logging.getLogger(__name__)

class PrinterService:
    def __init__(self, printer_repo: PrinterRepository = None):
        self.printer_repo = printer_repo or PrinterRepository()

    async def get_printer(self) -> Printer:
        logger.debug("Fetching printer from repository")
        return await self.printer_repo.get()

    async def set_printer_status(self, status: str) -> None:
        logger.debug(f"Setting printer status to: {status}")
        if status not in ["printing", "idle"]:
            raise ValueError(f"Invalid status: {status}. Must be 'printing' or 'idle'.")
        await self.printer_repo.set_status(status)

    async def get_printer_status(self) -> str:
        logger.debug("Fetching printer status from repository")
        return await self.printer_repo.get_status()

    async def get_serial_number(self) -> str:
        logger.debug("Fetching printer serial number from repository")
        return await self.printer_repo.get_serial_number()