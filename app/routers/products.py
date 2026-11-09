from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductRead
from app.services.exceptions import ProductNotFoundError
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    """Składa warstwy przez wstrzykiwanie zależności. W testach
    można podmienić całą usługę przez dependency_overrides."""
    return ProductService(ProductRepository(db))


@router.get("", response_model=list[ProductRead])
def list_products(
    service: ProductService = Depends(get_product_service),
) -> list[ProductRead]:
    return service.list_products()

@router.get("/{product_id}", response_model=ProductRead)
def get_product(
        product_id: int,
        service: ProductService = Depends(get_product_service),
) -> ProductRead:
    try:
        return service.get_product(product_id)
    except ProductNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
