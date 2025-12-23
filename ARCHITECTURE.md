# Architecture

## Components (minimal RAG)

1. **FastAPI service** (single container)
   - Ingest: chunk → embed → store (Pinecone)
   - Ask: embed question → retrieve top-k from Pinecone → generate answer → return citations

2. **Pinecone**
   - Stores chunks + embeddings as vectors with metadata (`content`, `source`, `chunk_index`, optional metadata).
   - Retrieval is a vector similarity query (cosine).

## Data flow

### Ingest
1. `POST /ingest` (text + optional metadata)
2. Chunking (fixed-size + overlap)
3. Embeddings
4. Upsert N vectors to Pinecone with metadata

### Ask
1. `POST /ask` (question)
2. Embed question
3. Retrieve top-k similar chunks from Pinecone
4. Build prompt with:
   - instructions
   - retrieved context (with citations)
   - question
5. Call the LLM
6. Return answer + citations (chunk ids + sources)

## Storage

Pinecone index:
- Vectors sized to embedding dimension (1536) with cosine metric.
- Metadata: `content`, `source`, `chunk_index`, plus user-supplied metadata.
- Namespace: configurable (default `default`).

## Deployments

### Local dev
- API via `uvicorn`
- Pinecone (managed) — requires API key and index; auto-created if missing.

### Cloud
- Containerize the FastAPI service (e.g., ECS/Fargate or your platform of choice).
- Pinecone remains managed; configure API key, index name, namespace, cloud/region via env vars.
