from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers import router
from app.core.database import engine, Base


@asynccontextmanager
async def lifespan(application: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app: FastAPI = FastAPI(lifespan=lifespan)

app.include_router(router)
