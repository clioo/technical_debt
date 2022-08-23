from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status


good_router = APIRouter(prefix="/api/v1/good")


@good_router.get("/healthcheck")
def get_service1_healthcheck():
    # Do your healthcheck for your specific service here
    return JSONResponse(
        content={'message': 'OK!'},
        status_code=status.HTTP_200_OK
    )
