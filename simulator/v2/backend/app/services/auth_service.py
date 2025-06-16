from simulator.v2.backend.app.domain.models.authentication_models import AuthenticationVerifyModel
from simulator.v2.backend.app.infrastructure.repositories.authentication_repo import AuthenticationRepository
import logging

auth_logger = logging.getLogger(__name__)

class AuthService:
    """
    Service for handling authentication-related operations.
    """
    def __init__(self, auth_repository: AuthenticationRepository):
        """
        Initializes the AuthService with a repository.
        """
        self.auth_repo = auth_repository
        auth_logger.debug("AuthService initialized with repository: %s", auth_repository)

    async def get_authentication_verify(self) -> AuthenticationVerifyModel:
        """
        Retrieves the authentication verification information.
        """
        auth_logger.debug("AuthService retrieving authentication verification info")
        auth_verify = await self.auth_repo.verify_authentication()
        auth_logger.debug("Authentication verification retrieved: %s", auth_verify)
        return auth_verify