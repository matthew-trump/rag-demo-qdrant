# Repository Guidelines

## Project Structure & Module Organization
- `app/main.py` is the FastAPI entrypoint; `app/rag/` holds core modules (`api.py` routes, `db.py`/`schema.py` for Postgres + pgvector, `chunking.py`, `embeddings.py`, `retrieval.py`, `llm.py`, `prompts.py`, `settings.py`).
- `data/` contains sample `.txt` files for `/ingest_dir`.
- `docker/` has the service `Dockerfile`; `docker-compose.yml` starts Postgres (and the API when built).
- `infra/terraform/aws/` provisions the AWS stack (ECR/ECS/RDS/ALB); `scripts/` includes helpers like `ecr_build_push.sh`.
- Python version is pinned to 3.13.1 (`.python-version`), dependencies in `requirements.txt`.

## Build, Test, and Development Commands
- Start Postgres locally: `docker compose up -d postgres`
- Create venv + install: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
- Run API locally (hot reload): `uvicorn app.main:app --reload --port 8011`
- Local Docker (linux/arm64 optimized): `docker compose up --build`
- AWS infra: `cd infra/terraform/aws && terraform init && terraform apply`; push image: `./scripts/ecr_build_push.sh <ecr_repo> <tag>`
- Set env: `DATABASE_URL` required; `OPENAI_API_KEY` optional (mock mode without it); see `.env.example`/`scripts/local_env.sh` for defaults.

## Coding Style & Naming Conventions
- Python 3.13, PEP 8, 4-space indent; favor type hints (as in `settings.py`), snake_case for modules/functions, UPPER_SNAKE for constants/env keys.
- Keep FastAPI routers lean; push logic into `app/rag/*` helpers. Use SQLAlchemy sessions via `SessionLocal()` context to avoid leaks.
- Imports ordered stdlib → third-party → local. Keep docstrings/comments minimal and focused on non-obvious behavior.

## Testing Guidelines
- Prefer `pytest`; place tests under `tests/` mirroring `app/rag/` modules. Use mock mode (omit `OPENAI_API_KEY`) for deterministic outputs.
- For endpoint checks, hit a running dev server with `curl` (see README examples) and include relevant request/response payloads.
- Aim to cover chunking, retrieval, and prompt construction; avoid making tests depend on live OpenAI.

## Commit & Pull Request Guidelines
- Recent history uses concise, present-tense messages (e.g., `chore: pin python version 3.13.1`); follow that style and keep scope narrow.
- In PRs, provide: summary of behavior change, commands run (`uvicorn`, `pytest`, `docker compose`, etc.), config/env changes, and screenshots or sample `curl` responses for API-facing changes.
- Link related issues/tasks when applicable and note any follow-up work or known gaps.

## Security & Configuration Tips
- Do not commit secrets; use `.env` locally and environment variables in deploys. Mock mode prevents accidental OpenAI spend.
- Postgres schema/extension are created on startup; ensure the DB user can run `CREATE EXTENSION vector` in non-mock environments.
