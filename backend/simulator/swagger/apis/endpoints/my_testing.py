from fastapi import APIRouter
from pydantic import BaseModel

route = APIRouter()

class AuthResponse(BaseModel):
    message: str

@route.get("/auth/check/{id}", tags=["Authentication"], response_model=AuthResponse)
def get_auth_check_by_id():
    return AuthResponse(message="authorized")

@route.get("/auth/verify", tags=["Authentication"], response_model=AuthResponse)
def get_auth_verify():
    return AuthResponse(message="ok")

if __name__ == "__main__":
    m1 = get_auth_check_by_id()
    m2 = get_auth_verify()
    print(m1.model_dump_json())
    print(m2.model_dump_json())