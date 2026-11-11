from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.product import Product


class ProductRepository:
    """The only place that knows how to read and write products."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> Sequence[Product]:
        return self.db.scalars(select(Product).order_by(Product.id)).all()

    def get_by_id(self, product_id: int) -> Product | None:
        return self.db.get(Product, product_id)

    def get_by_name(self, name: str) -> Product | None:
        # Case-insensitive: "Laptop" and "laptop" count as the same name.
        stmt = select(Product).where(func.lower(Product.name) == name.lower())
        return self.db.scalars(stmt).first()

    def create(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        # refresh loads database-generated values (e.g. id).
        self.db.refresh(product)
        return product

    def update(self, product: Product) -> Product:
        # The object was loaded through this session, so SQLAlchemy already
        # tracks its changes: commit is enough to persist them.
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self.db.delete(product)
        # Commit lives in the repository, which owns persistence.
        # Nothing to refresh: the row no longer exists after this.
        self.db.commit()
