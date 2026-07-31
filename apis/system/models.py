# ==============================================================================
#    Predefined types
# ------------------------------------------------------------------------------
# Predefined types
from pydantic import BaseModel
from app.core.config import settings
# ==============================================================================
#    DTOs
# ------------------------------------------------------------------------------
# Requests

# ------------------------------------------------------------------------------
# Responses
class SystemRes(BaseModel):
    service_name:str=settings.PROJECT_NAME
    port: int = settings.APP_PORT
    version:str=settings.VERSION
    host:str=settings.DOCKER_HOST
    log_level:str=settings.LOGGER_LOGLEVEL
    uvicorn_workers:int = settings.UVICORN_WORKERS
# ==============================================================================
