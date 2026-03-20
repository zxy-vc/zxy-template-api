# zxy-template-api

Boilerplate FastAPI para ventures de ZXY Ventures.

## Stack
- **FastAPI** + Python 3.11
- **Supabase** (PostgreSQL + Auth)
- **Fly.io** para hosting
- **GitHub Actions** para CI/CD
- **Doppler** para secrets

## Arrancar proyecto nuevo

```bash
# 1. Clonar template
git clone https://github.com/zxy-ventures/zxy-template-api zxy-[venture]-api
cd zxy-[venture]-api

# 2. Instalar dependencias
poetry install

# 3. Copiar y llenar variables de entorno
cp .env.example .env
# Editar .env con valores reales (también cargar en Doppler)

# 4. Correr en local
uvicorn app.main:app --reload

# 5. Tests
pytest tests/
```

## Estructura

```
app/
├── main.py        # Entry point
├── config.py      # Settings (pydantic-settings)
├── database.py    # Supabase client
├── routers/       # Endpoints por dominio
├── models/        # Pydantic models
├── services/      # Business logic
└── middleware/    # Auth, logging, cors
```

## Deploy

Push a `main` dispara deploy automático a Fly.io via GitHub Actions.
Requiere `FLY_API_TOKEN` en GitHub Secrets.

## ADR
- [ADR-001: Stack Estándar ZXY](../adr/ADR-001-stack-estandar-zxy.md)
- [ADR-002: Naming Conventions](../adr/ADR-002-naming-conventions.md)
