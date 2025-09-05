from simulator.v2.backend.app.domain.models.printer_models import Printer
from simulator.v2.backend.app.infrastructure.repositories.printer_repo import PrinterRepository
from simulator.v2.backend.app.infrastructure.simulators.print_head_sim import PrintHeadSimulator
import logging
import os

try:
	from simulator.v2.backend.app.infrastructure.repositories.mongo_printer_repo import MongoPrinterRepository
except Exception:
	MongoPrinterRepository = None  # optional

logger = logging.getLogger(__name__)


class PrinterService:
	def __init__(self, printer_repo: PrinterRepository = None, print_head_simulator: PrintHeadSimulator = None):
		repo_choice = (os.getenv("SIM_REPO") or "memory").lower()
		if printer_repo is not None:
			self.printer_repo = printer_repo
		elif repo_choice == "mongo" and MongoPrinterRepository is not None:
			self.printer_repo = MongoPrinterRepository()
		else:
			self.printer_repo = PrinterRepository()
		self.print_head_simulator = print_head_simulator or PrintHeadSimulator()

	async def get_printer(self) -> Printer:
		logger.debug("Fetching printer from repository")
		printer = await self.printer_repo.get()

		# Update the printer's head temperature using the simulator
		head_temperature = await self.print_head_simulator.get_temperature()
		logger.debug(f"Updating printer head temperature to: {head_temperature}")

		# Assuming the printer has at least one head and one extruder
		if printer.heads and printer.heads[0].extruders:
			printer.heads[0].extruders[0].hotend.temperature.current = head_temperature

		# Persist latest state if repo supports it
		if hasattr(self.printer_repo, "save_printer"):
			try:
				await self.printer_repo.save_printer(printer)
			except Exception as e:
				logger.warning(f"Failed to persist printer state: {e}")
		return printer

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