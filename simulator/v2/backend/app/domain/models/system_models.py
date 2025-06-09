from pydantic import BaseModel
from typing import List, Optional, Dict

"""
Objectives

system_time {
    utc (number, optional): Number of seconds since the Unix Epoch
}
system_memory {
    total (integer, optional): in bytes ,
    used (integer, optional): in bytes
}
system_hardware {
    typeid (integer, optional),
    revision (integer, optional)
}
System {
    name (string, optional),
    platform (string, optional),
    hostname (string, optional),
    firmware (string, optional),
    country (string, optional),
    language (string, optional),
    uptime (integer, optional),
    time (system_time, optional),
    type (string, optional),
    variant (string, optional),
    memory (system_memory, optional),
    hardware (system_hardware, optional),
    log (string, optional),
    guid (string, optional)
}
"""

class SystemTimeModel(BaseModel):
    utc: Optional[float] = None  # Number of seconds since the Unix Epoch

class SystemMemoryModel(BaseModel):
    total: Optional[int] = None  # Total memory in bytes
    used: Optional[int] = None   # Used memory in bytes

class SystemHardwareModel(BaseModel):
    typeid: Optional[int] = None  # Hardware type ID
    revision: Optional[int] = None  # Hardware revision ID

class SystemModel(BaseModel):
    name: Optional[str] = None
    platform: Optional[str] = None
    hostname: Optional[str] = None
    firmware: Optional[str] = None
    country: Optional[str] = None
    display_message: Optional[Dict] = None  # Display message for the system
    is_country_locked: Optional[bool] = None  # Indicates if the system is country locked
    language: Optional[str] = None
    uptime: Optional[int] = None  # Uptime in seconds
    time: Optional[SystemTimeModel] = None
    type: Optional[str] = None
    variant: Optional[str] = None
    memory: Optional[SystemMemoryModel] = None
    hardware: Optional[SystemHardwareModel] = None
    log: Optional[List] = None
    guid: Optional[str] = None  # Unique identifier for the system