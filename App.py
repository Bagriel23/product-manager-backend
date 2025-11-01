from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from Model import Product
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProductModel(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    available: Optional[bool] = True

@app.get("/products", tags=["products"], response_model=List[dict])
def list_products():
    products = Product.objects()
    return [p.to_mongo().to_dict() for p in products]


@app.get("/products/{product_id}", tags=["products"], response_model=dict)
def get_product_by_id(product_id: int):
    product = Product.objects(id=product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product.to_mongo().to_dict()


@app.post("/products", tags=["products"], response_model=dict)
def register_product(product: ProductModel):
    new_product = Product(
        name=product.name,
        description=product.description,
        price=str(product.price),
        available=product.available
    )
    new_product.save()
    return new_product.to_mongo().to_dict()


@app.put("/products/{product_id}", tags=["products"], response_model=dict)
def update_product(product_id: int, product: ProductModel):
    """Atualizar produto"""
    existing_product = Product.objects(id=product_id).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    existing_product.update(
        set__name=product.name,
        set__description=product.description,
        set__price=str(product.price),
        set__available=product.available
    )
    return Product.objects(id=product_id).first().to_mongo().to_dict()


@app.delete("/products/{product_id}", tags=["products"], response_model=dict)
def delete_product(product_id: int):
    product = Product.objects(id=product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    product.delete()
    return {"message": "Produto removido com sucesso"}


@app.get("/products/available", tags=["products"], response_model=List[dict])
def list_available_products():
    available_products = Product.objects(available=True)
    return [p.to_mongo().to_dict() for p in available_products]
