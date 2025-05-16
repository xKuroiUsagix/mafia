from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import asynccontextmanager
from config import settings


if not settings.USE_DB:
    DATABASE_URL = 'sqlite+aiosqlite:///sqlite.db'
else:
    DATABASE_URL = f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@postgres:5432/{settings.DB_NAME}'

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@asynccontextmanager
async def db_lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
