import uvicorn
from fastapi import FastAPI
from database import db_lifespan
from auth.routers.user import router as users_router
from auth.routers.authentication import router as token_router


app = FastAPI(lifespan=db_lifespan)

app.include_router(users_router, tags=['Users'])
app.include_router(token_router, tags=['Token'])


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
