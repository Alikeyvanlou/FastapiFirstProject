from datetime import datetime

from sqlalchemy import Select
from sqlalchemy.orm import Session

from core.exception import CostNotFoundError
from models.cost import CostModel
from models.user import UserModel
from schemas.cost import CostCreateSchema, CostUpdateSchema


def get_cost(db: Session, search: str, user: UserModel):
    query = Select(CostModel).where(CostModel.user_id == user.id)
    if search:
        query = Select(CostModel).where(CostModel.title == search, CostModel.user_id == user.id)
    return db.scalars(query).all()


def get_cost_by_id(db: Session, cost_id: int, user: UserModel):
    query = Select(CostModel).where(CostModel.id == cost_id, CostModel.user_id == user.id)
    cost = db.scalar(query)
    if cost is None:
        raise CostNotFoundError(cost_id=cost_id)
    return cost


def create_cost(item: CostCreateSchema, db: Session, user: UserModel):
    new_cost = CostModel(
        title=item.title,
        amount=item.amount,
        create_at=datetime.now().strftime("%a %d %b %Y, %I:%M%p"),
        user_id=user.id,
    )
    db.add(new_cost)
    db.commit()
    db.refresh(new_cost)
    return new_cost


def edit_cost(cost_id: int, item: CostUpdateSchema, db: Session, user: UserModel):
    query = Select(CostModel).where(CostModel.user_id == user.id, CostModel.id == cost_id)
    cost = db.scalar(query)
    if cost is None:
        raise CostNotFoundError(cost_id=cost_id)
    cost.title = item.title
    cost.amount = item.amount
    cost.update_at = datetime.now().strftime("%a %d %b %Y, %I:%M%p")
    db.commit()
    db.refresh(cost)
    return cost


def delete_cost(cost_id: int, db: Session, user: UserModel):
    query = Select(CostModel).where(CostModel.user_id == user.id, CostModel.id == cost_id)
    cost = db.scalar(query)
    if cost is None:
        raise CostNotFoundError(cost_id=cost_id)
    db.delete(cost)
    db.commit()
    return {"message": "cost sccessfully removed."}
