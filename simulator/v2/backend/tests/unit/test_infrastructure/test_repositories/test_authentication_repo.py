import pytest
from simulator.v2.backend.app.infrastructure.repositories.authentication_repo import AuthenticationRepository
from simulator.v2.backend.app.domain.models.authentication_models import AuthenticationVerifyModel

@pytest.mark.asyncio
async def test_verify_authentication():
    """
    Test the verify_authentication method of AuthenticationRepository.
    """
    repo = AuthenticationRepository()
    result = await repo.verify_authentication()

    # Check if the result is an instance of AuthenticationVerifyModel
    assert isinstance(result, AuthenticationVerifyModel)

    # Check if the message is 'ok'
    assert result.message == 'ok'