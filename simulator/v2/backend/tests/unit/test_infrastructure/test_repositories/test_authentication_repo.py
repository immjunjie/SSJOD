import pytest
from simulator.v2.backend.app.infrastructure.repositories.authentication_repo import AuthenticationRepository
from simulator.v2.backend.app.domain.models.authentication_models import Check, Verify

@pytest.mark.asyncio
async def test_get_check_by_id_returns_check():
    repo = AuthenticationRepository()
    result = await repo.get_check_by_id()
    assert isinstance(result, Check)
    assert result.message == "authorized"

@pytest.mark.asyncio
async def test_get_auth_verify_returns_verify():
    repo = AuthenticationRepository()
    result = await repo.get_auth_verify()
    assert isinstance(result, Verify) 
    assert result.message == "authorized"