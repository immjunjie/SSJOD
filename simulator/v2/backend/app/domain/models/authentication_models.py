from pydantic import BaseModel
from typing import Optional

"""
Objectives

authentication_verify_model {
    message (string, optional) = ['ok']
}
"""

class AuthenticationVerifyModel(BaseModel):
    message: Optional[str] = 'ok'  # Message indicating the result of the verification, default is 'ok'