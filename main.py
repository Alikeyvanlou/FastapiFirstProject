from fastapi import FastAPI
from routes.user import route as route_user
from routes.cost import route as route_cost
from i18n import load_translations

app = FastAPI()

@app.on_event("startup")
def startup_event():
    load_translations()

app.include_router(route_user, tags=["User"])
app.include_router(route_cost, tags=["Cost"])
