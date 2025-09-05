from pydantic import BaseModel

"""
Objectives

Camera {
    feed (string)
}
"""

class CameraModel(BaseModel):
    feed: str