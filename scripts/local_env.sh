#!/usr/bin/env bash
set -euo pipefail

export DATABASE_URL="${DATABASE_URL:-postgresql+psycopg://rag:rag@localhost:5432/rag}"
export OPENAI_MODEL="${OPENAI_MODEL:-gpt-5}"
export OPENAI_EMBEDDING_MODEL="${OPENAI_EMBEDDING_MODEL:-text-embedding-3-small}"
export CHUNK_SIZE="${CHUNK_SIZE:-800}"
export CHUNK_OVERLAP="${CHUNK_OVERLAP:-120}"
export PINECONE_API_KEY="${PINECONE_API_KEY:-}"
export PINECONE_INDEX="${PINECONE_INDEX:-rag-demo}"
export PINECONE_NAMESPACE="${PINECONE_NAMESPACE:-default}"
export PINECONE_CLOUD="${PINECONE_CLOUD:-aws}"
export PINECONE_REGION="${PINECONE_REGION:-us-east-1}"

echo "PINECONE_INDEX=$PINECONE_INDEX"
echo "PINECONE_NAMESPACE=$PINECONE_NAMESPACE"
