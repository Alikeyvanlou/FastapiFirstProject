from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import *
from sqlalchemy.orm import Session
from crud.user import *
from dependencies.dependencies import get_db, get_current_user
from schemas.token import TokenResponseModel
from dependencies.dependencies import verify_refresh_token, get_lang

route = APIRouter(prefix="/users")

@route.get("/", status_code=status.HTTP_200_OK, response_model=list[UserResponseSchema])
def get_user_route(search: str | None = None, db: Session = Depends(get_db)):
    return get_user(db, search)

@route.get("/", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
def get_user_info_route(user: UserModel = Depends(get_current_user)):
    return get_user_info(user)

@route.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema)
def create_user_route(item: RegisterUserSchema, 
                      db: Session = Depends(get_db),
                      lang: str = Depends(get_lang)):
    return create_user(item, db, lang)

@route.put("/", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
def edit_user_route(item: EditUserSchema ,db: Session =Depends(get_db), user: UserModel = Depends(get_current_user)):
    return edit_user(item, db, user)

@route.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_route(db: Session =Depends(get_db), 
                      user: UserModel = Depends(get_current_user),
                      lang: str = Depends(get_lang)):
    return delete_user(db, user, lang)

@route.post("/", status_code=status.HTTP_200_OK, response_model=TokenResponseModel)
def user_login_route(response: Response, 
                     db: Session = Depends(get_db), 
                     item: OAuth2PasswordRequestForm = Depends(),
                     lang: str = Depends(get_lang)):
    return user_login(response, db, item, lang)

@route.post("/refresh", status_code=status.HTTP_200_OK, response_model=TokenResponseModel)
def user_refresh_route(response: Response, db: Session = Depends(get_db), old_token: RefreshTokenModel = Depends(verify_refresh_token)):
    return user_refresh(db, response, old_token)