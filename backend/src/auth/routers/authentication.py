import jwt
from datetime import timedelta
from fastapi import APIRouter, Depends, Request
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from config import settings
from ..utils import authenticate_user, create_token
from ..schemas import TokenBase, TokenPair, TokenRequest
from ..exceptions import AuthenticationError, UserNotFoundError
from ..models import User


router = APIRouter(prefix='/token')


@router.post('/obtain')
async def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
) -> TokenPair:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise AuthenticationError()

    data = {'sub': user.username}
    access_token_expires = timedelta(minutes=settings.ACCES_TOKEN_EXPIRES_MINUTES)
    access_token = create_token(
        data=data, 
        expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(hours=settings.REFRESH_TOKEN_EXPIRES_HOURS)
    refresh_token = create_token(
        data=data, 
        expires_delta=refresh_token_expires
    )

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=settings.DEBUG == 0,
        samesite='lax',
        max_age=settings.REFRESH_TOKEN_EXPIRES_HOURS*60*60
    )

    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token if settings.DEBUG else None,
        token_type='bearer'
    )

@router.post('/refresh')
async def refresh_token(
    request: Request,
    token_data: TokenRequest = None, 
    db: AsyncSession = Depends(get_db)
) -> TokenBase:
    if settings.DEBUG and token_data:
        refresh_token = token_data.refresh_token
    else:
        refresh_token = request.cookies.get('refresh_token')

    if not refresh_token:
        raise AuthenticationError('Refresh token is missing.')

    try:
        payload = jwt.decode(
            token_data.token, 
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
    except jwt.ExpiredSignatureError:
        raise AuthenticationError('Token has expired.')
    except jwt.InvalidSignatureError:
        raise AuthenticationError('Token is invalid')
    except:
        raise AuthenticationError('Unknown authentication error.')
    
    username = payload.get('sub')
    result = await db.execute(select(User).where(User.username==username))
    user = result.scalar_one_or_none()

    if not user:
        raise UserNotFoundError

    data = {'sub': username}
    access_token_expires = timedelta(minutes=settings.ACCES_TOKEN_EXPIRES_MINUTES)
    access_token = create_token(
        data=data,
        expires_delta=access_token_expires
    )

    return TokenBase(
        access_token=access_token,
        token_type='bearer'
    )

@router.post('/verify')
async def verify_token(token_data: TokenRequest):
    try:
        jwt.decode(
            token_data.token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return {'token_valid': True}
    except jwt.ExpiredSignatureError:
        raise AuthenticationError('Token has expired.')
    except Exception:
        raise AuthenticationError('Token is invalid')
