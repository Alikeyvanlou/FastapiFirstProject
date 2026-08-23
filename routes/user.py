from fastapi import APIRouter, status, Depends
from schemas.user import *
from sqlalchemy.orm import Session
from crud.user import *
from dependencies.dependencies import get_db

route = APIRouter(prefix="/users")

@route.get("/", status_code=status.HTTP_200_OK, response_model=list[UserResponseSchema])
def get_user_route(search: str | None = None, db: Session = Depends(get_db)):
    return get_user(db, search)

@route.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
def get_user_by_id_route(user_id: int , db: Session = Depends(get_db)):
    return get_user_by_id(db, user_id)

@route.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema)
def create_user_route(item: RegisterUserSchema, db: Session = Depends(get_db)):
    return create_user(item, db)

@route.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
def edit_user_route(user_id: int, item:EditUserSchema ,db: Session =Depends(get_db)):
    return edit_user(user_id, item, db)

@route.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_route(user_id: int,db: Session =Depends(get_db)):
    return delete_user(user_id, db)