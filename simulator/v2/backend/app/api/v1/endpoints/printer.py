from fastapi import APIRouter, Depends, HTTPException
from simulator.v2.backend.app.services.printer_service import PrinterService
from simulator.v2.backend.app.api.v1.schemas import (
    PrinterResponse, BedResponse, HeadResponse, LedResponse, NetworkResponse,
    PreHeatResponse, TemperatureResponse, MaterialResponse, FeederResponse,
    OffsetResponse, StatisticsResponse, HotendResponse, ExtruderResponse,
    JerkResponse, MaxSpeedResponse, PositionResponse, EthernetResponse, WifiResponse
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

async def get_printer_service():
    logger.debug("Creating PrinterService instance")
    return PrinterService()

@router.get("/printer", response_model=PrinterResponse)
async def get_printer(printer_service: PrinterService = Depends(get_printer_service)):
    logger.info("Handling GET /api/v1/printer request")
    try:
        printer = await printer_service.get_printer()
        logger.debug(f"Returning printer data: {printer.status}")

        # Convert domain models to Pydantic models
        bed_response = BedResponse(
            pre_heat=PreHeatResponse(**printer.bed.pre_heat),
            temperature=TemperatureResponse(
                current=printer.bed.temperature.current,
                target=printer.bed.temperature.target
            ),
            type=printer.bed.type
        )
        heads_response = [
            HeadResponse(
                acceleration=head.acceleration,
                extruders=[
                    ExtruderResponse(
                        active_material=MaterialResponse(
                            GUID=extruder.active_material.GUID,
                            guid=extruder.active_material.guid,
                            length_remaining=extruder.active_material.length_remaining
                        ),
                        feeder=FeederResponse(
                            acceleration=extruder.feeder.acceleration,
                            jerk=extruder.feeder.jerk,
                            max_speed=extruder.feeder.max_speed
                        ),
                        hotend=HotendResponse(
                            id=extruder.hotend.id,
                            offset=OffsetResponse(
                                state=extruder.hotend.offset.state,
                                x=extruder.hotend.offset.x,
                                y=extruder.hotend.offset.y,
                                z=extruder.hotend.offset.z
                            ),
                            revision=extruder.hotend.revision,
                            serial=extruder.hotend.serial,
                            statistics=StatisticsResponse(
                                last_material_guid=extruder.hotend.statistics.last_material_guid,
                                material_extruded=extruder.hotend.statistics.material_extruded,
                                max_temperature_exposed=extruder.hotend.statistics.max_temperature_exposed,
                                prints_since_cleaned=extruder.hotend.statistics.prints_since_cleaned,
                                time_spent_hot=extruder.hotend.statistics.time_spent_hot
                            ),
                            temperature=TemperatureResponse(
                                current=extruder.hotend.temperature.current,
                                target=extruder.hotend.temperature.target
                            )
                        )
                    ) for extruder in head.extruders
                ],
                fan=head.fan,
                jerk=JerkResponse(**head.jerk),
                max_speed=MaxSpeedResponse(**head.max_speed),
                position=PositionResponse(**head.position)
            ) for head in printer.heads
        ]
        led_response = LedResponse(
            blink=printer.led.blink,
            brightness=printer.led.brightness,
            hue=printer.led.hue,
            saturation=printer.led.saturation
        )
        network_response = NetworkResponse(
            ethernet=EthernetResponse(**printer.network.ethernet),
            wifi=WifiResponse(**printer.network.wifi),
            wifi_networks=printer.network.wifi_networks
        )

        return PrinterResponse(
            bed=bed_response,
            diagnostics=printer.diagnostics,
            heads=heads_response,
            led=led_response,
            network=network_response,
            status=printer.status,
            validate_header=printer.validate_header
        )
    except Exception as e:
        logger.error(f"Error fetching printer: {e}")
        raise HTTPException(status_code=500, detail=str(e))