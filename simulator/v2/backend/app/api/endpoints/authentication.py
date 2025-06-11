from fastapi import APIRouter, Depends, HTTPException
from simulator.v2.backend.app.domain.models.authentication_models import AuthenticationVerifyModel
from simulator.v2.backend.app.infrastructure.repositories.authentication_repo import AuthenticationRepository
from simulator.v2.backend.app.services.auth_service import AuthService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

_auth_repo = AuthenticationRepository()
_auth_service = AuthService(auth_repository=_auth_repo)

def get_material_repo():
    return _auth_repo

def get_auth_service():
    return _auth_service

@router.get("/auth/verify", response_model=AuthenticationVerifyModel, tags=["Authentication"])
async def get_message_auth_verify(service: AuthService = Depends(get_auth_service)):
    """
    Verify the authorization status of the application.
    """
    try:
        logger.debug("Handling /auth/verify request")
        verify = await service.get_authentication_verify()
        logger.info(f"Authorization verify response: {verify}")
        return verify
    except Exception as e:
        logger.error(f"Error fetching authorization verify: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

