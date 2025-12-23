# Architecture

## Components (minimal RAG)

1. **FastAPI service** (single container)
   - Ingest: chunk → embed → store (Qdrant)
   - Ask: embed question → retrieve top-k from Qdrant → generate answer → return citations

2. **Qdrant**
   - Stores chunks + embeddings as vectors with payload (`content`, `source`, `chunk_index`, optional metadata).
   - Retrieval is a vector similarity query (cosine).

## Data flow

### Ingest
1. `POST /ingest` (text + optional metadata)
2. Chunking (fixed-size + overlap)
3. Embeddings
4. Upsert N vectors to Qdrant with payload metadata

### Ask
1. `POST /ask` (question)
2. Embed question
3. Retrieve top-k similar chunks from Qdrant
4. Build prompt with:
   - instructions
   - retrieved context (with citations)
   - question
5. Call the LLM
6. Return answer + citations (chunk ids + sources)

## Storage

Qdrant collection:
- Vectors sized to embedding dimension (1536) with cosine metric.
- Payload: `content`, `source`, `chunk_index`, plus user-supplied metadata.

## Deployments

### Local dev
- API via `uvicorn`
- Qdrant locally (e.g., `docker run -p 6333:6333 qdrant/qdrant`) or managed Qdrant Cloud.

### Cloud
- Containerize the FastAPI service (e.g., ECS/Fargate or your platform of choice).
- Use Qdrant Cloud or your own Qdrant deployment; configure URL/API key/collection via env vars.
