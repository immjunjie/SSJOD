import random
from typing import Dict, Any
import uuid


class PrinterDataGenerator:
    def __init__(self):
        self._printer_serial = "UM3-" + "".join(random.choices("0123456789ABCDEF", k=8))

    def generate_printer_info(self) -> Dict[str, Any]:
        return {
            "bed": self.generate_bed_status(),
            "diagnostics": {},
            "heads": [self.generate_head_status(0), self.generate_head_status(1)],
            "led": self.generate_led_status(),
            "network": self.generate_network_status(),
            "status": random.choice(["printing", "idle", "error"]),
            "validate_header": {}
        }

    def generate_printer_status() -> Dict[str, Any]:
        return {
            "status": random.choice(["printing", "idle", "error"]),
        }

    def generate_bed_status(self) -> Dict[str, Any]:
        return {
            "pre_heat": {"active": False},
            "temperature": {
                "current": round(random.uniform(20, 70), 1),
                "target": 60
            },
            "type": "glass"
        }

    def generate_head_status(self, head_index: int) -> Dict[str, Any]:
        material_guid = str(uuid.uuid4()) if random.random() > 0.3 else ""
        return {
            "acceleration": 1500,
            "extruders": [self.generate_extruder_status(head_index, material_guid)],
            "fan": 100,
            "jerk": {"x": 20, "y": 20, "z": 0.4},
            "max_speed": {"x": 300, "y": 300, "z": 40},
            "position": {
                "x": round(random.uniform(0, 300), 3),
                "y": round(random.uniform(0, 300), 3),
                "z": round(random.uniform(0, 50), 1)
            }
        }

    def generate_extruder_status(self, head_index: int, material_guid: str) -> Dict[str, Any]:
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

    def generate_led_status(self) -> Dict[str, Any]:
        return {
            "blink": {},
            "brightness": 100,
            "hue": 0,
            "saturation": 0
        }

    def generate_network_status(self) -> Dict[str, Any]:
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