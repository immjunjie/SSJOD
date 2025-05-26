from simulator.v2.backend.app.domain.models.authentication_models import Check, Verify
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class AuthenticationRepository:
    def __init__(self):
        self.data: Dict[str, Any] = {
            "check": Check(message="authorized"),
            "verify": Verify(message="authorized")
        }

    async def get_check_by_id(self) -> Check:
        logger.debug("Fetching check by ID")
        return self.data["check"]

    async def get_auth_verify(self) -> Verify:
        logger.debug("Fetching auth verify")
        return self.data["verify"]