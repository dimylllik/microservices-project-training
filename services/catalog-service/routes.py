from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from catalog_repository import ProductRepository
from catalog_service import ProductService
from schemas import ProductCreate, ProductUpdate, ProductRead

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductRead, status_code=201)
def create_product(data:ProductCreate, db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    service = ProductService(repo)
    return service.create_product(data)

@router.get("/", response_model=list[ProductRead])
def get_products(db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    service = ProductService(repo)
    return service.get_products()

@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: str, db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    service = ProductService(repo)
    return service.get_product(product_id)

@router.put("/{product_id}", response_model=ProductRead)
def update_product(product_id: str, data: ProductUpdate, db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    service = ProductService(repo)
    product = service.update_products(product_id, data)
    if not product:
        raise HTTPException(404, "Product not found")
    return product

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id:str, db:Session = Depends(get_db)):
    repo = ProductRepository(db)
    service = ProductService(repo)
    product = service.delete_product(product_id)
    if not product:
        raise HTTPException(404, "Product not found")
