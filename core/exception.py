from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException


class CostNotFoundError(Exception):
    def __init__(self, cost_id):
        self.cost_id = cost_id


async def cost_not_found_handler(request: Request, exc: CostNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "status_code": 404,
            "error": {
                "message": f"No cost with id {exc.cost_id} was found.",
                "path": request.url.path,
            },
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "status_code": exc.status_code,
            "error": {"message": exc.detail, "path": request.url.path},
        },
        headers=exc.headers,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [{"filed": err["loc"][-1], "message": err["msg"]} for err in exc.errors()]
    return JSONResponse(
        status_code=422,
        content={"success": False, "status_code": 422, "error": errors},
    )
