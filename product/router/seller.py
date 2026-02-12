from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from passlib.context import CryptContext

router = APIRouter(
    tags=["Seller"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/seller", response_model=schemas.DisplaySeller)
def create_seller(request: schemas.Seller, db: Session = Depends(get_db)):
    hashed_pwd = pwd_context.hash(request.password)
    get_seller = models.Seller(username=request.username, email=request.email, password=hashed_pwd)
    db.add(get_seller)
    db.commit()
    db.refresh(get_seller)
    return request