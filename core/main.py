from fastapi import FastAPI, status, HTTPException, Query, Path
from schema.schema import CastCreate, CastResponse, CastUpdate, CastDeleteResponse
from typing import List

app = FastAPI()

data = {
    1: {'id': 1, 'description': 'shopping for home', 'amount': 102.5},
    2: {'id': 2, 'description': 'grocery shopping', 'amount': 75.0},
    3: {'id': 3, 'description': 'electricity bill', 'amount': 45.8},
    4: {'id': 4, 'description': 'internet bill', 'amount': 30.0},
    5: {'id': 5, 'description': 'transportation', 'amount': 25.5},
    6: {'id': 6, 'description': 'restaurant', 'amount': 60.0}
}

@app.get('/cast', status_code=status.HTTP_200_OK, response_model=List[CastResponse])
def root(search: str | None = Query(default=None), min_amount: float | None = Query(default=None), max_amount: float | None = Query(default=None)):
    result = list(data.values())
    if search:
        result = [c for c in result if search.lower() in c['description'].lower()]
    if min_amount is not None:
        result = [c for c in result if c['amount'] >= min_amount]
    if max_amount is not None:
        result = [c for c in result if c['amount'] <= max_amount]
    return result

@app.post('/cast', status_code=status.HTTP_201_CREATED, response_model=CastResponse)
def create_cast(item: CastCreate):
    new_id = max((item for item in data), default=0) + 1
    new_cast = {'id': new_id, 'description': item.description, 'amount': item.amount}
    data[new_id]= new_cast
    return new_cast

@app.get('/cast/{cast_id}', status_code=status.HTTP_200_OK, response_model=CastResponse)
def read_cast(cast_id: int = Path(ge=1)):
    if cast_id in data:
        return data[cast_id]
    raise HTTPException(detail='cast not found', status_code=status.HTTP_404_NOT_FOUND)

@app.put('/cast/{cast_id}', status_code=status.HTTP_200_OK, response_model=CastResponse)
def edit_cast(item: CastUpdate, cast_id: int = Path(ge=1)):
    if cast_id in data:
        data[cast_id] = {'id': cast_id, 'description': item.description, 'amount' : item.amount}
        return data[cast_id]
    raise HTTPException(detail='cast not found', status_code=status.HTTP_404_NOT_FOUND)

@app.delete('/cast/{cast_id}', status_code=status.HTTP_200_OK, response_model=CastDeleteResponse)
def delete_cast(cast_id: int = Path(ge=1)):
    if cast_id in data:
        data.pop(cast_id)
        return {'message': 'The cost was successfully removed.'}
    raise HTTPException(detail='cast not found', status_code=status.HTTP_404_NOT_FOUND)
