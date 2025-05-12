import random
from typing import Dict, Any, List
import uuid


class PrinterDataGenerator:
    def __init__(self):
        self._printer_serial = "UM3-" + "".join(random.choices("0123456789ABCDEF", k=8))
        self._refresh_data()

    def _refresh_data(self):
        """refresh all data"""
        self._printer_info = self._generate_printer_info()
        self._printer_status = self._generate_printer_status()

    # ----------------------- Generators ------------------------
    def _generate_printer_info(self) -> Dict[str, Any]:
        return {
            "bed": self._generate_bed_status(),
            "diagnostics": {},
            "heads": [self._generate_head_status(0), self._generate_head_status(1)],
            "led": self._generate_led_status(),
            "network": self._generate_network_status(),
            "status": random.choice(["printing", "idle", "error"]),
            "validate_header": {}
        }

    def _generate_printer_status(self) -> Dict[str, Any]:
        return {
            "status": random.choice(["printing", "idle", "error"]),
        }

    def _generate_bed_status(self) -> Dict[str, Any]:
        return {
            "pre_heat": {"active": False},
            "temperature": {
                "current": round(random.uniform(20, 70), 1),
                "target": 60
            },
            "type": "glass"
        }

    def _generate_head_status(self, head_index: int) -> Dict[str, Any]:
        material_guid = str(uuid.uuid4()) if random.random() > 0.3 else ""
        return {
            "acceleration": 1500,
            "extruders": [self._generate_extruder_status(head_index, material_guid)],
            "fan": 100,
            "jerk": {"x": 20, "y": 20, "z": 0.4},
            "max_speed": {"x": 300, "y": 300, "z": 40},
            "position": {
                "x": round(random.uniform(0, 300), 3),
                "y": round(random.uniform(0, 300), 3),
                "z": round(random.uniform(0, 50), 1)
            }
        }

    def _generate_extruder_status(self, head_index: int, material_guid: str) -> Dict[str, Any]:
        return {
            "active_material": {
                "GUID": material_guid,
                "guid": material_guid,
                "length_remaining": -1
            },
            "feeder": {
                "acceleration": 3000,
                "jerk": 5,
                "max_speed": 45
            },
            "hotend": {
                "id": "AA 0.4",
                "offset": {
                    "state": "valid",
                    "x": round(random.uniform(0, 0.2), 10),
                    "y": round(random.uniform(0, 0.2), 10),
                    "z": 0
                },
                "revision": "1",
                "serial": f"{head_index}db675430000",
                "statistics": {
                    "last_material_guid": str(uuid.uuid4()),
                    "material_extruded": random.randint(1000, 100000),
                    "max_temperature_exposed": random.randint(200, 250),
                    "prints_since_cleaned": str(random.randint(1, 100)),
                    "time_spent_hot": random.randint(10000, 300000)
                },
                "temperature": {
                    "current": round(random.uniform(20, 250), 1),
                    "target": 215 if material_guid else 0
                }
            }
        }

    def _generate_led_status(self) -> Dict[str, Any]:
        return {
            "blink": {},
            "brightness": 100,
            "hue": 0,
            "saturation": 0
        }

    def _generate_network_status(self) -> Dict[str, Any]:
        return {
            "ethernet": {
                "connected": True,
                "enabled": True
            },
            "wifi": {
                "connected": False,
                "enabled": False,
                "mode": "CABLE",
                "ssid": "UM-NO-HOTSPOT-NAME-SET"
            },
            "wifi_networks": []
        }

    # ----------------------- Public Interface ------------------------
    def refresh(self):
        """refresh all data manually"""
        self._refresh_data()

    @property
    def printer_info(self) -> Dict[str, Any]:
        return self._printer_info

    @property
    def printer_status(self) -> Dict[str, Any]:
        return self._printer_status

    @property
    def bed_status(self) -> Dict[str, Any]:
        return self._printer_info["bed"]

    @property
    def head_statuses(self) -> List[Dict[str, Any]]:
        return self._printer_info["heads"]

    @property
    def led_status(self) -> Dict[str, Any]:
        return self._printer_info["led"]

    @property
    def network_status(self) -> Dict[str, Any]:
        return self._printer_info["network"]

    @property
    def serial_number(self) -> str:
        return self._printer_serial


if __name__ == "__main__":
    simulator = PrinterDataGenerator()

    # Print the data initially
    print("Initial Data:")
    print(simulator.printer_info)
    print(simulator.printer_status)
    print(simulator.bed_status)
    print(simulator.head_statuses)
    print(simulator.led_status)
    print(simulator.network_status)
    print(simulator.serial_number)

    # Print the data at the second time
    simulator.refresh()
    print("\nAfter Refresh:")
    print(simulator.printer_info)
    print(simulator.printer_status)
    print(simulator.bed_status)
    print(simulator.head_statuses)
    print(simulator.led_status)
    print(simulator.network_status)
    print(simulator.serial_number)