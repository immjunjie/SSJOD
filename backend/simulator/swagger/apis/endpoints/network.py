from fastapi import APIRouter

router = APIRouter()

@router.get("/printer/network", tags=["Network"])
def get_printer_network():
    message = {
      "wifi": {
        "connected": True,
        "enabled": True,
        "mode": "AUTO",
        "ssid": "string"
      },
      "wifi_networks": [
        {
          "ssid": "string",
          "security_required": True,
          "strength": 0
        }
      ],
      "ethernet": {
        "connected": True,
        "enabled": True
      }
    }
    return message

@router.get("/printer/network/wifi_networks", tags=["Network"])
def get_printer_network_wifi_networks():
    return {"Message": "mySuccessful"}