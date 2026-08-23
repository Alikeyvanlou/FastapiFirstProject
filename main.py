from fastapi import FastAPI
from routes.user import route as route_user
from routes.cost import route as route_cost

app = FastAPI()

app.include_router(route_user, tags=["User"])
app.include_router(route_cost, tags=["Cost"])
