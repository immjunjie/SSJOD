import pytest
from simulator.v2.backend.app.domain.models.authentication_models import AuthenticationVerifyModel
from simulator.v2.backend.app.infrastructure.repositories.authentication_repo import AuthenticationRepository
from simulator.v2.backend.app.services.auth_service import AuthService

@pytest.mark.asyncio
async def test_get_message_auth_verify_returns_verify():
    # Arrange
    auth_service = AuthService(AuthenticationRepository())

    # Act
    result = await auth_service.get_authentication_verify()

    # Assert
    assert isinstance(result, AuthenticationVerifyModel), "Result should be an instance of AuthenticationVerifyModel"
    assert result.message == 'ok', "Message should be 'ok'"