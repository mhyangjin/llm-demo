from fastapi import APIRouter
from apis.system.api.v1 import health_router as health_v1_router
from apis.semantic.api.v1 import semantic_router as semantic_v1_router

router = APIRouter()
router.include_router(health_v1_router, prefix="/system", tags=["System"])
router.include_router(semantic_v1_router, prefix="/semantic", tags=["Semantic"])