import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database import get_db
from config import settings
from .schemas import TokenData
from .utils import oauth2_scheme
from .models import User
from .exceptions import AuthenticationError


async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    error_message = 'Incorrect username or password'
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get('sub')
        
        if username is None:
            raise AuthenticationError(error_message)
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise AuthenticationError(error_message)
    
    result = await db.execute(
        User.__table__.select().where(User.username == token_data.username)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise AuthenticationError(error_message)
    return user
