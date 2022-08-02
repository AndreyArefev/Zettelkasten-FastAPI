from fastapi import APIRouter

from . import (
    auth,
    ideas,
)


router = APIRouter()
router.include_router(auth.router)
router.include_router(ideas.router)