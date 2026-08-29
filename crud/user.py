from datetime import timedelta

from fastapi import HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import Select
from sqlalchemy.orm import Session

from core.auth import create_access_token, create_refresh_token, hashing_pws, verifying_pws
from models.refresh_token import RefreshTokenModel
from models.user import UserModel
from schemas.user import EditUserSchema, RegisterUserSchema


def get_user(db: Session, search: str):
    users = Select(UserModel)
    if search:
        users = Select(UserModel).where(UserModel.username == search)
    res = db.scalars(users).all()
    return res


def get_user_info(user: UserModel):
    return user


def create_user(item: RegisterUserSchema, db: Session):
    existing_user = db.scalar(
        Select(UserModel).where(
            (UserModel.email == item.email) | (UserModel.username == item.username)
        )
    )
    if existing_user is not None:
        raise HTTPException(
            detail="Email or username already registered", status_code=status.HTTP_400_BAD_REQUEST
        )

    new_user = UserModel(
        username=item.username, email=item.email, password=hashing_pws(item.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def edit_user(item: EditUserSchema, db: Session, user: UserModel):
    if item.username is not None:
        user.username = item.username
    if item.email is not None:
        user.email = item.email
    if item.password is not None:
        user.password = hashing_pws(item.password)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: UserModel):
    db.delete(user)
    db.commit()
    return {"message": "user sccessfully removed."}


def user_login(response: Response, db: Session, form: OAuth2PasswordRequestForm):
    query = Select(UserModel).where(UserModel.username == form.username)
    user = db.scalar(query)
    if user is None:
        raise HTTPException(
            detail="username or password is incorrect.", status_code=status.HTTP_403_FORBIDDEN
        )
    if not verifying_pws(form.password, user.password):
        raise HTTPException(
            detail="username or password is incorrect.", status_code=status.HTTP_403_FORBIDDEN
        )
    payload = {"sub": user.username}
    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(
        response=response, payload=payload, expires_delta=timedelta(hours=24 * 7), user_id=user.id
    )
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)
    return {"access_token": access_token, "token_type": "bearer"}


def user_refresh(db: Session, response: Response, old_token: RefreshTokenModel):
    user = db.scalar(Select(UserModel).where(UserModel.id == old_token.user_id))
    payload = {"sub": user.username}
    new_refresh_token = create_refresh_token(
        response=response, payload=payload, expires_delta=timedelta(hours=24 * 7), user_id=user.id
    )
    new_access_token = create_access_token(payload=payload)
    db.add(new_refresh_token)
    db.delete(old_token)
    db.commit()
    db.refresh(new_refresh_token)
    return {"access_token": new_access_token, "token_type": "bearer"}
