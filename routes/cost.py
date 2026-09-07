from fastapi import APIRouter, Depends, status
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from crud.cost import create_cost, delete_cost, edit_cost, get_cost, get_cost_by_id
from dependencies.dependencies import get_current_user, get_db
from models.user import UserModel
from schemas.cost import CostCreateSchema, CostResponseSchema, CostUpdateSchema

route = APIRouter(prefix="/costs")


@route.get("/", status_code=status.HTTP_200_OK, response_model=list[CostResponseSchema])
@cache(60)
def get_cost_route(
    search: str | None = None,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    return get_cost(db, search, user)


@route.get("/{cost_id}", status_code=status.HTTP_200_OK, response_model=CostResponseSchema)
@cache(60)
def get_cost_by_id_route(
    cost_id: int, db: Session = Depends(get_db), user: UserModel = Depends(get_current_user)
):
    return get_cost_by_id(db, cost_id, user)


@route.post("/", status_code=status.HTTP_201_CREATED, response_model=CostResponseSchema)
def create_cost_route(
    item: CostCreateSchema,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    return create_cost(item, db, user)


@route.put("/{cost_id}", status_code=status.HTTP_200_OK, response_model=CostResponseSchema)
def edit_cost_route(
    cost_id: int,
    item: CostUpdateSchema,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    return edit_cost(cost_id, item, db, user)


@route.delete("/{cost_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cost_route(
    cost_id: int, db: Session = Depends(get_db), user: UserModel = Depends(get_current_user)
):
    await FastAPICache.clear(namespace="get_cost_by_id_route")
    return delete_cost(cost_id, db, user)
