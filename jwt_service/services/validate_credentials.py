import fastapi as fa
import httpx
import orjson

from jwt_service.settings import SETTINGS


async def validate_credentials(credentials: dict) -> str:
    try:
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.post(
                url=f'http://{SETTINGS.USER_SERVICE_HOSTS}/user/credentials',
                data=orjson.dumps(credentials),  # type: ignore
                headers={'Content-Type': 'application/json'},
            )
    except httpx.ConnectError:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_401_UNAUTHORIZED,
            detail='Connection error! Something went wrong, try later',
        )
    except httpx.ConnectTimeout:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_401_UNAUTHORIZED,
            detail='Timeout! Something went wrong, try later',
        )

    is_valid: bool = response.status_code == fa.status.HTTP_200_OK
    if not is_valid:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect login or password',
        )

    iss: str = response.json().get('userId', None)

    if iss is None:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal error - undefined `userId`',
        )

    return iss
