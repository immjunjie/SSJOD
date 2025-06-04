import pytest
from simulator.v2.backend.app.infrastructure.repositories.printer_repo import PrinterRepository
from simulator.v2.backend.app.domain.models.printer_models import Printer

@pytest.mark.asyncio
async def test_get_returns_printer():
    repo = PrinterRepository()
    printer = await repo.get()
    assert isinstance(printer, Printer)
    assert printer.status in ["idle", "printing", "paused"]
    assert type(printer.serial_number) == str

@pytest.mark.asyncio
async def test_get_status_returns_initial_status():
    repo = PrinterRepository()
    status = await repo.get_status()
    assert status in ["idle", "printing", "paused"]

@pytest.mark.asyncio
async def test_set_status_updates_status():
    repo = PrinterRepository()
    await repo.set_status("printing")
    status = await repo.get_status()
    assert status in ["printing", "paused"]

@pytest.mark.asyncio
async def test_get_serial_number_returns_expected_value():
    repo = PrinterRepository()
    serial = await repo.get_serial_number()
    assert type(serial) == str