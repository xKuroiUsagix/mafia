import uvicorn
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine
from database import Base, engine
from auth.routers.user import router as users_router
from auth.routers.authentication import router as token_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users_router, tags=['Users'])
app.include_router(token_router, tags=['Token'])

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
