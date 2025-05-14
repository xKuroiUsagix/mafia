import uvicorn
from fastapi import FastAPI
from database import Base, engine
from auth.routers.user import router as users_router
from auth.routers.authentication import router as token_router


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router, tags=['Users'])
app.include_router(token_router, tags=['Token'])

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
