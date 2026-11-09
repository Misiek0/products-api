from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductRead
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