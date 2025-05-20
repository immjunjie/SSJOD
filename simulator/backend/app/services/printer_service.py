import time
from typing import Dict, Any
from simulator.backend.app.domain.models.printer_data_gen import PrinterDataGenerator

class PrinterService:
    def __init__(self):
        """
        Initialize printer service
        """
        self._printer = PrinterDataGenerator()

    def refresh(self):
        """Manually refresh printer data"""
        self._printer.refresh()

    # ----------------------- Query Interfaces -----------------------
    def get_printer_info(self) -> Dict[str, Any]:
        """Get complete printer information"""
        return self._printer.printer_info

    def get_printer_status(self) -> Dict[str, Any]:
        """Get printer status"""
        return self._printer.printer_status

    def get_bed_status(self) -> Dict[str, Any]:
        """Get print bed status"""
        return self._printer.bed_status

    def get_head_statuses(self) -> list[Dict[str, Any]]:
        """Get list of print head statuses"""
        return self._printer.head_statuses

    def get_led_status(self) -> Dict[str, Any]:
        """Get LED status"""
        return self._printer.led_status

    def get_network_status(self) -> Dict[str, Any]:
        """Get Network status"""
        return self._printer.network_status

    def get_serial_number(self) -> str:
        """Get Serial Number"""
        return self._printer.serial_number

if __name__ == "__main__":
    # Create service instance
    simulator = PrinterService()

    try:
        # Test data fetching
        print("=== Testing printer data ===")
        for i in range(3):
            print(f"\nIteration {i + 1}:")
            print("Printer status:", simulator.get_printer_status())
            print("Bed temperature:", simulator.get_bed_status()["temperature"])
            # Manual refresh
            simulator.refresh()
            time.sleep(1)

        # Test head positions
        print("\n=== Testing head positions ===")
        for i in range(3):
            print(f"\nIteration {i + 1}:")
            print("Head positions:", [head["position"] for head in simulator.get_head_statuses()])
            simulator.refresh()
            time.sleep(1)

    finally:
        print("\nTest completed successfully")