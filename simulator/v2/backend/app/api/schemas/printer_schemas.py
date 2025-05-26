from pydantic import BaseModel
from typing import Dict, List, Any, Literal

class PreHeatResponse(BaseModel):
    active: bool

class TemperatureResponse(BaseModel):
    current: float
    target: float

class BedResponse(BaseModel):
    pre_heat: PreHeatResponse
    temperature: TemperatureResponse
    type: str

class MaterialResponse(BaseModel):
    GUID: str
    guid: str
    length_remaining: int

class FeederResponse(BaseModel):
    acceleration: int
    jerk: float
    max_speed: int

class OffsetResponse(BaseModel):
    state: str
    x: float
    y: float
    z: float

class StatisticsResponse(BaseModel):
    last_material_guid: str
    material_extruded: int
    max_temperature_exposed: int
    prints_since_cleaned: str
    time_spent_hot: int

class HotendResponse(BaseModel):
    id: str
    offset: OffsetResponse
    revision: str
    serial: str
    statistics: StatisticsResponse
    temperature: TemperatureResponse

class ExtruderResponse(BaseModel):
    active_material: MaterialResponse
    feeder: FeederResponse
    hotend: HotendResponse

class JerkResponse(BaseModel):
    x: float
    y: float
    z: float

class MaxSpeedResponse(BaseModel):
    x: int
    y: int
    z: int

class PositionResponse(BaseModel):
    x: float
    y: float
    z: float

class HeadResponse(BaseModel):
    acceleration: int
    extruders: List[ExtruderResponse]
    fan: int
    jerk: JerkResponse
    max_speed: MaxSpeedResponse
    position: PositionResponse

class LedResponse(BaseModel):
    blink: Dict[str, Any]
    brightness: int
    hue: int
    saturation: int

class EthernetResponse(BaseModel):
    connected: bool
    enabled: bool

class WifiResponse(BaseModel):
    connected: bool
    enabled: bool
    mode: str
    ssid: str

class NetworkResponse(BaseModel):
    ethernet: EthernetResponse
    wifi: WifiResponse
    wifi_networks: List[Any]

class PrinterResponse(BaseModel):
    bed: BedResponse
    diagnostics: Dict[str, Any]
    heads: List[HeadResponse]
    led: LedResponse
    network: NetworkResponse
    status: str
    validate_header: Dict[str, Any]
    serial_number: str

class StatusRequest(BaseModel):
    status: Literal["printing", "idle"]

class StatusResponse(BaseModel):
    status: str