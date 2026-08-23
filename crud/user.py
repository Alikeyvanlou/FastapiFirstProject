from sqlalchemy.orm import Session
from sqlalchemy import Select
from models.user import UserModel
from fastapi import HTTPException, status
from schemas.user import RegisterUserSchema, EditUserSchema
from datetime import datetime

def get_user(db: Session, search: str):
    query = Select(UserModel)
    if not search:
        query = Select(UserModel).where(UserModel.username == search)
    return db.scalars(query).all()

def get_user_by_id(db: Session, user_id: int):
    query = Select(UserModel).where(UserModel.id == user_id)
    if query == None:
        raise HTTPException(detail="user not found", status_code=status.HTTP_404_NOT_FOUND)
    user = db.scalar(query)
    return user

def create_user(item: RegisterUserSchema, db: Session):
    email = Select(UserModel).where(UserModel.email == item.email)
    if email != None:
        raise HTTPException(detail="{item.email} register before", status_code=status.HTTP_400_BAD_REQUEST)
    new_user = UserModel(username = item.username, email = item.email, password =  item.password)               
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def edit_user(user_id: int, item: EditUserSchema, db: Session):
    user = Select(UserModel).where(UserModel.id == user_id)
    if user == None:
        raise HTTPException(detail="user not found", status_code=status.HTTP_404_NOT_FOUND)
    user.username = item.username
    user.email = item.email
    user.password = item.password
    db.commit()
    db.refresh(user)
    return user

def delete_user(user_id: int, db: Session):
    user = Select(UserModel).where(UserModel.id == user_id)
    if user == None:
        raise HTTPException(detail="user not found", status_code=status.HTTP_404_NOT_FOUND)
    db.delete(user)
    db.commit()
    return {"message" : "user sccessfully removed."}