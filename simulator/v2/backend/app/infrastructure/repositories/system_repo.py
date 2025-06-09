from typing import List
from simulator.v2.backend.app.domain.models.system_models import SystemModel,SystemHardwareModel,SystemTimeModel,SystemMemoryModel
import logging

system_logger = logging.getLogger(__name__)

class SystemRepo:
    """
    Repository for managing system information.

    Insert DataModel Example:  
    {
        "country": "",
        "display_message": {},
        "firmware": "8.2.0",
        "guid": "4b0fc38e-95e3-436c-aa7e-0f57442aac63",
        "hardware": {
            "revision": 2,
            "typeid": 214476
        },  
        "hostname": "ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63",
        "is_country_locked": false,
        "language": "en",
        "log": [
            "Jun 09 10:30:06 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<923e604c-8432-4b09-96aa-9bbbd42207f4>(Generic BVOH Generic) - diameter: 1.750000, density: 1.140000 with MaterialProfile<923e604c-8432-4b09-96aa-9bbbd42207f4>(Generic BVOH Generic) - diameter: 1.750000, density: 1.140000",
            "Jun 09 10:30:16 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<a468d86a-220c-47eb-99a5-bbb47e514eb0>(Generic HIPS Generic) - diameter: 1.750000, density: 1.240000 with MaterialProfile<a468d86a-220c-47eb-99a5-bbb47e514eb0>(Generic HIPS Generic) - diameter: 1.750000, density: 1.240000",
            "Jun 09 10:30:18 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<07a4547f-d21f-41a0-8eee-bc92125221b3>(Ultimaker TPU 95A Red) - diameter: 2.850000, density: 1.220000 with MaterialProfile<07a4547f-d21f-41a0-8eee-bc92125221b3>(Ultimaker TPU 95A Red) - diameter: 2.850000, density: 1.220000",
            "Jun 09 10:30:22 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<c8394116-30ba-4112-b4d9-8b2394278cb3>(Ultimaker PETG Gray) - diameter: 2.850000, density: 1.270000 with MaterialProfile<c8394116-30ba-4112-b4d9-8b2394278cb3>(Ultimaker PETG Gray) - diameter: 2.850000, density: 1.270000",
            "Jun 09 10:30:25 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<61eb5c6c-0110-49de-9756-13b8c7cc2ff1>(Ultimaker PETG White) - diameter: 2.850000, density: 1.270000 with MaterialProfile<61eb5c6c-0110-49de-9756-13b8c7cc2ff1>(Ultimaker PETG White) - diameter: 2.850000, density: 1.270000",
            "Jun 09 10:30:26 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<b6f76172-bb0f-4326-bdbc-ee8f0e84b283>(Generic HIPS Generic) - diameter: 2.850000, density: 1.240000 with MaterialProfile<b6f76172-bb0f-4326-bdbc-ee8f0e84b283>(Generic HIPS Generic) - diameter: 2.850000, density: 1.240000",
            "Jun 09 10:30:27 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<0b4ca6ef-eac8-4b23-b3ca-5f21af00e54f>(Ultimaker ABS Orange) - diameter: 2.850000, density: 1.100000 with MaterialProfile<0b4ca6ef-eac8-4b23-b3ca-5f21af00e54f>(Ultimaker ABS Orange) - diameter: 2.850000, density: 1.100000",
            "Jun 09 10:30:28 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<e2409626-b5a0-4025-b73e-b58070219259>(Generic CPE+ Generic) - diameter: 2.850000, density: 1.180000 with MaterialProfile<e2409626-b5a0-4025-b73e-b58070219259>(Generic CPE+ Generic) - diameter: 2.850000, density: 1.180000",
            "Jun 09 10:30:39 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<5df7afa6-48bd-4c19-b314-839fe9f08f1f>(Ultimaker ABS Red) - diameter: 2.850000, density: 1.100000 with MaterialProfile<5df7afa6-48bd-4c19-b314-839fe9f08f1f>(Ultimaker ABS Red) - diameter: 2.850000, density: 1.100000",
            "Jun 09 10:30:40 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<da1872c1-b991-4795-80ad-bdac0f131726>(Generic CPE Generic) - diameter: 1.750000, density: 1.270000 with MaterialProfile<da1872c1-b991-4795-80ad-bdac0f131726>(Generic CPE Generic) - diameter: 1.750000, density: 1.270000",
            "Jun 09 10:30:42 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<6a2573e6-c8ee-4c66-8029-3ebb3d5adc5b>(Ultimaker TPU 95A White) - diameter: 2.850000, density: 1.220000 with MaterialProfile<6a2573e6-c8ee-4c66-8029-3ebb3d5adc5b>(Ultimaker TPU 95A White) - diameter: 2.850000, density: 1.220000",
            "Jun 09 10:30:45 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<1cbfaeb3-1906-4b26-b2e7-6f777a8c197a>(Generic PETG Generic) - diameter: 2.850000, density: 1.270000 with MaterialProfile<1cbfaeb3-1906-4b26-b2e7-6f777a8c197a>(Generic PETG Generic) - diameter: 2.850000, density: 1.270000",
            "Jun 09 10:30:47 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<98c05714-bf4e-4455-ba27-57d74fe331e4>(Generic PC Generic) - diameter: 2.850000, density: 1.190000 with MaterialProfile<98c05714-bf4e-4455-ba27-57d74fe331e4>(Generic PC Generic) - diameter: 2.850000, density: 1.190000",
            "Jun 09 10:30:50 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<283d439a-3490-4481-920c-c51d8cdecf9c>(Generic Nylon Generic) - diameter: 1.750000, density: 1.140000 with MaterialProfile<283d439a-3490-4481-920c-c51d8cdecf9c>(Generic Nylon Generic) - diameter: 1.750000, density: 1.140000",
            "Jun 09 10:30:51 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<bd0d9eb3-a920-4632-84e8-dcd6086746c5>(Ultimaker CPE Transparent) - diameter: 2.850000, density: 1.270000 with MaterialProfile<bd0d9eb3-a920-4632-84e8-dcd6086746c5>(Ultimaker CPE Transparent) - diameter: 2.850000, density: 1.270000",
            "Jun 09 10:30:52 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<fe15ed8a-33c3-4f57-a2a7-b4b78a38c3cb>(Ultimaker PVA Natural) - diameter: 2.850000, density: 1.230000 with MaterialProfile<fe15ed8a-33c3-4f57-a2a7-b4b78a38c3cb>(Ultimaker PVA Natural) - diameter: 2.850000, density: 1.230000",
            "Jun 09 10:30:53 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<6660eb2e-aa40-49ad-ac9b-ada979f3de9b>(Ultimaker Tough PLA Gray) - diameter: 2.850000, density: 1.240000 with MaterialProfile<6660eb2e-aa40-49ad-ac9b-ada979f3de9b>(Ultimaker Tough PLA Gray) - diameter: 2.850000, density: 1.240000",
            "Jun 09 10:30:54 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<c8639119-5cae-4f56-9bcf-3bb00e8225fd>(Ultimaker PETG Red Translucent) - diameter: 2.850000, density: 1.270000 with MaterialProfile<c8639119-5cae-4f56-9bcf-3bb00e8225fd>(Ultimaker PETG Red Translucent) - diameter: 2.850000, density: 1.270000",
            "Jun 09 10:30:58 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<62414577-94d1-490d-b1e4-7ef3ec40db02>(Generic PC Generic) - diameter: 1.750000, density: 1.190000 with MaterialProfile<62414577-94d1-490d-b1e4-7ef3ec40db02>(Generic PC Generic) - diameter: 1.750000, density: 1.190000",
            "Jun 09 10:31:01 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<4b049931-6ee9-408c-8588-ddd4673467d1>(Ultimaker Tough PLA Blue) - diameter: 2.850000, density: 1.240000 with MaterialProfile<4b049931-6ee9-408c-8588-ddd4673467d1>(Ultimaker Tough PLA Blue) - diameter: 2.850000, density: 1.240000",
            "Jun 09 10:31:02 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: ERR - materialDatabase:97 - invalid literal for int() with base 16: '17668dfbeb1c46a5a513bdb7c06959p3'",
            "Jun 09 10:31:03 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<64d44410-be10-428c-8891-f0ae47ea1734>(Generic PET CF Generic) - diameter: 2.850000, density: 1.280000 with MaterialProfile<64d44410-be10-428c-8891-f0ae47ea1734>(Generic PET CF Generic) - diameter: 2.850000, density: 1.390000",
            "Jun 09 10:31:04 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<a6f8d4f1-7205-40cc-b9e5-3bad20bc8011>(Ultimaker PET CF Black) - diameter: 2.850000, density: 1.280000 with MaterialProfile<a6f8d4f1-7205-40cc-b9e5-3bad20bc8011>(Ultimaker PET CF Black) - diameter: 2.850000, density: 1.330000",
            "Jun 09 10:31:07 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<40a273c6-0e15-4db5-a278-8eb0b4a9e293>(Ultimaker PETG Silver) - diameter: 2.850000, density: 1.270000 with MaterialProfile<40a273c6-0e15-4db5-a278-8eb0b4a9e293>(Ultimaker PETG Silver) - diameter: 2.850000, density: 1.270000",
            "Jun 09 10:31:08 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<98896281-3972-4dc5-8d6d-76ed417b10ea>(Ultimaker PET CF Gray) - diameter: 2.850000, density: 1.280000 with MaterialProfile<98896281-3972-4dc5-8d6d-76ed417b10ea>(Ultimaker PET CF Gray) - diameter: 2.850000, density: 1.450000",
            "Jun 09 10:31:09 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<3ee70a86-77d8-4b87-8005-e4a1bc57d2ce>(Ultimaker PLA Black) - diameter: 2.850000, density: 1.240000 with MaterialProfile<3ee70a86-77d8-4b87-8005-e4a1bc57d2ce>(Ultimaker PLA Black) - diameter: 2.850000, density: 1.240000",
            "Jun 09 10:31:11 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<c64c2dbe-5691-4363-a7d9-66b2dc12837f>(Ultimaker Nylon Black) - diameter: 2.850000, density: 1.140000 with MaterialProfile<c64c2dbe-5691-4363-a7d9-66b2dc12837f>(Ultimaker Nylon Black) - diameter: 2.850000, density: 1.140000",
            "Jun 09 10:31:13 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<532e8b3d-5fd4-4149-b936-53ada9bd6b85>(Ultimaker PLA Transparent) - diameter: 2.850000, density: 1.240000 with MaterialProfile<532e8b3d-5fd4-4149-b936-53ada9bd6b85>(Ultimaker PLA Transparent) - diameter: 2.850000, density: 1.240000",
            "Jun 09 10:31:17 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<2db25566-9a91-4145-84a5-46c90ed22bdf>(Ultimaker Tough PLA Red) - diameter: 2.850000, density: 1.240000 with MaterialProfile<2db25566-9a91-4145-84a5-46c90ed22bdf>(Ultimaker Tough PLA Red) - diameter: 2.850000, density: 1.240000",
            "Jun 09 10:31:20 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<12f41353-1a33-415e-8b4f-a775a6c70cc6>(Generic CPE Generic) - diameter: 2.850000, density: 1.270000 with MaterialProfile<12f41353-1a33-415e-8b4f-a775a6c70cc6>(Generic CPE Generic) - diameter: 2.850000, density: 1.270000",
            "Jun 09 10:31:21 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<e92b1f0b-a069-4969-86b4-30127cfb6f7b>(Ultimaker PC Black) - diameter: 2.850000, density: 1.190000 with MaterialProfile<e92b1f0b-a069-4969-86b4-30127cfb6f7b>(Ultimaker PC Black) - diameter: 2.850000, density: 1.190000",
            "Jun 09 10:31:22 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<5f9f3de0-045b-48d9-84ec-19db92be7603>(Ultimaker PETG Black) - diameter: 2.850000, density: 1.270000 with MaterialProfile<5f9f3de0-045b-48d9-84ec-19db92be7603>(Ultimaker PETG Black) - diameter: 2.850000, density: 1.270000",
            "Jun 09 10:31:30 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<a02a3978-eb33-47ca-b32b-d08b92b58638>(Ultimaker PETG Orange) - diameter: 2.850000, density: 1.270000 with MaterialProfile<a02a3978-eb33-47ca-b32b-d08b92b58638>(Ultimaker PETG Orange) - diameter: 2.850000, density: 1.270000",
            "Jun 09 10:31:32 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<2433b8fb-dcd6-4e36-9cd5-9f4ee551c04c>(Ultimaker PLA Green) - diameter: 2.850000, density: 1.240000 with MaterialProfile<2433b8fb-dcd6-4e36-9cd5-9f4ee551c04c>(Ultimaker PLA Green) - diameter: 2.850000, density: 1.240000",
            "Jun 09 10:37:48 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 StardustService[1850]: INF - stardust:126 - Connection to the gateway is closed",
            "Jun 09 10:37:48 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 StardustService[1850]: INF - stardust.StardustWebsocketThread:129 - Connection stopped working; fail_reason: ConnectionFailReason.connection_broke",
            "Jun 09 10:37:50 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 StardustService[1850]: INF - stardust.StardustService:49 - 'startCloudConnection' command received on DBus with cluster_id 'QaIGxtYhdvd2F2s48HtdZlSWC2Ge0VDzBRgLcPKtmj8W'",
            "Jun 09 10:37:50 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 StardustService[1850]: INF - stardust.StardustApplication:172 - Starting websocket connection with Ultimaker cloud",
            "Jun 09 10:37:53 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 StardustService[1850]: INF - stardust.StardustService:49 - 'startCloudConnection' command received on DBus with cluster_id 'QaIGxtYhdvd2F2s48HtdZlSWC2Ge0VDzBRgLcPKtmj8W'",
            "Jun 09 10:37:53 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 StardustService[1850]: INF - stardust.StardustApplication:172 - Starting websocket connection with Ultimaker cloud",
            "Jun 09 10:37:53 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 StardustService[1850]: INF - stardust.StardustWebsocketThread:127 - StardustWebsocketThread is opening the websocket connection",
            "Jun 09 10:37:53 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 StardustService[1850]: INF - stardust:176 - Stardust configuration: ID=QaIGxtYhdvd2F2s48HtdZlSWC2Ge0VDzBRgLcPKtmj8W, host_guid=4b0fc38e-95e3-436c-aa7e-0f57442aac63, capabilities: ['connect_with_cluster_id', 'connect_with_pin_code', 'group', 'identify', 'import_material', 'print_job_action_duplicate', 'print_job_action_reprint', 'print_job_action_response', 'print_job_action', 'print_job_recent_history', 'printer_action_response', 'printer_action', 'printer_faults', 'queue', 'rename', 'schedule', 'set_availability', 'status', 'update_firmware', 'webcam_snapshot', 'cluster_account_status', 'firewall', 'pin_code_lock', 'firmware_channel']",
            "Jun 09 10:37:53 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 StardustService[1850]: INF - stardust:33 - Attempting to connect to wss://api.ultimaker.com:443/gateway/v1/socket",
            "Jun 09 10:37:53 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 StardustService[1850]: INF - stardust:54 - WebSocket connection opened",
            "Jun 09 10:37:53 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 StardustService[1850]: INF - stardust:112 - Opening connection to the Gateway",
            "Jun 09 10:37:53 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 StardustService[1850]: INF - stardust:280 - Reconnection confirmed with ID QaIGxtYhdvd2F2s48HtdZlSWC2Ge0VDzBRgLcPKtmj8W.",
            "Jun 09 10:37:53 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 StardustService[1850]: INF - stardust:487 - Received Digital Factory account information. user_id: buMym6WLc2JIjEg7wPi03bYVHGV7NQ5R0gFDx0odjUrm, organization_id: None",
            "Jun 09 10:37:53 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 Okuda[28793]: INFO     Okuda.DBus.stardustServiceProxy StardustServiceProxy cloud account changed: user_id = buMym6WLc2JIjEg7wPi03bYVHGV7NQ5R0gFDx0odjUrm",
            "Jun 09 10:37:56 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 PrintClusterServer[3676]: INF - app.services.access_control.cloud_access_control_backend:385 - Updating cluster_id from startdust DBus to 'QaIGxtYhdvd2F2s48HtdZlSWC2Ge0VDzBRgLcPKtmj8W'",
            "Jun 09 10:37:56 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 PrintClusterServer[3676]: INF - app.services.access_control.cloud_access_control_backend:389 - Entering state ConnectionState.connected"
        ],
        "memory": {
            "total": 1053614080,
            "used": 678916096
        },
        "name": "Ultimaker-2aac63",
        "platform": "Linux-4.14.32-ultimaker+-armv7l-with-debian-10.1",
        "time": {
            "utc": 1749465947.1309733
        },
        "type": "3D printer",
        "uptime": 11474649,
        "variant": "Ultimaker S5"
    }
    """
    def __init__(self) -> None:
        self.system_info: SystemModel = SystemModel(
            country="",
            display_message={},
            firmware="8.2.0",
            guid="4b0fc38e-95e3-436c-aa7e-0f57442aac63",
            hardware=SystemHardwareModel(
                revision=2,
                typeid=214476
            ),
            hostname="ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63",
            is_country_locked=False,
            language="en",
            log=[
                "Jun 09 10:30:06 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<923e604c-8432-4b09-96aa-9bbbd42207f4>(Generic BVOH Generic) - diameter: 1.750000, density: 1.140000 with MaterialProfile<923e604c-8432-4b09-96aa-9bbbd42207f4>(Generic BVOH Generic) - diameter: 1.750000, density: 1.140000",
                "Jun 09 10:30:16 ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63 MaterialService[449]: WAR - materialDatabase:371 - Refused to overrule the internal material profile MaterialProfile<a468d86a-220c-47eb-99a5-bbb47e514eb0>(Generic HIPS Generic) - diameter: 1.750000, density: 1.240000 with MaterialProfile<a468d86a-220c-47eb-99a5-bbb47e514eb0>(Generic HIPS Generic) - diameter: 1.750000, density: 1.240000",
                # ... other log entries
            ],
            memory=SystemMemoryModel(
                total=1053614080,
                used=678916096
            ),
            name="Ultimaker-2aac63",
            platform="Linux-4.14.32-ultimaker+-armv7l-with-debian-10.1",
            time=SystemTimeModel(utc=1749465947.1309733),
            type="3D printer",
            uptime=11474649,
            variant="Ultimaker S5"
        )

    async def get_system(self) -> SystemModel:
        system_logger.debug("Retrieving system information.")
        return self.system_info

    # create a new system log
    async def create_system_log(self, log_entry: str) -> None:
        system_logger.debug("Adding log entry: %s", log_entry)
        self.system_info.log.append(log_entry)
        system_logger.debug("Log entry added successfully.")
        return log_entry