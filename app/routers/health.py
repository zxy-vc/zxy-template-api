from datetime import datetime, timezone

from fastapi import APIRouter, Request

from app.config import settings
from app.middleware.rate_limit import limiter

router = APIRouter()


@router.get("/health")
@limiter.limit("60/minute")
async def health_check(request: Request):
    """Returns service health with version, environment and timestamp."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
