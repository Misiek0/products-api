from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.product import Category


class ProductCreate(BaseModel):
    """Input contract for POST. Has no id because the database assigns it.
    Only format rules live here. Rules that need the database or several
    fields together (unique name, price range per category) live in the
    service. Invalid input is rejected with 422 before reaching it."""

    name: str = Field(min_length=3, max_length=20)
    category: Category
    # max_digits/decimal_places match Numeric(10, 2) in the model.
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    # strict=True: only a real JSON integer is accepted (not "5" or 5.5).
    quantity: int = Field(strict=True, ge=0)

    @field_validator("name")
    @classmethod
    def name_must_be_alphanumeric(cls, value: str) -> str:
        # isalnum() accepts letters (including Polish ones) and digits only;
        # spaces, hyphens and underscores are rejected.
        if not value.isalnum():
            raise ValueError("must contain only letters and digits")
        return value


class ProductUpdate(ProductCreate):
    """Input contract for PUT. PUT replaces the whole resource, so it needs
    exactly the same fields and rules as creation. A separate class keeps
    the two contracts independent: if PUT rules ever diverge from POST,
    only this class changes."""


class ProductListItem(BaseModel):
    """Short representation for the list endpoint (id, name, price)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: Decimal


class ProductRead(ProductListItem):
    """Full representation for the details endpoint and write responses."""

    category: Category
    quantity: int
