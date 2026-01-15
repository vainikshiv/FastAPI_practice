import uvicorn
from fastapi import FastAPI
from fastapi import Depends, HTTPException
from sqlalchemy.sql.functions import mode
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/products")
def products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@app.get("/product/{id}")
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    return product

@app.post("/products")
def add(request: schemas.Product, db: Session = Depends(get_db)):
    add_product = models.Product(
        name=request.name,
        description=request.description,
        price=request.price
    )
    db.add(add_product)
    db.commit()
    db.refresh(add_product)
    return request

@app.put("/product/{id}")
def update_product(id: int,request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        raise HTTPException(status_code=404, detail="Product not found")
    product.update(request.model_dump())
    db.commit()
    return {"Product updated."}

@app.delete("/product/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {f"Product deleted."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)