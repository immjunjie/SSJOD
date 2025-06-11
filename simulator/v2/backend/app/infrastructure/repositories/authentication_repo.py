from simulator.v2.backend.app.domain.models.authentication_models import AuthenticationVerifyModel
import logging

auth_logger = logging.getLogger(__name__)

class AuthenticationRepository:
    def __init__(self):
        """
        Repository for handling authentication verification.
        """
        self._authentication_verify = AuthenticationVerifyModel()

    async def verify_authentication(self) -> AuthenticationVerifyModel:
        """
        Verifies the authentication and returns a model indicating the result.

        Returns:
            AuthenticationVerifyModel: Model containing the verification message.
        """
        auth_logger.debug(self._authentication_verify)
        return self._authentication_verify