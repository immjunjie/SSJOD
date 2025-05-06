from fastapi import APIRouter

router = APIRouter()

@router.get("/printers", tags=["printers"], summary="Return a list of all the connected printers")
def get_a_list_of_all_the_connected_printers():
    """myDescription"""
    return {"Message": "mySuccessful"}