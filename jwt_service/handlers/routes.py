import fastapi as fa

from .v1 import jwt_router


api_router = fa.APIRouter()

api_router.include_router(jwt_router, prefix="/jwt", tags=["jwt"])
