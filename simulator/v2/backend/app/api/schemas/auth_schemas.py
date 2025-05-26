from pydantic import BaseModel
# from typing import Dict, List, Any, Literal

class AuthCheckResponse(BaseModel):
    message: str

class AuthVerifyResponse(BaseModel):
    message: str