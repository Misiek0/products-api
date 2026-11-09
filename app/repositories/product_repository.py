from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product


class ProductRepository:
    """Place which knows how to get data from db."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> Sequence[Product]:
        return self.db.scalars(select(Product).order_by(Product.id)).all()
