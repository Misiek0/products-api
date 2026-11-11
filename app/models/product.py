from decimal import Decimal
from enum import StrEnum

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Category(StrEnum):
    """Allowed product categories. Adding one here also requires an entry
    in PRICE_LIMITS in the service, otherwise its price check will fail."""

    ELECTRONICS = "electronics"
    BOOKS = "books"
    CLOTHING = "clothing"


class Product(Base):
    """ORM model: describes the table, nothing more."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)
    category: Mapped[str] = mapped_column(String(20))
    # Numeric instead of Float: money must not have rounding errors.
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    quantity: Mapped[int]