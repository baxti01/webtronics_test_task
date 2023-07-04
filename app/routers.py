from fastapi import APIRouter

from app.auth import auth_router
from app.posts import posts_router

router = APIRouter()

router.include_router(auth_router.router)
router.include_router(posts_router.router)
