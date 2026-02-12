from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from typing import List

router = APIRouter(
    tags=["Products"],
    prefix="/product",
)

@router.get("/", response_model=List[schemas.DisplayProduct])
def products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@router.get("/{id}", response_model=schemas.DisplayProduct)
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@router.post("/", status_code=status.HTTP_201_CREATED)
def add(request: schemas.Product, db: Session = Depends(get_db)):
    add_product = models.Product(
        name=request.name,
        description=request.description,
        price=request.price,
        seller_id=1
    )
    db.add(add_product)
    db.commit()
    db.refresh(add_product)
    return request

@router.put("/{id}")
def update_product(id: int,request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        raise HTTPException(status_code=404, detail="Product not found")
    product.update(request.model_dump())
    db.commit()
    return {"Product updated."}

@router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {f"Product deleted."}