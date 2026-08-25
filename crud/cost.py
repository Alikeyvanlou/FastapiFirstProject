from sqlalchemy.orm import Session
from sqlalchemy import Select
from models.cost import CostModel
from models.user import UserModel
from fastapi import HTTPException, status
from schemas.cost import CostCreateSchema, CostUpdateSchema
from datetime import datetime

def get_cost(db: Session, search: str, user: UserModel):
    query = Select(CostModel).where(CostModel.user_id == user.id)
    if search:
        query = Select(CostModel).where(CostModel.title == search, CostModel.user_id == user.id)
    return db.scalars(query).all()

def get_cost_by_id(db: Session, cost_id: int, user: UserModel):
    query = Select(CostModel).where(CostModel.id == cost_id, CostModel.user_id == user.id)
    cost = db.scalar(query)
    if cost == None:
        raise HTTPException(detail="cost not found", status_code=status.HTTP_404_NOT_FOUND)
    return cost

def create_cost(item: CostCreateSchema, db: Session, user: UserModel):
    new_cost = CostModel(title = item.title, amount = item.amount, 
                         create_at = datetime.now().strftime('%a %d %b %Y, %I:%M%p'),
                         user_id= user.id)
    db.add(new_cost)
    db.commit()
    db.refresh(new_cost)
    return new_cost

def edit_cost(cost_title: int, item: CostUpdateSchema, db: Session, user: UserModel):
    query = Select(CostModel).where(CostModel.user_id == user.id, CostModel.title == cost_title)
    cost = db.scalar(query)
    if cost == None:
        raise HTTPException(detail="cost not found", status_code=status.HTTP_404_NOT_FOUND)
    cost.title = item.title
    cost.amount = item.amount
    cost.update_at = datetime.now().strftime('%a %d %b %Y, %I:%M%p')
    db.commit()
    db.refresh(cost)
    return cost

def delete_cost(cost_title: str, db: Session, user: UserModel):
    query = Select(CostModel).where(CostModel.user_id == user.id, CostModel.title == cost_title)
    cost = db.scalar(query)
    if cost == None:
        raise HTTPException(detail="cost not found", status_code=status.HTTP_404_NOT_FOUND)
    db.delete(cost)
    db.commit()
    return {"message" : "cost sccessfully removed."}