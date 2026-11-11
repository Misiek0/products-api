from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.models  # noqa: F401  (registers models in Base.metadata)
from app.database import Base, engine
from app.error_handlers import register_error_handlers
from app.routers import products


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Products API", lifespan=lifespan)
register_error_handlers(app)
app.include_router(products.router, prefix="/api/v1")
