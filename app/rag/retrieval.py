from __future__ import annotations

from app.rag.vector_store import query_top_k

def retrieve_top_k(query_embedding: list[float], top_k: int) -> list[dict]:
    return query_top_k(query_embedding, top_k)
