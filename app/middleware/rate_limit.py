"""
Rate limiting middleware using slowapi (wraps limits library).

Limits:
  - General routes:  60 requests/minute per IP
  - Auth routes:     10 requests/minute per IP
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

# Shared limiter instance — import this wherever you need @limiter.limit()
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])

# Stricter limit string for auth/sensitive endpoints
AUTH_RATE_LIMIT = "10/minute"
