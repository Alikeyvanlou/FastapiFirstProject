from fastapi import FastAPI

from routes.cost import route as route_cost
from routes.user import route as route_user

app = FastAPI()

app.include_router(route_user, tags=["User"])
app.include_router(route_cost, tags=["Cost"])
