from collections.abc import Sequence

from app.models.product import Product
from app.repositories.product_repository import ProductRepository


class ProductService:
    """Business logic."""

    def __init__(self, repository: ProductRepository) -> None:
        self.repository = repository

    def list_products(self) -> Sequence[Product]:
        return self.repository.get_all()