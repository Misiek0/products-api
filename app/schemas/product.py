from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProductRead(BaseModel):
    """API Response Contract. Separated from ORM model."""

    # from_attributes pozwala zbudować schemat prosto z obiektu ORM.
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: Decimal