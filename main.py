from contextlib import asynccontextmanager
from fastapi import FastAPI

import models
from db import Base, engine
from routers import posts, users

@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(posts.router)
app.include_router(users.router)