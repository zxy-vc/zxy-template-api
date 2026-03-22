from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.config import settings
from app.logging_config import configure_logging, get_logger
from app.middleware.rate_limit import limiter
from app.routers import health, payments

# ── Logging ───────────────────────────────────────────────────────────────────
configure_logging(environment=settings.ENVIRONMENT)
logger = get_logger(__name__)

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
)

# ── Rate limiting ─────────────────────────────────────────────────────────────
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(health.router, tags=["health"])
app.include_router(payments.router, tags=["payments"])


# ── Root ──────────────────────────────────────────────────────────────────────
@app.get("/")
@limiter.limit("60/minute")
async def root(request: Request):
    logger.info("root_ping", env=settings.ENVIRONMENT)
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.ENVIRONMENT}
