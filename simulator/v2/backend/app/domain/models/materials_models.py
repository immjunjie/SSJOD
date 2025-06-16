from pydantic import BaseModel
from typing import List

"""
Objectives

MaterialsModel [
    string
]
"""

class MaterialsModel(BaseModel):
    materials: List[str] = []  # List of materials