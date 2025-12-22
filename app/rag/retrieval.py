from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session
from pgvector.sqlalchemy import Vector

from app.rag.schema import Chunk, Document

def retrieve_top_k(session: Session, query_embedding: list[float], top_k: int) -> list[dict]:
    # Use L2 distance for robustness across pgvector versions (cosine occasionally returns no rows with bound params).
    stmt = (
        select(Chunk.id, Chunk.content, Document.source)
        .join(Document, Document.id == Chunk.document_id)
        .order_by(Chunk.embedding.l2_distance(query_embedding))
        .limit(top_k)
    )
    rows = session.execute(stmt).all()
    return [{"id": r.id, "content": r.content, "source": r.source} for r in rows]
