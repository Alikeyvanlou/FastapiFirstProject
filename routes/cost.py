from fastapi import APIRouter, status, Depends
from models.cost import CostModel
from schemas.cost import *
from sqlalchemy.orm import Session
from crud.cost import *
from dependencies.dependencies import get_db

route = APIRouter(prefix="/costs")

@route.get("/", status_code=status.HTTP_200_OK, response_model=list[CostResponseSchema])
def get_cost_route(search: str | None = None, db: Session = Depends(get_db)):
    return get_cost(db, search)

@route.get("/{cost_id}", status_code=status.HTTP_200_OK, response_model=CostResponseSchema)
def get_cost_by_id_route(cost_id: int , db: Session = Depends(get_db)):
    return get_cost_by_id(db, cost_id)

@route.post("/", status_code=status.HTTP_201_CREATED, response_model=CostResponseSchema)
def create_cost_route(item: CostCreateSchema, db: Session = Depends(get_db)):
    return create_cost(item, db)

@route.put("/{cost_id}", status_code=status.HTTP_200_OK, response_model=CostResponseSchema)
def edit_cost_route(cost_id: int, item:CostUpdateSchema ,db: Session =Depends(get_db)):
    return edit_cost(cost_id, item, db)

@route.delete("/{cost_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cost_route(cost_id: int,db: Session =Depends(get_db)):
    return delete_cost(cost_id, db)