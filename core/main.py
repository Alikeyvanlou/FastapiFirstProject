from fastapi import FastAPI, status, HTTPException, Query, Path, Depends
from schema.schema import CostCreateSchema, CostResponseSchema, CostUpdateSchema, CostDeleteResponseSchema
from typing import List
from database import SessionLocal, Cost
from sqlalchemy import select
from sqlalchemy.orm import Session

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_cost_or_404(cost_id: int = Path(ge=1), db: Session = Depends (get_db)):
    stmt = select(Cost).where(Cost.id == cost_id)
    cost = db.scalar(stmt)
    if cost:
        return cost
    raise HTTPException(detail='cost not found', status_code=status.HTTP_404_NOT_FOUND)

@app.get('/costs', status_code=status.HTTP_200_OK, response_model=List[CostResponseSchema])
def root(search: str | None = Query(default=None), min_amount: float | None = Query(default=None), 
         max_amount: float | None = Query(default=None), db: Session = Depends (get_db)):
    stmt = select(Cost)
    if search:
        stmt = stmt.where(search.lower() == Cost.description)
    if min_amount is not None:
        stmt = stmt.where(min_amount <= Cost.amount)
    if max_amount is not None:
        stmt = stmt.where(max_amount >= Cost.amount)
    result = db.scalars(stmt).all()
    return result

@app.post('/cost', status_code=status.HTTP_201_CREATED, response_model=CostResponseSchema)
def create_cost(item: CostCreateSchema, db: Session = Depends (get_db)):
    new_cost =  Cost(description= item.description, amount = item.amount)
    db.add(new_cost)
    db.commit()
    db.refresh(new_cost)
    return new_cost

@app.get('/costs/{cost_id}', status_code=status.HTTP_200_OK, response_model=CostResponseSchema)
def read_cost(cost: Cost = Depends (get_cost_or_404)):
    return cost

@app.put('/costs/{cost_id}', status_code=status.HTTP_200_OK, response_model=CostResponseSchema)
def edit_cost(item: CostUpdateSchema, cost: Cost = Depends (get_cost_or_404), db: Session = Depends (get_db)):
    cost.description = item.description
    cost.amount = item.amount
    db.commit()
    db.refresh(cost)
    return cost

@app.delete('/cost/{cost_id}', status_code=status.HTTP_200_OK, response_model=CostDeleteResponseSchema)
def delete_cost(cost: Cost = Depends (get_cost_or_404), db: Session = Depends (get_db)):
    db.delete(cost)
    db.commit()
    return {'message': 'The cost was successfully removed.'}