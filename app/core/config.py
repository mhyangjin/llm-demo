from typing import Any, Dict, List, Optional, Union
import os
from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    ENV: str = "dev"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    VERSION: str
    UVICORN_RELOAD: bool = True
    UVICORN_WORKERS: int = 1
    DOCKER_HOST: str = "127.0.0.1"

    ##Logger Setting
    LOGGER_LOGLEVEL: str

    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        extra = "ignore"
        env_file = ".env"

settings = Settings()
