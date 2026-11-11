from decimal import Decimal


class ProductNotFoundError(Exception):
    """Domain exception: knows nothing about HTTP."""

    def __init__(self, product_id: int) -> None:
        super().__init__(f"Product {product_id} not found")
        self.product_id = product_id


class ProductRuleViolation(Exception):
    """Base class for business-rule errors tied to one request field.
    The field name lets the API tell the client exactly what to fix."""

    field: str

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class DuplicateProductNameError(ProductRuleViolation):
    field = "name"

    def __init__(self, name: str) -> None:
        super().__init__(f"Product name '{name}' is already taken")


class PriceOutOfRangeError(ProductRuleViolation):
    field = "price"

    def __init__(self, category: str, minimum: Decimal, maximum: Decimal) -> None:
        super().__init__(
            f"Price for category '{category}' must be between "
            f"{minimum} and {maximum} PLN"
        )