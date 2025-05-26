from fastapi import APIRouter, Depends, HTTPException
from simulator.v2.backend.app.api.schemas.auth_schemas import AuthCheckResponse
from simulator.v2.backend.app.services.auth_service import AuthService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

_auth_service = AuthService()


def get_auth_service():
    """
    Dependency to provide the AuthService instance.
    """
    return _auth_service


@router.get("/auth/check", response_model=AuthCheckResponse, tags=["Authentication"])
async def get_message_check_by_id(service: AuthService = Depends(get_auth_service)):
    """
    Get the authorization status of the application.
    """
    try:
        logger.debug("Handling /auth/check request")

        check = await service.get_message_check_by_id()

        logger.info(f"Authorization check response: {check.message}")
        return AuthCheckResponse(message=check.message)
    except Exception as e:
        logger.error(f"Error fetching authorization check: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/auth/verify", response_model=AuthCheckResponse, tags=["Authentication"])
async def get_message_auth_verify(service: AuthService = Depends(get_auth_service)):
    """
    Verify the authorization status of the application.
    """
    try:
        logger.debug("Handling /auth/verify request")

        verify = await service.get_message_auth_verify()

        logger.info(f"Authorization verify response: {verify.message}")
        return AuthCheckResponse(message=verify.message)
    except Exception as e:
        logger.error(f"Error fetching authorization verify: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

