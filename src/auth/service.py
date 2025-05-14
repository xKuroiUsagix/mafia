from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from .models import User
from .utils import get_password_hash
from .schemas import (
    UserCreateRequest,
    UserResponse
)


class UserService:

    def create_user(self, db: Session, user_data: UserCreateRequest) -> User:
        if user_data.password != user_data.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='password and confirm_password do not match'
            )
    
        user_in_db = db.query(User).filter(or_(User.username == user_data.username, 
                                            User.email == user_data.email)).first()
        if user_in_db is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User with provided username or email already exists'
            )
        
        user = User(
            username=user_data.username,
            email=user_data.email,
            password=get_password_hash(user_data.password)
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user


user_service = UserService()
