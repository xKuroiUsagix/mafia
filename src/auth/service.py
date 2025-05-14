from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User
from .utils import get_password_hash
from .schemas import UserCreateRequest


class UserService:

    async def create_user(self, db: AsyncSession, user_data: UserCreateRequest) -> User:
        if user_data.password != user_data.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='password and confirm_password do not match'
            )
        result = await db.execute(
            User.__table__.select().where(
                (User.username == user_data.username) | (User.email == user_data.email)
            )
        )
        user_in_db = result.scalar_one_or_none()
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
        await db.commit()
        await db.refresh(user)

        return user


user_service = UserService()
