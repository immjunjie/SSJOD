from fastapi import APIRouter

router = APIRouter()

@router.get("/debug/match_matrix/{nr}", tags=["debug"], summary="Shows a list of all the last job <-> printer matcher from the scheduler")
def get_debug_match_matrix():
    """myDescription"""
    return {"Message": "mySuccessful"}

@router.get("/debug/schedule/{nr}", tags=["debug"], summary="Shows a list of all the last job <-> printer matcher from the scheduler")
def get_debug_schedule():
    """myDescription"""
    return {"Message": "mySuccessful"}

