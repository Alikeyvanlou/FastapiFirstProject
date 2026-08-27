from database.db import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, Request, Query
import jwt
from core.config import settings
from jwt.exceptions import InvalidTokenError
from sqlalchemy import Select
from models.user import UserModel
from sqlalchemy.orm import Session
from models.refresh_token import RefreshTokenModel
from datetime import datetime , timezone


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    query = Select(UserModel).where(UserModel.username == username)
    user = db.scalar(query)
    if user is None:
        raise credentials_exception
    return user

def verify_refresh_token(request: Request, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = request.cookies.get("refresh_token")
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        if payload.get("type") != "refresh":
             raise credentials_exception
    except InvalidTokenError:
            raise credentials_exception
    
    user = db.scalar(Select(UserModel).where(UserModel.username == username))
    if user is None:
         raise credentials_exception
    jti = payload.get("jti")
    refresh_token = db.scalar(Select(RefreshTokenModel).where(RefreshTokenModel.jti == jti))

    if jti is None or refresh_token is None:
        raise credentials_exception
    if refresh_token.is_revoked :
        raise credentials_exception
    if refresh_token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc) :
        raise credentials_exception

    return refresh_token

def get_lang(lang: str = Query(default="en")) -> str:
    return lang
