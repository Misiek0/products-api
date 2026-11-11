from collections.abc import Sequence
from decimal import Decimal

from app.models.product import Category, Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate
from app.services.exceptions import (
    DuplicateProductNameError,
    PriceOutOfRangeError,
    ProductNotFoundError,
)

# Business rule from the assignment: allowed price range (in PLN) per category.
PRICE_LIMITS: dict[Category, tuple[Decimal, Decimal]] = {
    Category.ELECTRONICS: (Decimal("50"), Decimal("50000")),
    Category.BOOKS: (Decimal("5"), Decimal("500")),
    Category.CLOTHING: (Decimal("10"), Decimal("5000")),
}


class ProductService:
    """Business logic layer."""

    def __init__(self, repository: ProductRepository) -> None:
        self.repository = repository

    def list_products(self) -> Sequence[Product]:
        return self.repository.get_all()

    def get_product(self, product_id: int) -> Product:
        product = self.repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(product_id)
        return product

    def create_product(self, data: ProductCreate) -> Product:
        # Cheap in-memory check first, database lookup second.
        self._ensure_price_in_range(data.category, data.price)
        self._ensure_name_is_unique(data.name)
        # The service turns API data into a domain object (ORM model);
        # the repository receives a ready Product and knows no schemas.
        product = Product(
            name=data.name,
            category=data.category.value,
            price=data.price,
            quantity=data.quantity,
        )
        return self.repository.create(product)

    def _ensure_price_in_range(self, category: Category, price: Decimal) -> None:
        minimum, maximum = PRICE_LIMITS[category]
        if not minimum <= price <= maximum:
            raise PriceOutOfRangeError(category.value, minimum, maximum)

    def _ensure_name_is_unique(self, name: str) -> None:
        if self.repository.get_by_name(name) is not None:
            raise DuplicateProductNameError(name)