from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Temperature:
    current: float
    target: float

@dataclass
class Bed:
    pre_heat: Dict[str, bool]
    temperature: Temperature
    type: str

@dataclass
class Feeder:
    acceleration: int
    jerk: float
    max_speed: int

@dataclass
class HotendOffset:
    state: str
    x: float
    y: float
    z: float

@dataclass
class HotendStatistics:
    last_material_guid: str
    material_extruded: int
    max_temperature_exposed: int
    prints_since_cleaned: str
    time_spent_hot: int

@dataclass
class Hotend:
    id: str
    offset: HotendOffset
    revision: str
    serial: str
    statistics: HotendStatistics
    temperature: Temperature

@dataclass
class ActiveMaterial:
    GUID: str
    guid: str
    length_remaining: int

@dataclass
class Extruder:
    active_material: ActiveMaterial
    feeder: Feeder
    hotend: Hotend

@dataclass
class Head:
    acceleration: int
    extruders: List[Extruder]
    fan: int
    jerk: Dict[str, float]
    max_speed: Dict[str, int]
    position: Dict[str, float]

@dataclass
class Led:
    blink: Dict
    brightness: int
    hue: int
    saturation: int

@dataclass
class Network:
    ethernet: Dict[str, bool]
    wifi: Dict[str, Any]
    wifi_networks: List

@dataclass
class Printer:
    bed: Bed
    diagnostics: Dict
    heads: List[Head]
    led: Led
    network: Network
    status: str
    validate_header: Dict
    serial_number: str