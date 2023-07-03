import fastapi as fa

from jwt_service.handlers import api_router
from jwt_service.settings import SETTINGS


def get_app() -> fa.FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = "Микросервис для генерации JWT."

    application = fa.FastAPI(
        title="JWT generator",
        description=description,
        docs_url="/swagger",
        openapi_url="/openapi",
        version="0.1.0",
    )

    application.include_router(api_router)
    application.state.settings = SETTINGS
    return application


app = get_app()
