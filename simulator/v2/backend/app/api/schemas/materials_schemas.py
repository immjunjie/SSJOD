from pydantic import BaseModel
from typing import List

class MaterialListResponse(BaseModel):
    materials: List[str]