from fastapi import FastAPI, status, HTTPException, Query, Path

app = FastAPI()

data = {
    1: {'id': 1, 'description': 'shopping for home', 'amount': 102.5},
    2: {'id': 2, 'description': 'grocery shopping', 'amount': 75.0},
    3: {'id': 3, 'description': 'electricity bill', 'amount': 45.8},
    4: {'id': 4, 'description': 'internet bill', 'amount': 30.0},
    5: {'id': 5, 'description': 'transportation', 'amount': 25.5},
    6: {'id': 6, 'description': 'restaurant', 'amount': 60.0}
}

@app.get('/cast', status_code=status.HTTP_200_OK)
def root():
    return data

@app.post('/cast/', status_code=status.HTTP_201_CREATED)
def create_cast(description: str =Query(min_length=2, max_length=50), amount: float = Query(gt=0.1)):
    new_id = max((item for item in data), default=0) + 1
    new_cast = {'id': new_id, 'description': description, 'amount': amount}
    data[new_id]= new_cast
    return new_cast

@app.get('/cast/{cast_id}', status_code=status.HTTP_200_OK)
def read_cast(cast_id: int = Path(ge=1)):
    if cast_id in data:
        return data[cast_id]
    raise HTTPException(detail='cast not found', status_code=status.HTTP_404_NOT_FOUND)

@app.put('/cast/{cast_id}', status_code=status.HTTP_200_OK)
def edit_cast(cast_id: int = Path(ge=1), description: str = Query(min_length=2, max_length=50), amount: float = Query(gt=0.1)):
    if cast_id in data:
        data[cast_id] = {'id': cast_id, 'description': description, 'amount' : amount}
        return data[cast_id]
    raise HTTPException(detail='cast not found', status_code=status.HTTP_404_NOT_FOUND)

@app.delete('/cast/{cast_id}', status_code=status.HTTP_200_OK)
def delete_cast(cast_id: int = Path(ge=1)):
    if cast_id in data:
        return data.pop(cast_id)
    raise HTTPException(detail='cast not found', status_code=status.HTTP_404_NOT_FOUND)
