from pydantic import BaseModel
from typing import List

class WifiNetwork(BaseModel):
    ssid: str
    security_required: bool
    strength: int

class InlineModel(BaseModel):
    connected: bool = False
    enabled: bool = False
    mode: str = "OFFLINE"
    ssid: str = ""

class InlineModel0(BaseModel):
    connected: bool = False
    enabled: bool = False

class Network(BaseModel):
    ethernet: InlineModel0
    wifi: InlineModel
    wifi_networks: List[WifiNetwork] = []