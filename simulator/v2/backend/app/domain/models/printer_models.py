from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class Temperature(BaseModel):
    current: Optional[float] = None
    target: Optional[float] = None

class BedPreHeat(BaseModel):
    temperature: Optional[float] = Field(default=None, description="Target temperature of bed in degrees Celsius. Set to 0 to stop pre-heating")
    timeout: Optional[float] = Field(default=None, description="Timeout for preheating in seconds")

class Bed(BaseModel):
    type: Optional[str] = None
    temperature: Optional[Temperature] = None
    pre_heat: Optional[Dict[str, Any]] = None

class Feeder(BaseModel):
    position: Optional[float] = Field(default=None, description="The position of the feeder. This is otherwise known as the E value")
    max_speed: Optional[float] = Field(default=None, description="Max speed of the feeder in mm/s")
    jerk: Optional[float] = Field(default=None, description="Acceleration of the acceleration (in mm/s^3)")
    acceleration: Optional[float] = Field(default=None, description="Acceleration of the feeder (in mm/s^2)")

class HotendOffset(BaseModel):
    state: Optional[str] = Field(default=None, description="State of the offset", pattern=r"^(valid|invalid)$")
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None

class HotendStatistics(BaseModel):
    last_material_guid: Optional[str] = Field(default=None, description="UUID in UUID4 format")
    material_extruded: Optional[int] = Field(default=None, description="Approximate accumulated amount of material extruded during printing in millimeters")
    max_temperature_exposed: Optional[int] = Field(default=None, description="Maximum temperature exposed in degrees Celsius")
    time_spent_hot: Optional[int] = Field(default=None, description="Approximate time spent above 65 degrees Celsius in seconds")
    prints_since_cleaned: Optional[str] = None

class Hotend(BaseModel):
    id: str
    revision: Optional[str] = None
    serial: Optional[str] = Field(default=None, description="A hexadecimal representation of the serial number")
    temperature: Optional[Temperature] = None
    offset: Optional[HotendOffset] = None
    statistics: Optional[HotendStatistics] = None

class Material(BaseModel):
    GUID: Optional[str] = Field(default=None, description="Unique identifier of the material, empty string if no material loaded")
    guid: Optional[str] = None
    length_remaining: Optional[float] = Field(default=None, description="mm of filament remaining on spool. Returns -1 if the remaining length is unknown")

class Extruder(BaseModel):
    active_material: Optional[Material] = None
    feeder: Optional[Feeder] = None
    hotend: Optional[Hotend] = None

class XYZ(BaseModel):
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None

class Head(BaseModel):
    position: Optional[Dict[str, Any]] = None
    max_speed: Optional[Dict[str, Any]] = None
    acceleration: Optional[float] = Field(default=None, description="The default acceleration for the X, Y and Z axis")
    jerk: Optional[Dict[str, Any]] = None
    extruders: Optional[List[Extruder]] = None
    fan: Optional[float] = Field(default=None, description="The speed of the fan in percentage")

class Led(BaseModel):
    hue: Optional[float] = Field(default=None, ge=0, le=360, description="A LED hue value that ranges from 0-360")
    saturation: Optional[float] = Field(default=None, ge=0, le=100, description="A LED saturation value that ranges from 0-100")
    brightness: Optional[float] = Field(default=None, ge=0, le=100, description="A LED brightness value that ranges from 0-100")
    blink: Optional[Dict[str, Any]] = None

class WifiNetwork(BaseModel):
    ssid: Optional[str] = None
    security_required: Optional[bool] = None
    strength: Optional[int] = None

class InlineModel(BaseModel):
    connected: Optional[bool] = Field(default=None, description="A bool indicating if the interface is connected")
    enabled: Optional[bool] = Field(default=None, description="A bool indicating if the interface is enabled")
    mode: Optional[str] = Field(default=None, description="Wifi mode", pattern=r"^(AUTO|HOTSPOT|WIFI SETUP|CABLE|WIRELESS|OFFLINE)$")
    ssid: Optional[str] = Field(default=None, description="If connected, the SSID of the hotspot this machine is connected to")

class InlineModel0(BaseModel):
    connected: Optional[bool] = Field(default=None, description="A bool indicating if the interface is connected")
    enabled: Optional[bool] = Field(default=None, description="A bool indicating if the interface is enabled")

class Network(BaseModel):
    wifi: Optional[Dict[str, Any]] = None
    wifi_networks: Optional[List[WifiNetwork]] = None
    ethernet: Optional[Dict[str, Any]] = None

class Camera(BaseModel):
    feed: str

class AirManagerStatus(str, Enum):
    ERROR = "error"
    UNAVAILABLE = "unavailable"
    AVAILABLE = "available"
    INSTALLING_FIRMWARE = "installing_firmware"

class AirManagerFilterStatus(str, Enum):
    UNKNOWN = "unknown"
    PEAK_PERFORMANCE = "peak_performance"
    REPLACEMENT_NEAR = "replacement_near"
    REPLACEMENT_REQUIRED = "replacement_required"
    MISSING = "missing"

class AirManager(BaseModel):
    firmware_version: Optional[str] = Field(default=None, description="Version of the installed firmware")
    filter_age: Optional[float] = Field(default=None, description="Filter hours used")
    filter_max_age: Optional[float] = Field(default=None, description="Lifespan of the filter in hours")
    filter_status: Optional[AirManagerFilterStatus] = Field(default=None, description="Indicate the status of the Air Manager filter")
    status: Optional[AirManagerStatus] = Field(default=None, description="Indicate the status of the Air Manager device")
    fan_speed: Optional[float] = Field(default=None, description="Speed of the fan in revolutions per minute")

class PrinterStatus(str, Enum):
    BOOTING = "booting"
    WAITING_FOR_PERIPHERALS = "waiting_for_peripherals"
    IDLE = "idle"
    PRINTING = "printing"
    ERROR = "error"
    MAINTENANCE = "maintenance"

class Printer(BaseModel):
    bed: Optional[Bed] = None
    diagnostics: Optional[Dict[str, Any]] = None
    heads: List[Head]
    led: Optional[Led] = None
    network: Optional[Network] = None
    status: Optional[PrinterStatus] = Field(default=None, description="Printer status")
    validate_header: Optional[Dict[str, Any]] = None
    serial_number: Optional[str] = None
    camera: Optional[Camera] = None
    airmanager: Optional[AirManager] = None