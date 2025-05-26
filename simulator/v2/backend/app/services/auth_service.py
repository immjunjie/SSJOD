from simulator.v2.backend.app.domain.models.authentication_models import Check, Verify
from simulator.v2.backend.app.infrastructure.repositories.authentication_repo import AuthenticationRepository
import logging

logger = logging.getLogger(__name__)

class AuthService:
    """
    Service for handling authentication-related operations.
    """
    def __init__(self, printer_repo: AuthenticationRepository = None):
        self.auth_repo = printer_repo or AuthenticationRepository()

    async def get_message_check_by_id(self) -> Check:
        logger.debug("Fetching message check by ID")
        return await self.auth_repo.get_check_by_id()

    async def get_message_auth_verify(self) -> Verify:
        logger.debug("Fetching message auth verify")
        return await self.auth_repo.get_auth_verify()