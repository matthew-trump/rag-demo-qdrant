#!/usr/bin/env bash
set -euo pipefail

export DATABASE_URL="${DATABASE_URL:-postgresql+psycopg://rag:rag@localhost:5432/rag}"
export OPENAI_MODEL="${OPENAI_MODEL:-gpt-5}"
export OPENAI_EMBEDDING_MODEL="${OPENAI_EMBEDDING_MODEL:-text-embedding-3-small}"
export CHUNK_SIZE="${CHUNK_SIZE:-800}"
export CHUNK_OVERLAP="${CHUNK_OVERLAP:-120}"
export QDRANT_URL="${QDRANT_URL:-http://localhost:6333}"
export QDRANT_API_KEY="${QDRANT_API_KEY:-}"
export QDRANT_COLLECTION="${QDRANT_COLLECTION:-rag-demo}"

echo "QDRANT_URL=$QDRANT_URL"
echo "QDRANT_COLLECTION=$QDRANT_COLLECTION"
