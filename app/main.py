from fastapi import FastAPI
from contextlib import asynccontextmanager
import app.models
from app.database import Base, engine
from app.routers import products


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Products API", lifespan=lifespan)
app.include_router(products.router, prefix="/api/v1")
