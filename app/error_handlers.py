from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.services.exceptions import (
    DuplicateProductNameError,
    PriceOutOfRangeError,
    ProductNotFoundError,
    ProductRuleViolation,
)


def _field_error(exc: ProductRuleViolation) -> dict:
    # Same shape as FastAPI's own 422 body, so clients parse one format
    # for both schema errors and business-rule errors.
    return {
        "detail": [
            {"loc": ["body", exc.field], "msg": exc.message, "type": "business_rule"}
        ]
    }


def register_error_handlers(app: FastAPI) -> None:
    """Translates domain exceptions to HTTP in one place, so routers
    (POST now, PUT later) do not repeat try/except blocks."""

    @app.exception_handler(ProductNotFoundError)
    async def not_found_handler(_: Request, exc: ProductNotFoundError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Product not found"},
        )

    @app.exception_handler(DuplicateProductNameError)
    async def duplicate_handler(
        _: Request, exc: DuplicateProductNameError
    ) -> JSONResponse:
        # 409 Conflict: the data is valid but clashes with existing state.
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT, content=_field_error(exc)
        )

    @app.exception_handler(PriceOutOfRangeError)
    async def price_handler(_: Request, exc: PriceOutOfRangeError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=_field_error(exc),
        )