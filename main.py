from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from core.config import settings
from core.exception import (
    CostNotFoundError,
    cost_not_found_handler,
    http_exception_handler,
    validation_exception_handler,
)
from routes.cost import route as route_cost
from routes.user import route as route_user

@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.TESTING:
        import fakeredis.aioredis
        redis = fakeredis.aioredis.FakeRedis()
    else:
        redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis),prefix="fastapi_cache")
    yield
    await redis.close()
    if not settings.TESTING:
        await redis.connection_pool.disconnect()
                      

app = FastAPI(lifespan=lifespan)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(CostNotFoundError, cost_not_found_handler)


app.include_router(route_user, tags=["User"])
app.include_router(route_cost, tags=["Cost"])
