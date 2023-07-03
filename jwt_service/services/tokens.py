import abc
from datetime import datetime, timedelta, timezone

import jwt
from jwt_service.settings import SETTINGS


class BaseJWT(abc.ABC):
    _ALGORITHM: str = "HS256"
    duration: timedelta | None
    token_type: str | None

    @classmethod
    def validate(cls, token: str) -> bool:
        try:
            jwt.decode(token, SETTINGS.JWT_SECRET_KEY, algorithms=[cls._ALGORITHM])
            return True
        except jwt.exceptions.InvalidTokenError:
            return False

    @classmethod
    def _get_exp_time(cls) -> int:
        if cls.duration is None:
            raise ValueError("Property `duration` must be specified!")
        return int((datetime.now(timezone.utc) + cls.duration).timestamp())

    @classmethod
    def _populate_payload(cls, credentials: dict) -> dict:
        credentials["exp"] = cls._get_exp_time()
        credentials["token_type"] = cls.token_type
        return credentials

    @classmethod
    def gen_token(cls, credentials: dict) -> str:
        if cls.duration is None or cls.token_type is None:
            raise ValueError("Property `duration` and `token_type` must be specified!")

        payload = cls._populate_payload(credentials)
        return jwt.encode(payload, SETTINGS.JWT_SECRET_KEY, algorithm=cls._ALGORITHM)


class JWTAccess(BaseJWT):
    duration = timedelta(minutes=5)
    token_type = 'access'


class JWTRefresh(BaseJWT):
    duration = timedelta(days=30)
    token_type = 'refresh'
