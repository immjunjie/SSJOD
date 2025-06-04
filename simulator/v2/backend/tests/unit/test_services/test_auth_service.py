import pytest
from simulator.v2.backend.app.domain.models.authentication_models import Check, Verify
from simulator.v2.backend.app.infrastructure.repositories.authentication_repo import AuthenticationRepository
from simulator.v2.backend.app.services.auth_service import AuthService

@pytest.mark.asyncio
async def test_get_message_check_by_id_returns_check():
    # Arrange
    auth_service = AuthService(AuthenticationRepository())

    # Act
    result = await auth_service.get_message_check_by_id()

    # Assert
    assert isinstance(result, Check)
    assert result.message == "authorized"

@pytest.mark.asyncio
async def test_get_message_auth_verify_returns_verify():
    # Arrange
    auth_service = AuthService(AuthenticationRepository())

    # Act
    result = await auth_service.get_message_auth_verify()

    # Assert
    assert isinstance(result, Verify)
    assert result.message == "authorized"