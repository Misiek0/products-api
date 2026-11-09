from collections.abc import Sequence

from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.services.exceptions import ProductNotFoundError


class ProductService:
    """Business logic."""

    def __init__(self, repository: ProductRepository) -> None:
        self.repository = repository

    def list_products(self) -> Sequence[Product]:
        return self.repository.get_all()

    def get_product(self, product_id: int) -> Product:
        product = self.repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(product_id)
        return product
