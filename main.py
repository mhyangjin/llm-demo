from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apis import router
import uvicorn

from app.core.config import settings
from app.core.logger.log import CustomisedJSONFormatter, CustomisedUvicornJSONFormatter
import logging
from app.core.logger import sendyLogger

def init_logformatters(app_: FastAPI) -> None:
    log_level = logging.getLevelName(settings.LOGGER_LOGLEVEL)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(CustomisedJSONFormatter())
    logger = logging.getLogger(f"{settings.PROJECT_NAME}")
    logger.setLevel(log_level)
    if not logger.hasHandlers() :
        logger.addHandler(streamHandler)

    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.setLevel(log_level)
    uvicornStreamHandler = logging.StreamHandler()
    uvicornStreamHandler.setFormatter(CustomisedUvicornJSONFormatter())
    if not uvicorn_logger.hasHandlers() :
        uvicorn_logger.addHandler(uvicornStreamHandler)

@asynccontextmanager
async def lifespan(app_: FastAPI):


    try:
        yield
    finally:
        # Trigger shutdown
        sendyLogger.info("Shutting down FastAPI application and stopping consumers...")
    sendyLogger.info("Shutdown complete.")

class HealthCheckFilter(logging.Filter):
    def __init__(self, *exclude_paths: str):
        super().__init__()
        self.exclude_paths = exclude_paths

    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        return not any(path in msg for path in self.exclude_paths)


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME,
                   docs_url=None,
                   openapi_url=None,
                   redoc_url=None,
                   lifespan=lifespan)

    access_logger = logging.getLogger("uvicorn.access")
    access_logger.addFilter(HealthCheckFilter("/system"))

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.include_router(router)
    init_logformatters(app_=_app)
    sendyLogger.info(f"config: {settings}")

    return _app

app = get_application()

def main():
    uvicorn.run(
            app="main:app",
            host=settings.APP_HOST,
            port=settings.APP_PORT,
            log_config=None,
            reload=settings.UVICORN_RELOAD,
            workers=settings.UVICORN_WORKERS,
    )

if __name__ == "__main__":
    main()
