from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from crud.user import (
    create_user,
    delete_user,
    edit_user,
    get_user,
    get_user_info,
    user_login,
    user_refresh,
)
from dependencies.dependencies import get_current_user, get_db, verify_refresh_token
from models.refresh_token import RefreshTokenModel
from models.user import UserModel
from schemas.token import TokenResponseModel
from schemas.user import EditUserSchema, RegisterUserSchema, UserResponseSchema

from fastapi_cache.decorator import cache
from fastapi_cache import FastAPICache

route = APIRouter(prefix="/users")

@route.get("/", status_code=status.HTTP_200_OK, response_model=list[UserResponseSchema])
@cache(60)
def get_user_route(search: str | None = None, db: Session = Depends(get_db)):
    return get_user(db, search)


@route.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
@cache(60 * 3)
def get_user_info_route(user: UserModel = Depends(get_current_user)):
    return get_user_info(user)


@route.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema)
def create_user_route(item: RegisterUserSchema, db: Session = Depends(get_db)):
    return create_user(item, db)


@route.put("/", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
def edit_user_route(
    item: EditUserSchema, db: Session = Depends(get_db), user: UserModel = Depends(get_current_user)
):
    return edit_user(item, db, user)


@route.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_route(db: Session = Depends(get_db), user: UserModel = Depends(get_current_user)):
    await FastAPICache.clear(namespace="get_user_info_route")
    return delete_user(db, user)


@route.post("/login", status_code=status.HTTP_200_OK, response_model=TokenResponseModel)
def user_login_route(
    response: Response, db: Session = Depends(get_db), item: OAuth2PasswordRequestForm = Depends()
):
    return user_login(response, db, item)


@route.post("/refresh", status_code=status.HTTP_200_OK, response_model=TokenResponseModel)
def user_refresh_route(
    response: Response,
    db: Session = Depends(get_db),
    old_token: RefreshTokenModel = Depends(verify_refresh_token),
):
    return user_refresh(db, response, old_token)
