from functools import lru_cache

import pydantic as pd

from jwt_service.enums import Stages


def validate_env_var(varname, v):
    if not v:
        raise ValueError(f"`{varname}` variable is empty")
    return v


class Settings(pd.BaseSettings):
    STAGE: Stages = Stages.PROD
    JWT_SECRET_KEY: str = 'kXpBmV^_|BFq#c.-""B:cd#k6-/EuVp]'
    USER_SERVICE_HOSTS: str | None

    @pd.validator("JWT_SECRET_KEY")
    def validate_secret_not_empty(cls, v: str):
        return validate_env_var('JWT_SECRET_KEY', v)

    @pd.validator("USER_SERVICE_HOSTS")
    def validate_user_service_not_empty(cls, v: str, values: dict):
        if values.get('STAGE', '') == Stages.TEST:
            return ''
        return validate_env_var('USER_SERVICE_HOSTS', v)

    class Config:
        env_file = '.env'


@lru_cache
def get_settings() -> Settings:
    return Settings()


SETTINGS: Settings = get_settings()
