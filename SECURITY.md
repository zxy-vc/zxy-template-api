# ZXY Security Checklist

> Baseline security posture for every API in the ZXY portfolio.  
> Status key: ✅ Implemented in this boilerplate · ⚠️ Manual / env-specific · ❌ Not applicable

---

## Authentication & Authorization

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 1 | **Rate limiting on all endpoints** | ✅ | `slowapi` — 60 req/min general, 10/min for auth routes (`app/middleware/rate_limit.py`) |
| 2 | **Rate limiting on auth/login routes** | ✅ | `AUTH_RATE_LIMIT = "10/minute"` — apply with `@limiter.limit(AUTH_RATE_LIMIT)` |
| 3 | **No API keys / secrets exposed to the frontend** | ⚠️ | `STRIPE_PUBLISHABLE_KEY` is the only key intended for the client. All others stay server-side. Verify before each deploy. |
| 4 | **JWT / session tokens verified server-side** | ⚠️ | Boilerplate has no auth router yet. Add Supabase JWT verification middleware when adding user routes. |
| 5 | **Role-based access control (RBAC)** | ⚠️ | Not implemented. Add Supabase RLS policies and FastAPI dependency guards per route. |

---

## Input & Data

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 6 | **Input validation with Pydantic** | ✅ | All request bodies use `BaseModel` — automatic type coercion and validation. |
| 7 | **Input sanitization (XSS / injection)** | ⚠️ | Pydantic rejects wrong types; add explicit sanitization (e.g., `bleach`) for any user-supplied HTML/text stored or rendered. |
| 8 | **SQL injection prevention** | ⚠️ | Using Supabase SDK (parameterized queries). Never build raw SQL strings from user input. |
| 9 | **File upload validation** | ❌ | No file upload endpoints in this boilerplate. Add mime-type + size checks if added. |
| 10 | **Sensitive data never logged** | ⚠️ | `structlog` is configured (`app/logging_config.py`). Review every log call — never log passwords, tokens, or PII. |

---

## Stripe / Payments

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 11 | **Stripe webhook signature verification** | ✅ | `stripe.Webhook.construct_event()` used in `app/routers/payments.py` — rejects unsigned/tampered payloads. |
| 12 | **Stripe secret key server-side only** | ✅ | `STRIPE_SECRET_KEY` loaded from env via `pydantic-settings`, never exposed in responses. |
| 13 | **Idempotent webhook processing** | ⚠️ | TODO: store processed `event.id` in DB to prevent double-fulfillment on retries. |
| 14 | **Checkout amount set server-side** | ✅ | Price is looked up by `price_id` — client cannot dictate the amount. |

---

## Infrastructure & Secrets

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 15 | **Secrets in environment variables, not source code** | ✅ | `pydantic-settings` + `.env` file. `.env` is git-ignored. `.env.example` provided. |
| 16 | **HTTPS enforced in production** | ⚠️ | Handled at infra level (Fly.io TLS / reverse proxy). Verify `ALLOWED_ORIGINS` contains only `https://` in production. |
| 17 | **CORS restricted to known origins** | ✅ | `ALLOWED_ORIGINS` list in config — defaults to `localhost:3000`. Update per environment. |
| 18 | **Docs endpoint disabled in production** | ✅ | `docs_url=None` when `ENVIRONMENT=production` (`app/main.py`). |
| 19 | **Structured / auditable logging** | ✅ | `structlog` with JSON output in production, human-readable in dev (`app/logging_config.py`). |
| 20 | **Dependency pinning & vulnerability scanning** | ⚠️ | `pyproject.toml` uses `^` ranges. Add `pip-audit` or Dependabot to CI for CVE scanning. |

---

## How to use this checklist

1. Copy it into every new ZXY API repo.
2. Update status column after each sprint.
3. All ⚠️ items must be resolved before a production launch — create a GitHub Issue for each.
4. Tag security PRs with the `security` label.

---

*Last updated: 2026-03-22 — ZXY Ventures Tech Team*
