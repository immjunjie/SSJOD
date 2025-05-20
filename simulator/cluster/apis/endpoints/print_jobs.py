from fastapi import APIRouter

router = APIRouter()

@router.get("/print_jobs", tags=["print_jobs"], summary="Return a list of all current print jobs in the queuue")
def get_print_jobs():
    """myDescription"""
    return {"jobs": ["Job1", "Job2"]}

@router.get("/print_jobs/history/recently_completed", tags=["print_jobs"])
def get_print_jobs_history_recently_completed():
    """myDescription"""
    return {"Message": "mySuccessful"}

@router.get("/print_jobs/printing", tags=["print_jobs"], summary="Return a list of all started print jobs")
def get_print_jobs_printing():
    """myDescription"""
    return {"Message": "mySuccessful"}

@router.get("/print_jobs/queued", tags=["print_jobs"], summary="Return a list of all queued print jobs")
def get_print_jobs_queued():
    """myDescription"""
    return {"Message": "mySuccessful"}

