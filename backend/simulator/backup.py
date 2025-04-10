from typing import Union

from fastapi import FastAPI, status, APIRouter
from fastapi.responses import RedirectResponse
# from pydantic import BaseModel

# init
app = FastAPI()



# sub application (routes and documentation) - Ultimaker - Connect API
sub_app = FastAPI(docs_url="/docs")
router = APIRouter()

@router.get("/request_template")
def get_a_request_template():
    return "this is the sample request"

@router.get("/print_jobs")
def get_a_list_of_all_current_print_jobs_in_the_queue():
    status = True
    if status != True:
        return []
    return [
    {
      "uuid": "string",
      "name": "string",
      "created_at": "2025-04-09T09:55:36.733Z",
      "started": True,
      "status": "sent_to_printer",
      "printer_uuid": "string",
      "configuration": [
        {
          "extruder_index": 0,
          "print_core_id": "string",
          "material": {
            "guid": "string",
            "brand": "string",
            "material": "string",
            "color": "string",
            "version": 0,
            "density": 0
          }
        }
      ],
      "machine_variant": "Ultimaker 3",
      "constraints": {
        "require_printer_name": "string"
      },
      "time_elapsed": 0,
      "time_total": 0,
      "last_seen": 0,
      "network_error_count": 0,
      "force": True,
      "assigned_to": "string",
      "owner": "string",
      "build_plate": {
        "type": "string"
      },
      "configuration_changes_required": [
        {
          "type_of_change": "material_change",
          "index": 0,
          "target_id": "string",
          "origin_id": "string",
          "target_name": "string",
          "origin_name": "string"
        }
      ],
      "impediments_to_printing": [
        {
          "translation_key": "string",
          "severity": "string"
        }
      ],
      "compatible_machine_families": [
        "Ultimaker 3"
      ],
      "printed_on_uuid": "string",
      "deleted_at": "2025-04-09T09:55:36.734Z",
      "cloud_job_id": "string"
    }
  ]
 
@router.get("/printers")
def return_a_list_of_all_the_connected_printers():
    return [
    {
        "uuid": "6cf81fcb-e940-41c7-a987-a3b116f7dd77",
        "status": "idle",
        "unique_name": "ultimakersystem-4b0fc38e95e3436caa7e0f57442aac63",
        "ip_address": "143.239.73.224",
        "is_host": True,
        "firmware_version": "8.2.0.0",
        "friendly_name": "Ultimaker-2aac63",
        "enabled": True,
        "reserved_by": None,
        "machine_variant": "Ultimaker S5",
        "build_plate": {
            "type": "glass"
        },
        "air_manager": {
            "supported": True,
            "status": "available",
            "filter_status": "peak_performance",
            "filter_age": 79,
            "filter_max_age": 1500
        },
        "material_station": {
            "supported": True,
            "status": "available",
            "material_slots": [
                {
                    "slot_index": 0,
                    "extruder_index": -1,
                    "print_core_id": None,
                    "material": None,
                    "material_empty": False,
                    "material_remaining": -1.0,
                    "compatible": False
                },
                {
                    "slot_index": 1,
                    "extruder_index": 0,
                    "print_core_id": "AA 0.4",
                    "material": {
                        "guid": "03f24266-0291-43c2-a6da-5211892a2699",
                        "brand": "Ultimaker",
                        "material": "Tough PLA",
                        "color": "Black"
                    },
                    "material_empty": False,
                    "material_remaining": 0.4748180780109531,
                    "compatible": True
                },
                {
                    "slot_index": 2,
                    "extruder_index": -1,
                    "print_core_id": None,
                    "material": None,
                    "material_empty": False,
                    "material_remaining": -1.0,
                    "compatible": False
                },
                {
                    "slot_index": 3,
                    "extruder_index": 1,
                    "print_core_id": "AA 0.4",
                    "material": {
                        "guid": "e509f649-9fe6-4b14-ac45-d441438cb4ef",
                        "brand": "Ultimaker",
                        "material": "PLA",
                        "color": "White"
                    },
                    "material_empty": False,
                    "material_remaining": 1.0,
                    "compatible": True
                },
                {
                    "slot_index": 4,
                    "extruder_index": 1,
                    "print_core_id": "AA 0.4",
                    "material": {
                        "guid": "2433b8fb-dcd6-4e36-9cd5-9f4ee551c04c",
                        "brand": "Ultimaker",
                        "material": "PLA",
                        "color": "Green"
                    },
                    "material_empty": False,
                    "material_remaining": 0.8870093333333333,
                    "compatible": True
                },
                {
                    "slot_index": 5,
                    "extruder_index": -1,
                    "print_core_id": None,
                    "material": None,
                    "material_empty": False,
                    "material_remaining": -1.0,
                    "compatible": False
                }
            ]
        },
        "configuration": [
            {
                "extruder_index": 0,
                "print_core_id": "AA 0.4",
                "material": {
                    "guid": "00000000-0000-0000-0000-000000000000",
                    "brand": "empty",
                    "material": "empty",
                    "color": "empty"
                }
            },
            {
                "extruder_index": 1,
                "print_core_id": "AA 0.4",
                "material": {
                    "guid": "00000000-0000-0000-0000-000000000000",
                    "brand": "empty",
                    "material": "empty",
                    "color": "empty"
                }
            }
        ],
        "maintenance_required": False,
        "firmware_update_status": "update_available",
        "latest_available_firmware": "9.0.2.0",
        "errors": [],
        "faults": []
    }
]

# 
sub_app.include_router(router)

# sub-app loads into the main-app
app.mount("/cluster-api/v1", sub_app)







# main application (routes and documentation) - Swagger UI
@app.get("/")
def read_api_docs():
    return RedirectResponse(url="/cluster-api/v1/docs", status_code=status.HTTP_302_FOUND)
