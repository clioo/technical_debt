from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status


bad_router = APIRouter(prefix="/api/v1/bad")


@bad_router.get("/healthcheck")
def get_bad_healthcheck():
    # Do your healthcheck for your specific service here
    return JSONResponse(
        content={'message': 'OK!'},
        status_code=status.HTTP_200_OK
    )
