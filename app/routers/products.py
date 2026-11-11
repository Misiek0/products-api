from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.product_repository import ProductRepository
from app.schemas.product import (
    ProductCreate,
    ProductListItem,
    ProductRead,
    ProductUpdate,
)
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    """Wires the layers together through dependency injection."""
    return ProductService(ProductRepository(db))


# The list returns only the key fields; details return everything.
@router.get("", response_model=list[ProductListItem])
def list_products(
    service: ProductService = Depends(get_product_service),
) -> list[ProductListItem]:
    return service.list_products()


@router.get("/{product_id}", response_model=ProductRead)
def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
) -> ProductRead:
    # No try/except: ProductNotFoundError is turned into 404 by the
    # handler registered in error_handlers.py.
    return service.get_product(product_id)


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    data: ProductCreate,
    service: ProductService = Depends(get_product_service),
) -> ProductRead:
    return service.create_product(data)


# 200 OK (the default): the resource already existed and is returned updated.
@router.put("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    data: ProductUpdate,
    service: ProductService = Depends(get_product_service),
) -> ProductRead:
    # Not-found, duplicate-name and price errors are all mapped to HTTP
    # by the global handlers, so the router stays free of error handling.
    return service.update_product(product_id, data)