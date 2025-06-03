import pytest
from unittest.mock import AsyncMock

from simulator.v2.backend.app.services.printer_service import PrinterService
from simulator.v2.backend.app.domain.models.printer_models import Printer
from simulator.v2.backend.app.infrastructure.repositories.printer_repo import PrinterRepository
from simulator.v2.backend.app.infrastructure.simulators.print_head_sim import PrintHeadSimulator


@pytest.mark.asyncio
async def test_get_printer_updates_temperature():
    from simulator.v2.backend.app.infrastructure.repositories.printer_repo import PrinterRepository
    # Arrange
    mock_repo = AsyncMock(spec=PrinterRepository)
    mock_simulator = AsyncMock(spec=PrintHeadSimulator)

    # Suppose the warehouse returns a printer object (the real class can be reused directly)
    from simulator.v2.backend.app.infrastructure.repositories.printer_repo import PrinterRepository
    real_repo = PrinterRepository()
    mock_repo.get.return_value = await real_repo.get()

    mock_simulator.get_temperature.return_value = 99.9

    service = PrinterService(printer_repo=mock_repo, print_head_simulator=mock_simulator)

    # Act
    printer = await service.get_printer()

    # Assert
    assert isinstance(printer, Printer)
    assert printer.heads[0].extruders[0].hotend.temperature.current == 99.9


@pytest.mark.asyncio
async def test_set_printer_status_valid():
    mock_repo = AsyncMock(spec=PrinterRepository)
    service = PrinterService(printer_repo=mock_repo)

    await service.set_printer_status("printing")
    mock_repo.set_status.assert_called_with("printing")


@pytest.mark.asyncio
async def test_set_printer_status_invalid():
    mock_repo = AsyncMock(spec=PrinterRepository)
    service = PrinterService(printer_repo=mock_repo)

    with pytest.raises(ValueError, match="Invalid status"):
        await service.set_printer_status("paused")


@pytest.mark.asyncio
async def test_get_printer_status():
    mock_repo = AsyncMock(spec=PrinterRepository)
    mock_repo.get_status.return_value = "idle"

    service = PrinterService(printer_repo=mock_repo)

    result = await service.get_printer_status()
    assert result == "idle"


@pytest.mark.asyncio
async def test_get_serial_number():
    mock_repo = AsyncMock(spec=PrinterRepository)
    mock_repo.get_serial_number.return_value = "ULTIMAKER-123456"

    service = PrinterService(printer_repo=mock_repo)

    result = await service.get_serial_number()
    assert isinstance(result, str)