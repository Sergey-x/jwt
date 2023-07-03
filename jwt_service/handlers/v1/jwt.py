import fastapi as fa
from fastapi.responses import ORJSONResponse

import jwt
from jwt_service.schemas import Credentials, RefreshToken, TokenPair
from jwt_service.services import JWTAccess, JWTRefresh, validate_credentials


api_router = fa.APIRouter()


@api_router.post(
    "/obtain",
    response_class=ORJSONResponse,
    response_model=TokenPair,
    status_code=fa.status.HTTP_200_OK,
    responses={
        fa.status.HTTP_200_OK: {
            "description": "Ok",
        },
        fa.status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
)
async def obtain_token_pair(credentials: Credentials):
    """Получение пары JWT.

    Принимает данные для получения токена (email, password).
    Проверяет, что они существуют и корректны.
    Если корректны вернет токены. Иначе - 401.
    """
    iss: str = await validate_credentials(credentials.dict())

    payload = {
        'iss': iss,
        'email': credentials.email,
    }

    token_pair = {
        "access": JWTAccess.gen_token(payload),
        "refresh": JWTRefresh.gen_token(payload),
    }
    return token_pair


@api_router.post(
    "/refresh",
    response_class=ORJSONResponse,
    response_model=TokenPair,
    status_code=fa.status.HTTP_200_OK,
    responses={
        fa.status.HTTP_200_OK: {
            "description": "Ok",
        },
        fa.status.HTTP_400_BAD_REQUEST: {
            "description": "Refresh token is not valid",
        },
    },
)
async def refresh_token_pair(refresh_token: RefreshToken):
    """Получение новой пары JWT по refresh.

    Принимает refresh токен. Если он валиден - вернет новую пару JWT.
    Иначе - 400.
    """
    token = refresh_token.token

    refresh_token_is_valid = JWTRefresh.validate(token)
    if not refresh_token_is_valid:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail='Refresh token is not valid',
        )

    payload = jwt.decode(token, options={"verify_signature": False})

    token_pair = {
        "access": JWTAccess.gen_token(payload),
        "refresh": JWTRefresh.gen_token(payload),
    }
    return token_pair
