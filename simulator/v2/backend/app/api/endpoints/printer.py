from fastapi import APIRouter, Depends, HTTPException
from simulator.v2.backend.app.services.printer_service import PrinterService
from simulator.v2.backend.app.api.schemas import (
    PrinterResponse, BedResponse, HeadResponse, LedResponse, NetworkResponse,
    PreHeatResponse, TemperatureResponse, MaterialResponse, FeederResponse,
    OffsetResponse, StatisticsResponse, HotendResponse, ExtruderResponse,
    JerkResponse, MaxSpeedResponse, PositionResponse, EthernetResponse, WifiResponse,
    StatusRequest, StatusResponse
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Create a global PrinterService instance
_printer_service = PrinterService()

async def get_printer_service():
    logger.debug("Returning global PrinterService instance")
    return _printer_service

# ----------------------- Printer Integration -----------------------

@router.get("/printer", response_model=PrinterResponse, tags=["Printer"])
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
            validate_header=printer.validate_header,
            serial_number=printer.serial_number
        )
    except Exception as e:
        logger.error(f"Error fetching printer: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/printer/status", response_model=StatusResponse, tags=["Printer"])
async def get_printer_status(printer_service: PrinterService = Depends(get_printer_service)):
    logger.info("Handling GET /api/v1/printer/status request")
    try:
        status = await printer_service.get_printer_status()
        return StatusResponse(status=status)
    except Exception as e:
        logger.error(f"Error fetching printer status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/printer/status", response_model=StatusResponse, tags=["Printer"])
async def set_printer_status(
    status_request: StatusRequest,
    printer_service: PrinterService = Depends(get_printer_service)
):
    logger.info(f"Handling POST /api/v1/printer/status request with status: {status_request.status}")
    try:
        await printer_service.set_printer_status(status_request.status)
        return StatusResponse(status=status_request.status)
    except ValueError as e:
        logger.error(f"Invalid status: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error setting printer status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------- Bed Integration -----------------------

@router.get("/printer/bed", response_model=BedResponse, tags=["Printer"])
async def get_printer_bed(printer_service: PrinterService = Depends(get_printer_service)):
    logger.info("Handling GET /api/v1/printer/bed request")
    try:
        printer = await printer_service.get_printer()
        return BedResponse(
            pre_heat=PreHeatResponse(**printer.bed.pre_heat),
            temperature=TemperatureResponse(
                current=printer.bed.temperature.current,
                target=printer.bed.temperature.target
            ),
            type=printer.bed.type
        )
    except Exception as e:
        logger.error(f"Error fetching printer bed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/printer/bed/temperature", response_model=TemperatureResponse, tags=["Printer"])
async def get_printer_bed_temperature(printer_service: PrinterService = Depends(get_printer_service)):
    logger.info("Handling GET /api/v1/printer/bed/temperature request")
    try:
        printer = await printer_service.get_printer()
        return TemperatureResponse(
            current=printer.bed.temperature.current,
            target=printer.bed.temperature.target
        )
    except Exception as e:
        logger.error(f"Error fetching bed temperature: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------- Head Integration -----------------------

@router.get("/printer/heads", response_model=list[HeadResponse], tags=["Printer"])
async def get_printer_heads(printer_service: PrinterService = Depends(get_printer_service)):
    logger.info("Handling GET /api/v1/printer/heads request")
    try:
        printer = await printer_service.get_printer()
        return [
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
    except Exception as e:
        logger.error(f"Error fetching printer heads: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/printer/heads/{head_id}", response_model=HeadResponse, tags=["Printer"])
async def get_printer_head_by_id(head_id: int, printer_service: PrinterService = Depends(get_printer_service)):
    logger.info(f"Handling GET /api/v1/printer/heads/{head_id} request")
    try:
        printer = await printer_service.get_printer()
        if head_id < 0 or head_id >= len(printer.heads):
            logger.error(f"Head ID {head_id} not found")
            raise HTTPException(status_code=404, detail="Head ID not found")
        head = printer.heads[head_id]
        return HeadResponse(
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
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching head {head_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/printer/heads/{head_id}/position", response_model=PositionResponse, tags=["Printer"])
async def get_printer_head_position_by_id(head_id: int, printer_service: PrinterService = Depends(get_printer_service)):
    logger.info(f"Handling GET /api/v1/printer/heads/{head_id}/position request")
    try:
        printer = await printer_service.get_printer()
        if head_id < 0 or head_id >= len(printer.heads):
            logger.error(f"Head ID {head_id} not found")
            raise HTTPException(status_code=404, detail="Head ID not found")
        head = printer.heads[head_id]
        return PositionResponse(**head.position)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching head {head_id} position: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/printer/heads/{head_id}/extruders", response_model=list[ExtruderResponse], tags=["Printer"])
async def get_printer_head_extruders_by_id(head_id: int, printer_service: PrinterService = Depends(get_printer_service)):
    logger.info(f"Handling GET /api/v1/printer/heads/{head_id}/extruders request")
    try:
        printer = await printer_service.get_printer()
        if head_id < 0 or head_id >= len(printer.heads):
            logger.error(f"Head ID {head_id} not found")
            raise HTTPException(status_code=404, detail="Head ID not found")
        head = printer.heads[head_id]
        return [
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
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching extruders for head {head_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/printer/heads/{head_id}/extruders/{extruder_id}", response_model=ExtruderResponse, tags=["Printer"])
async def get_printer_head_extruder_by_id(head_id: int, extruder_id: int, printer_service: PrinterService = Depends(get_printer_service)):
    logger.info(f"Handling GET /api/v1/printer/heads/{head_id}/extruders/{extruder_id} request")
    try:
        printer = await printer_service.get_printer()
        if head_id < 0 or head_id >= len(printer.heads):
            logger.error(f"Head ID {head_id} not found")
            raise HTTPException(status_code=404, detail="Head ID not found")
        head = printer.heads[head_id]
        if extruder_id < 0 or extruder_id >= len(head.extruders):
            logger.error(f"Extruder ID {extruder_id} not found for head {head_id}")
            raise HTTPException(status_code=404, detail="Extruder ID not found")
        extruder = head.extruders[extruder_id]
        return ExtruderResponse(
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
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching extruder {extruder_id} for head {head_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/printer/heads/{head_id}/extruders/{extruder_id}/hotend", response_model=HotendResponse, tags=["Printer"])
async def get_printer_head_extruder_hotend(head_id: int, extruder_id: int, printer_service: PrinterService = Depends(get_printer_service)):
    logger.info(f"Handling GET /api/v1/printer/heads/{head_id}/extruders/{extruder_id}/hotend request")
    try:
        printer = await printer_service.get_printer()
        if head_id < 0 or head_id >= len(printer.heads):
            logger.error(f"Head ID {head_id} not found")
            raise HTTPException(status_code=404, detail="Head ID not found")
        head = printer.heads[head_id]
        if extruder_id < 0 or extruder_id >= len(head.extruders):
            logger.error(f"Extruder ID {extruder_id} not found for head {head_id}")
            raise HTTPException(status_code=404, detail="Extruder ID not found")
        extruder = head.extruders[extruder_id]
        return HotendResponse(
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
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching hotend for extruder {extruder_id} in head {head_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/printer/heads/{head_id}/extruders/{extruder_id}/hotend/temperature", response_model=TemperatureResponse, tags=["Printer"])
async def get_printer_head_extruder_hotend_temperature(head_id: int, extruder_id: int, printer_service: PrinterService = Depends(get_printer_service)):
    logger.info(f"Handling GET /api/v1/printer/heads/{head_id}/extruders/{extruder_id}/hotend/temperature request")
    try:
        printer = await printer_service.get_printer()
        if head_id < 0 or head_id >= len(printer.heads):
            logger.error(f"Head ID {head_id} not found")
            raise HTTPException(status_code=404, detail="Head ID not found")
        head = printer.heads[head_id]
        if extruder_id < 0 or extruder_id >= len(head.extruders):
            logger.error(f"Extruder ID {extruder_id} not found for head {head_id}")
            raise HTTPException(status_code=404, detail="Extruder ID not found")
        extruder = head.extruders[extruder_id]
        return TemperatureResponse(
            current=extruder.hotend.temperature.current,
            target=extruder.hotend.temperature.target
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching hotend temperature for extruder {extruder_id} in head {head_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/printer/heads/{head_id}/extruders/{extruder_id}/hotend/temperature/current", response_model=float, tags=["Printer"])
async def get_printer_head_extruder_hotend_temperature_current(head_id: int, extruder_id: int, printer_service: PrinterService = Depends(get_printer_service)):
    logger.info(f"Handling GET /api/v1/printer/heads/{head_id}/extruders/{extruder_id}/hotend/temperature/current request")
    try:
        printer = await printer_service.get_printer()
        if head_id < 0 or head_id >= len(printer.heads):
            logger.error(f"Head ID {head_id} not found")
            raise HTTPException(status_code=404, detail="Head ID not found")
        head = printer.heads[head_id]
        if extruder_id < 0 or extruder_id >= len(head.extruders):
            logger.error(f"Extruder ID {extruder_id} not found for head {head_id}")
            raise HTTPException(status_code=404, detail="Extruder ID not found")
        extruder = head.extruders[extruder_id]
        return extruder.hotend.temperature.current
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching hotend current temperature for extruder {extruder_id} in head {head_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/printer/heads/{head_id}/extruders/{extruder_id}/hotend/temperature/target", response_model=float, tags=["Printer"])
async def get_printer_head_extruder_hotend_temperature_target(head_id: int, extruder_id: int, printer_service: PrinterService = Depends(get_printer_service)):
    logger.info(f"Handling GET /api/v1/printer/heads/{head_id}/extruders/{extruder_id}/hotend/temperature/target request")
    try:
        printer = await printer_service.get_printer()
        if head_id < 0 or head_id >= len(printer.heads):
            logger.error(f"Head ID {head_id} not found")
            raise HTTPException(status_code=404, detail="Head ID not found")
        head = printer.heads[head_id]
        if extruder_id < 0 or extruder_id >= len(head.extruders):
            logger.error(f"Extruder ID {extruder_id} not found for head {head_id}")
            raise HTTPException(status_code=404, detail="Extruder ID not found")
        extruder = head.extruders[extruder_id]
        return extruder.hotend.temperature.target
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching hotend target temperature for extruder {extruder_id} in head {head_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/printer/heads/{head_id}/extruders/{extruder_id}/hotend/statistics", response_model=StatisticsResponse, tags=["Printer"])
async def get_printer_head_extruder_hotend_statistics(head_id: int, extruder_id: int, printer_service: PrinterService = Depends(get_printer_service)):
    logger.info(f"Handling GET /api/v1/printer/heads/{head_id}/extruders/{extruder_id}/hotend/statistics request")
    try:
        printer = await printer_service.get_printer()
        if head_id < 0 or head_id >= len(printer.heads):
            logger.error(f"Head ID {head_id} not found")
            raise HTTPException(status_code=404, detail="Head ID not found")
        head = printer.heads[head_id]
        if extruder_id < 0 or extruder_id >= len(head.extruders):
            logger.error(f"Extruder ID {extruder_id} not found for head {head_id}")
            raise HTTPException(status_code=404, detail="Extruder ID not found")
        extruder = head.extruders[extruder_id]
        return StatisticsResponse(
            last_material_guid=extruder.hotend.statistics.last_material_guid,
            material_extruded=extruder.hotend.statistics.material_extruded,
            max_temperature_exposed=extruder.hotend.statistics.max_temperature_exposed,
            prints_since_cleaned=extruder.hotend.statistics.prints_since_cleaned,
            time_spent_hot=extruder.hotend.statistics.time_spent_hot
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching hotend statistics for extruder {extruder_id} in head {head_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/printer/heads/{head_id}/extruders/{extruder_id}/hotend/statistics/time_spent_hot", response_model=float, tags=["Printer"])
async def get_printer_head_extruder_hotend_statistics_time_spent_hot(head_id: int, extruder_id: int, printer_service: PrinterService = Depends(get_printer_service)):
    logger.info(f"Handling GET /api/v1/printer/heads/{head_id}/extruders/{extruder_id}/hotend/statistics/time_spent_hot request")
    try:
        printer = await printer_service.get_printer()
        if head_id < 0 or head_id >= len(printer.heads):
            logger.error(f"Head ID {head_id} not found")
            raise HTTPException(status_code=404, detail="Head ID not found")
        head = printer.heads[head_id]
        if extruder_id < 0 or extruder_id >= len(head.extruders):
            logger.error(f"Extruder ID {extruder_id} not found for head {head_id}")
            raise HTTPException(status_code=404, detail="Extruder ID not found")
        extruder = head.extruders[extruder_id]
        return extruder.hotend.statistics.time_spent_hot
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching hotend time spent hot for extruder {extruder_id} in head {head_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/printer/heads/{head_id}/extruders/{extruder_id}/hotend/statistics/material_extruded", response_model=float, tags=["Printer"])
async def get_printer_head_extruder_hotend_statistics_material_extruded(head_id: int, extruder_id: int, printer_service: PrinterService = Depends(get_printer_service)):
    logger.info(f"Handling GET /api/v1/printer/heads/{head_id}/extruders/{extruder_id}/hotend/statistics/material_extruded request")
    try:
        printer = await printer_service.get_printer()
        if head_id < 0 or head_id >= len(printer.heads):
            logger.error(f"Head ID {head_id} not found")
            raise HTTPException(status_code=404, detail="Head ID not found")
        head = printer.heads[head_id]
        if extruder_id < 0 or extruder_id >= len(head.extruders):
            logger.error(f"Extruder ID {extruder_id} not found for head {head_id}")
            raise HTTPException(status_code=404, detail="Extruder ID not found")
        extruder = head.extruders[extruder_id]
        return extruder.hotend.statistics.material_extruded
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching hotend material extruded for extruder {extruder_id} in head {head_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/printer/heads/{head_id}/extruders/{extruder_id}/feeder", response_model=FeederResponse, tags=["Printer"])
async def get_printer_head_extruder_feeder(head_id: int, extruder_id: int, printer_service: PrinterService = Depends(get_printer_service)):
    logger.info(f"Handling GET /api/v1/printer/heads/{head_id}/extruders/{extruder_id}/feeder request")
    try:
        printer = await printer_service.get_printer()
        if head_id < 0 or head_id >= len(printer.heads):
            logger.error(f"Head ID {head_id} not found")
            raise HTTPException(status_code=404, detail="Head ID not found")
        head = printer.heads[head_id]
        if extruder_id < 0 or extruder_id >= len(head.extruders):
            logger.error(f"Extruder ID {extruder_id} not found for head {head_id}")
            raise HTTPException(status_code=404, detail="Extruder ID not found")
        extruder = head.extruders[extruder_id]
        return FeederResponse(
            acceleration=extruder.feeder.acceleration,
            jerk=extruder.feeder.jerk,
            max_speed=extruder.feeder.max_speed
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching feeder for extruder {extruder_id} in head {head_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/printer/heads/{head_id}/extruders/{extruder_id}/feeder/max_speed", response_model=float, tags=["Printer"])
async def get_printer_head_extruder_feeder_max_speed(head_id: int, extruder_id: int, printer_service: PrinterService = Depends(get_printer_service)):
    logger.info(f"Handling GET /api/v1/printer/heads/{head_id}/extruders/{extruder_id}/feeder/max_speed request")
    try:
        printer = await printer_service.get_printer()
        if head_id < 0 or head_id >= len(printer.heads):
            logger.error(f"Head ID {head_id} not found")
            raise HTTPException(status_code=404, detail="Head ID not found")
        head = printer.heads[head_id]
        if extruder_id < 0 or extruder_id >= len(head.extruders):
            logger.error(f"Extruder ID {extruder_id} not found for head {head_id}")
            raise HTTPException(status_code=404, detail="Extruder ID not found")
        extruder = head.extruders[extruder_id]
        return extruder.feeder.max_speed
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching feeder max speed for extruder {extruder_id} in head {head_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/printer/heads/{head_id}/extruders/{extruder_id}/active_material", response_model=MaterialResponse, tags=["Printer"])
async def get_printer_head_extruder_active_material(head_id: int, extruder_id: int, printer_service: PrinterService = Depends(get_printer_service)):
    logger.info(f"Handling GET /api/v1/printer/heads/{head_id}/extruders/{extruder_id}/active_material request")
    try:
        printer = await printer_service.get_printer()
        if head_id < 0 or head_id >= len(printer.heads):
            logger.error(f"Head ID {head_id} not found")
            raise HTTPException(status_code=404, detail="Head ID not found")
        head = printer.heads[head_id]
        if extruder_id < 0 or extruder_id >= len(head.extruders):
            logger.error(f"Extruder ID {extruder_id} not found for head {head_id}")
            raise HTTPException(status_code=404, detail="Extruder ID not found")
        extruder = head.extruders[extruder_id]
        return MaterialResponse(
            GUID=extruder.active_material.GUID,
            guid=extruder.active_material.guid,
            length_remaining=extruder.active_material.length_remaining
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching active material for extruder {extruder_id} in head {head_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/printer/heads/{head_id}/extruders/{extruder_id}/active_material/length_remaining", response_model=float, tags=["Printer"])
async def get_printer_head_extruder_active_material_length_remaining(head_id: int, extruder_id: int, printer_service: PrinterService = Depends(get_printer_service)):
    logger.info(f"Handling GET /api/v1/printer/heads/{head_id}/extruders/{extruder_id}/active_material/length_remaining request")
    try:
        printer = await printer_service.get_printer()
        if head_id < 0 or head_id >= len(printer.heads):
            logger.error(f"Head ID {head_id} not found")
            raise HTTPException(status_code=404, detail="Head ID not found")
        head = printer.heads[head_id]
        if extruder_id < 0 or extruder_id >= len(head.extruders):
            logger.error(f"Extruder ID {extruder_id} not found for head {head_id}")
            raise HTTPException(status_code=404, detail="Extruder ID not found")
        extruder = head.extruders[extruder_id]
        return extruder.active_material.length_remaining
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching active material length remaining for extruder {extruder_id} in head {head_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------- LED Integration -----------------------

@router.get("/printer/led", response_model=LedResponse, tags=["Printer"])
async def get_printer_led(printer_service: PrinterService = Depends(get_printer_service)):
    logger.info("Handling GET /api/v1/printer/led request")
    try:
        printer = await printer_service.get_printer()
        return LedResponse(
            blink=printer.led.blink,
            brightness=printer.led.brightness,
            hue=printer.led.hue,
            saturation=printer.led.saturation
        )
    except Exception as e:
        logger.error(f"Error fetching printer LED: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------- Network Integration -----------------------

@router.get("/printer/network_status", response_model=NetworkResponse, tags=["Printer"])
async def get_printer_network_status(printer_service: PrinterService = Depends(get_printer_service)):
    logger.info("Handling GET /api/v1/printer/network_status request")
    try:
        printer = await printer_service.get_printer()
        return NetworkResponse(
            ethernet=EthernetResponse(**printer.network.ethernet),
            wifi=WifiResponse(**printer.network.wifi),
            wifi_networks=printer.network.wifi_networks
        )
    except Exception as e:
        logger.error(f"Error fetching network status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------- Serial Number Integration -----------------------

@router.get("/printer/serial_number", response_model=str, tags=["Printer"])
async def get_printer_serial_number(printer_service: PrinterService = Depends(get_printer_service)):
    logger.info("Handling GET /api/v1/printer/serial_number request")
    try:
        return await printer_service.get_serial_number()
    except Exception as e:
        logger.error(f"Error fetching serial number: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------- Manual Integration Test -----------------------

def run_manual_integration_tests():
    from simulator.v2.backend.main import app
    from starlette.testclient import TestClient

    client = TestClient(app)

    endpoints = [
        "printer",
        "printer/status",
        "printer/bed",
        "printer/bed/temperature",
        "printer/heads",
        "printer/heads/0",
        "printer/heads/0/position",
        "printer/heads/0/extruders",
        "printer/heads/0/extruders/0",
        "printer/heads/0/extruders/0/hotend",
        "printer/heads/0/extruders/0/hotend/temperature",
        "printer/heads/0/extruders/0/hotend/temperature/current",
        "printer/heads/0/extruders/0/hotend/temperature/target",
        "printer/heads/0/extruders/0/hotend/statistics",
        "printer/heads/0/extruders/0/hotend/statistics/time_spent_hot",
        "printer/heads/0/extruders/0/hotend/statistics/material_extruded",
        "printer/heads/0/extruders/0/feeder",
        "printer/heads/0/extruders/0/feeder/max_speed",
        "printer/heads/0/extruders/0/active_material",
        "printer/heads/0/extruders/0/active_material/length_remaining",
        "printer/led",
        "printer/network_status",
        "printer/serial_number"
    ]

    for ep in endpoints:
        print(f"\n --- Test: /api/v1/{ep} ---")
        try:
            response = client.get(f"/api/v1/{ep}")
            print(f"Code: {response.status_code}, Response: {response.json()}")
        except Exception as e:
            print(f"Error testing /api/v1/{ep}: {e}")

if __name__ == "__main__":
    run_manual_integration_tests()