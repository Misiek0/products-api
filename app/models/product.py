from decimal import Decimal

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Product(Base):
    """Model ORM: opisuje tabelę w bazie"""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    # Numeric instead of Float: money can't have rounding errors.
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    