from fastapi import APIRouter

router = APIRouter()

@router.get("/print_job", tags=["PrintJob"])
def get_print_job():
    status = True
    if status:
        # return {"Message": "mySuccessful"}
        pass
    return []