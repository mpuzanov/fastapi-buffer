from fastapi import APIRouter

from . import (
    auth,
    buffer,
    tables,
    reports,
)


router = APIRouter()
router.include_router(auth.router)
router.include_router(tables.router)
router.include_router(buffer.router)
router.include_router(reports.router)
