import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from database import get_db
from config import settings
from .schemas import TokenData
from .utils import oauth2_scheme
from .models import User
from sqlalchemy.ext.asyncio import AsyncSession


async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get('sub')
        
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    
    result = await db.execute(
        User.__table__.select().where(User.username == token_data.username)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception
    return user
