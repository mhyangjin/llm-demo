import os
from fastapi import APIRouter
from ..models import SystemRes
from http import HTTPStatus
from starlette.responses import JSONResponse

health_router = APIRouter()


@health_router.get("")
async def get_system():
    if os.path.exists("/MAINTENANCE"):
        return JSONResponse(status_code=HTTPStatus.SERVICE_UNAVAILABLE, content={"message": "MAINTENANCE_MODE"})
    return SystemRes()

@health_router.get("/health")
async def get_health():
    return SystemRes()

