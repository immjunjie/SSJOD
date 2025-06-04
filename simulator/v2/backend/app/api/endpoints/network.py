from fastapi import APIRouter, Depends, HTTPException
from simulator.v2.backend.app.domain.models.network_models import Network
from simulator.v2.backend.app.services.network_service import NetworkService
from simulator.v2.backend.app.infrastructure.repositories.network_repo import NetworkRepo
import logging

network_logger = logging.getLogger(__name__)
router = APIRouter()

def get_network_repo() -> NetworkRepo:
    """
    Dependency to provide NetworkRepo instance.
    """
    network_logger.debug("Creating new NetworkRepo instance.")
    return NetworkRepo()

def get_network_service(repo: NetworkRepo = Depends(get_network_repo)) -> NetworkService:
    """
    Dependency to provide NetworkService instance.
    """
    network_logger.debug("Creating new NetworkService instance.")
    return NetworkService(network_repository=repo)

@router.get("/network", response_model=Network, tags=["Network"])
async def get_network(service: NetworkService = Depends(get_network_service)):
    """
    Retrieve current network configuration.

    Returns:
        Network: The current network configuration including ethernet, wifi, and wifi networks.

    Raises:
        HTTPException: If an error occurs while fetching the network configuration.
    """
    try:
        network_logger.debug("Request received to fetch network configuration.")
        network = await service.get_network()
        network_logger.debug("Network configuration fetched successfully: %s", network)
        return network
    except Exception as e:
        network_logger.error("Error fetching network configuration: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.patch("/network", response_model=Network, tags=["Network"])
async def update_network(network: Network, service: NetworkService = Depends(get_network_service)):
    """
    Update the current network configuration.

    Args:
        network: The new network configuration to apply.

    Returns:
        Network: The updated network configuration.

    Raises:
        HTTPException: If an error occurs while updating the network configuration.
    """
    try:
        network_logger.debug("Request received to update network configuration: %s", network)
        updated_network = await service.update_network(network)
        network_logger.debug("Network configuration updated successfully: %s", updated_network)
        return updated_network
    except ValueError as ve:
        network_logger.error("Validation error: %s", ve)
        raise HTTPException(status_code=400, detail=f"Invalid network data: {str(ve)}")
    except Exception as e:
        network_logger.error("Error updating network configuration: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")