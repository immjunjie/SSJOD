from typing import Any, Dict, Optional
import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from simulator.v2.backend.app.domain.models.printer_models import Printer

logger = logging.getLogger(__name__)


class MongoPrinterRepository:
	def __init__(self,
				mongo_uri: Optional[str] = None,
				database_name: Optional[str] = None,
				collection_name: Optional[str] = None) -> None:
		self.mongo_uri = mongo_uri or os.getenv("SIM_MONGO_URI", "mongodb://localhost:27017")
		db_name = database_name or os.getenv("SIM_MONGO_DB", "simulator_v2")
		coll_name = collection_name or os.getenv("SIM_MONGO_COLL", "printer_state")
		self.client = AsyncIOMotorClient(self.mongo_uri)
		self.db = self.client[db_name]
		self.collection = self.db[coll_name]
		self._id = "singleton"

	async def get(self) -> Printer:
		logger.debug("Mongo get printer state")
		doc: Optional[Dict[str, Any]] = await self.collection.find_one({"_id": self._id})
		if not doc:
			logger.info("No state found in Mongo, initializing default")
			printer = Printer(heads=[], diagnostics={}, validate_header={})
			await self._save_printer(printer)
			return printer
		# remove _id for model parsing safety
		doc.pop("_id", None)
		return Printer(**doc)

	async def set_status(self, status: str) -> None:
		await self.collection.update_one({"_id": self._id}, {"$set": {"status": status}}, upsert=True)

	async def get_status(self) -> str:
		doc = await self.collection.find_one({"_id": self._id}, {"status": 1})
		return (doc or {}).get("status", "idle")

	async def get_serial_number(self) -> str:
		doc = await self.collection.find_one({"_id": self._id}, {"serial_number": 1})
		return (doc or {}).get("serial_number", "SIM-000000")

	async def save_printer(self, printer: Printer) -> None:
		await self._save_printer(printer)

	async def _save_printer(self, printer: Printer) -> None:
		payload = printer.model_dump(by_alias=True)
		payload["_id"] = self._id
		await self.collection.replace_one({"_id": self._id}, payload, upsert=True)
