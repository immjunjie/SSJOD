from simulator.v2.backend.app.domain.models.printer_models import Printer, Bed, Temperature, Head, Extruder, Hotend, HotendOffset, HotendStatistics, Material, Feeder, Led, Network
import logging

logger = logging.getLogger(__name__)

class PrinterRepository:
    def __init__(self):
        self.printer = Printer(
            bed=Bed(
                pre_heat={"active": False},
                temperature=Temperature(current=24.7, target=0),
                type="glass"
            ),
            diagnostics={},
            heads=[
                Head(
                    acceleration=3000,
                    extruders=[
                        Extruder(
                            active_material=Material(GUID="", length_remaining=-1),
                            feeder=Feeder(acceleration=3000, jerk=5, max_speed=45),
                            hotend=Hotend(
                                id="AA 0.4",
                                offset=HotendOffset(state="valid", x=0, y=0, z=0),
                                serial="1db675430000",
                                statistics=HotendStatistics(
                                    last_material_guid="03f24266-0291-43c2-a6da-5211892a2699",
                                    material_extruded=67790,
                                    max_temperature_exposed=235,
                                    time_spent_hot=278760
                                ),
                                temperature=Temperature(current=20.0, target=0)
                            )
                        ),
                        Extruder(
                            active_material=Material(GUID="", length_remaining=-1),
                            feeder=Feeder(acceleration=3000, jerk=5, max_speed=45),
                            hotend=Hotend(
                                id="AA 0.4",
                                offset=HotendOffset(state="valid", x=0.14634146341463428, y=0.14634146341463428, z=0),
                                serial="502f75430000",
                                statistics=HotendStatistics(
                                    last_material_guid="e509f649-9fe6-4b14-ac45-d441438cb4ef",
                                    material_extruded=4370,
                                    max_temperature_exposed=213,
                                    time_spent_hot=47580
                                ),
                                temperature=Temperature(current=20.0, target=0)
                            )
                        )
                    ],
                    fan=0,
                    jerk={"x": 20, "y": 20, "z": 0.4},
                    max_speed={"x": 300, "y": 300, "z": 40},
                    position={"x": -27.8, "y": 247.5, "z": 315}
                )
            ],
            led=Led(blink={}, brightness=100, hue=0, saturation=0),
            network=Network(
                ethernet={"connected": True, "enabled": True},
                wifi={"connected": False, "enabled": False, "mode": "CABLE", "ssid": "UM-NO-HOTSPOT-NAME-SET"},
                wifi_networks=[]
            ),
            status="idle",
            validate_header={},
            serial_number="ULTIMAKER-123456"
        )

    async def get(self) -> Printer:
        logger.info("Fetching printer from repository")
        return self.printer

    async def set_status(self, status: str) -> None:
        logger.info(f"Updating printer status to: {status}")
        self.printer.status = status

    async def get_status(self) -> str:
        logger.info("Fetching printer status from repository")
        return self.printer.status

    async def get_serial_number(self) -> str:
        logger.info("Fetching printer serial number from repository")
        return self.printer.serial_number