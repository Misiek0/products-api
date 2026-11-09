class ProductNotFoundError(Exception):
    """Exception"""

    def __init__(self, product_id: int) -> None:
        super().__init__(f"Product {product_id} not found")
        self.product_id = product_id
