from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from config import settings
from ..utils import authenticate_user, create_access_token
from ..schemas import TokenBase


router = APIRouter()


@router.post('/token')
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
) -> TokenBase:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    access_token_expires = timedelta(minutes=settings.ACCES_TOKEN_EXPIRES_MINUTES)
    acces_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return TokenBase(access_token=acces_token, token_type='bearer')
