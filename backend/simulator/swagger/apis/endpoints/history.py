from fastapi import APIRouter

router = APIRouter()

@router.get("/history/print_jobs", tags=["History"])
def get_history_print_jobs():
    return {"Message": "mySuccessful"}
