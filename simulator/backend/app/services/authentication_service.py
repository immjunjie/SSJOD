from pydantic import BaseModel
from simulator.backend.app.domain.models.authentication_gen import AuthDataGenerator

class AuthResponse(BaseModel):
    message: str

class AuthService:
    def __init__(self):
        self.printer_memory = AuthDataGenerator()

    def get_message_check_by_id(self) -> AuthResponse:
        return AuthResponse(message=self.printer_memory.get_message_check_by_id())

    def get_message_auth_verify(self) -> AuthResponse:
        return AuthResponse(message=self.printer_memory.get_message_auth_verify())


if __name__ == "__main__":
    service = AuthService()
    print("Test check_by_id:", service.get_message_check_by_id().model_dump_json())
    print("Test verify:", service.get_message_auth_verify().model_dump_json())