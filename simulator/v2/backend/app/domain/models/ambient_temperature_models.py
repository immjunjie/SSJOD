from pydantic import BaseModel
from typing import Optional

"""
Objectives

ambient_temperature_model {
    current: float (optional)  # Current ambient temperature in degrees Celsius
}
"""

class AmbientTemperatureModel(BaseModel):
    current: Optional[float] = None  # Current ambient temperature in degrees Celsius