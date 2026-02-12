from fastapi import APIRouter
from .. import schemas

router = APIRouter()

@router.post("/login")
def login(request: schemas.Login):
    return request