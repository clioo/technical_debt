from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import uvicorn
from api.api_v1.bad.bad_service import bad_router
from core import config
from db.session import create_db_connection
from sqlalchemy.exc import DBAPIError
from utils.decorators import logcemex, warnings_decorator
from utils.misc import obtain_error_code_from_exception
from utils.warnings import add_warning


settings = config.get_settings()


app = FastAPI(
    title=settings.app_name, docs_url="/api/docs", openapi_url="/api"
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    req: Request,
    exc: RequestValidationError
):
    """Handles validation errors, you can customize your needs"""
    pydantic_errors = exc.errors()
    content_response = {
        "detail": pydantic_errors,
        "your_additional_errors": {"Will be inside": "this message"},
    }
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(content_response),
    )


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as ex:
        # you probably want some kind of logging here
        error_code, message = obtain_error_code_from_exception(ex)
        return JSONResponse(
            {"error_code": error_code, 'message': message},
            status_code=status.HTTP_400_BAD_REQUEST
        )


@app.get("/healthcheck")
async def healthcheck():
    return JSONResponse({"message": "OK!"}, status_code=status.HTTP_200_OK)


@app.get("/warning-log-example")
@warnings_decorator
@logcemex(prefix='test-prefix', database='landing')
async def warning_log_example(request: Request):
    add_warning("Test warning!!!")
    return JSONResponse({"message": "OK!"}, status_code=status.HTTP_200_OK)


@app.get("/database/{database_name}")
def obtain_database_healthcheck(database_name: str):
    healtcheck_query = (
        "SELECT SYSDATETIME(), "
        "SYSDATETIMEOFFSET(), "
        "SYSUTCDATETIME(), "
        "CURRENT_TIMESTAMP, "
        "GETDATE(), "
        "GETUTCDATE();"
    )
    connection, connection_time = create_db_connection(database_name)
    is_connection_active = False
    try:
        connection.execute(healtcheck_query)
        is_connection_active = True
    except DBAPIError:
        is_connection_active = False
        connection_time = 0
    res = {
        "database": {
            "connection_name": database_name,
            "time": connection_time,
            "is_connection_active": is_connection_active,
        }
    }
    return JSONResponse(content=res, status_code=status.HTTP_200_OK)


# Routers
app.include_router(service1_router, tags=["your_router_tag"])


# Catching not caught exceptions with a middleware
app.middleware("http")(catch_exceptions_middleware)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
