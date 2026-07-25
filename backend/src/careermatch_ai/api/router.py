from fastapi import APIRouter

from careermatch_ai.api.routes.auth import router as auth_router
from careermatch_ai.api.routes.health import router as health_router
from careermatch_ai.api.routes.resumes import router as resumes_router


api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(resumes_router)
