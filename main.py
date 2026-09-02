from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from core.exception import (
    CostNotFoundError,
    cost_not_found_handler,
    http_exception_handler,
    validation_exception_handler,
)
from routes.cost import route as route_cost
from routes.user import route as route_user

app = FastAPI()

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(CostNotFoundError, cost_not_found_handler)


app.include_router(route_user, tags=["User"])
app.include_router(route_cost, tags=["Cost"])
