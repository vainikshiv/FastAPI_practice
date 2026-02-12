import uvicorn
from fastapi import FastAPI
from . import models
from .database import engine
from .router import product, seller, login


app = FastAPI(
    title="Seller API",
    description="Details of products and seller",
    version="1.0.1",
    terms_of_service="https://www.google.com/policies/list/",
    contact={
        "developer": "XYZ",
        "email": "xyz@gmail.com",
    },
    license_info={
        "name": "Open Source",
        "url": "https://www.google.com/",
    }
)

app.include_router(product.router)
app.include_router(seller.router)
app.include_router(login.router)

models.Base.metadata.create_all(engine)



# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)