from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from ..schemas import UserCreateRequest, UserResponse
from ..models import User
from ..dependencies import get_current_user
from ..service import user_service


router = APIRouter(prefix='/users')


@router.post('', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreateRequest, db: Session = Depends(get_db)):
    return user_service.create_user(db, user_data)

@router.get('', response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get('/me', response_model=UserResponse)
def get_user(current_user: UserResponse = Depends(get_current_user)):
    return current_user
