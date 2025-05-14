from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from ..schemas import UserCreateRequest, UserResponse
from ..models import User
from ..dependencies import get_current_user
from ..service import user_service


router = APIRouter(prefix='/users')


@router.post('', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateRequest, db: AsyncSession = Depends(get_db)):
    return await user_service.create_user(db, user_data)

@router.get('', response_model=List[UserResponse])
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(User.__table__.select())
    users = result.scalars().all()
    return users

@router.get('/me', response_model=UserResponse)
async def get_user(current_user: UserResponse = Depends(get_current_user)):
    return current_user
