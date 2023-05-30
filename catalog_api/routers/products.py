from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models import Product, User
from ..authentication import get_current_user
from ..database import products_collection

router = APIRouter()


@router.get("/products", response_model=List[Product])
def get_all_products():
    products = products_collection.find()
    return list(products)


@router.get("/products/{product_sku}", response_model=Product)
def get_product(product_sku: str):
    product = products_collection.find_one({"sku": product_sku})
    if product:
        return product
    else:
        raise HTTPException(status_code=404, detail="Product not found")


@router.post("/products", response_model=Product)
def create_product(product: Product, current_user: User = Depends(get_current_user)):
    product_dict = product.dict()
    inserted_product = products_collection.insert_one(product_dict)
    return product


@router.put("/products/{product_sku}", response_model=Product)
def update_product(product_sku: str, product: Product, current_user: User = Depends(get_current_user)):
    existing_product = products_collection.find_one({"sku": product_sku})
    if existing_product:
        product_dict = product.dict()
        product_dict["sku"] = existing_product["sku"]
        products_collection.replace_one({"sku": product_sku}, product_dict)
        return product
    else:
        raise HTTPException(status_code=404, detail="Product not found")


@router.delete("/products/{product_sku}")
def delete_product(product_sku: str, current_user: User = Depends(get_current_user)):
    result = products_collection.delete_one({"sku": product_sku})
    if result.deleted_count == 1:
        return {"message": "Product deleted"}
    else:
        raise HTTPException(status_code=404, detail="Product not found")
