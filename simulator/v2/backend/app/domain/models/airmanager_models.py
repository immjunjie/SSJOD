from pydantic import BaseModel
from typing import List, Optional, Dict, Literal

"""
Objectives

AirManager {
    firmware_version (string, optional): Version of the installed firmware ,
    filter_age (number, optional): Filter hours used ,
    filter_max_age (number, optional): Lifespan of the filter in hours ,
    filter_status (string, optional): Indicate the status of the Air Manager filter = ['unknown', 'peak_performance', 'replacement_near', 'replacement_required', 'missing'],
    status (string, optional): Indicate the status of the Air Manager device = ['error', 'unavailable', 'available', 'installing_firmware'],
    fan_speed (number, optional): Speed of the fan in revolutions per minute
"""

class AirManagerModel(BaseModel):
    firmware_version: Optional[str] = None  # Version of the installed firmware
    filter_age: Optional[int] = None  # Filter hours used
    filter_max_age: Optional[int] = None  # Lifespan of the filter in hours
    filter_status: Optional[str] = None  # Status of the Air Manager filter
    status: Optional[str] = None  # Status of the Air Manager device
    fan_speed: Optional[int] = None  # Speed of the fan in revolutions per minute