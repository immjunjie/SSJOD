from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

try:
	from pydantic import ConfigDict
except Exception:
	ConfigDict = dict  # fallback, though environment uses pydantic v2


class TemperatureResponse(BaseModel):
	current: Optional[float] = None
	target: Optional[float] = None


class PreHeatResponse(BaseModel):
	model_config = ConfigDict(extra='allow')
	active: Optional[bool] = None


class MaterialResponse(BaseModel):
	GUID: Optional[str] = None
	guid: Optional[str] = None
	length_remaining: Optional[float] = None


class FeederResponse(BaseModel):
	acceleration: Optional[float] = None
	jerk: Optional[float] = None
	max_speed: Optional[float] = None


class OffsetResponse(BaseModel):
	state: Optional[str] = None
	x: Optional[float] = None
	y: Optional[float] = None
	z: Optional[float] = None


class StatisticsResponse(BaseModel):
	last_material_guid: Optional[str] = None
	material_extruded: Optional[int] = None
	max_temperature_exposed: Optional[int] = None
	prints_since_cleaned: Optional[str] = None
	time_spent_hot: Optional[int] = None


class HotendResponse(BaseModel):
	id: str
	revision: Optional[str] = None
	serial: Optional[str] = None
	statistics: Optional[StatisticsResponse] = None
	temperature: Optional[TemperatureResponse] = None
	offset: Optional[OffsetResponse] = None


class ExtruderResponse(BaseModel):
	active_material: Optional[MaterialResponse] = None
	feeder: Optional[FeederResponse] = None
	hotend: Optional[HotendResponse] = None


class JerkResponse(BaseModel):
	x: Optional[float] = None
	y: Optional[float] = None
	z: Optional[float] = None


class MaxSpeedResponse(BaseModel):
	x: Optional[float] = None
	y: Optional[float] = None
	z: Optional[float] = None


class PositionResponse(BaseModel):
	x: Optional[float] = None
	y: Optional[float] = None
	z: Optional[float] = None


class HeadResponse(BaseModel):
	acceleration: Optional[float] = None
	extruders: Optional[List[ExtruderResponse]] = None
	fan: Optional[float] = None
	jerk: Optional[JerkResponse] = None
	max_speed: Optional[MaxSpeedResponse] = None
	position: Optional[PositionResponse] = None


class BedResponse(BaseModel):
	pre_heat: Optional[PreHeatResponse] = None
	temperature: Optional[TemperatureResponse] = None
	type: Optional[str] = None


class LedResponse(BaseModel):
	blink: Optional[Dict[str, Any]] = None
	brightness: Optional[float] = None
	hue: Optional[float] = None
	saturation: Optional[float] = None


class EthernetResponse(BaseModel):
	connected: Optional[bool] = None
	enabled: Optional[bool] = None


class WifiResponse(BaseModel):
	connected: Optional[bool] = None
	enabled: Optional[bool] = None
	mode: Optional[str] = None
	ssid: Optional[str] = None


class NetworkResponse(BaseModel):
	ethernet: Optional[EthernetResponse] = None
	wifi: Optional[WifiResponse] = None
	wifi_networks: Optional[List[Any]] = None


class StatusRequest(BaseModel):
	status: str = Field(...)


class StatusResponse(BaseModel):
	status: str


class PrinterResponse(BaseModel):
	bed: Optional[BedResponse] = None
	diagnostics: Optional[Dict[str, Any]] = None
	headS: Optional[List[HeadResponse]] = Field(default=None, alias='heads')
	led: Optional[LedResponse] = None
	network: Optional[NetworkResponse] = None
	status: Optional[str] = None
	validate_header: Optional[Dict[str, Any]] = None
	serial_number: Optional[str] = None
