from __future__ import annotations

from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.rag.settings import settings
from app.rag.db import SessionLocal
from app.rag.schema import Document, Chunk
from app.rag.chunking import chunk_text
from app.rag.embeddings import embed_texts
from app.rag.retrieval import retrieve_top_k
from app.rag.prompts import build_context_block
from app.rag.llm import generate_answer

router = APIRouter()

class IngestRequest(BaseModel):
    source: str = "manual"
    text: str = Field(min_length=1)
    metadata: dict = Field(default_factory=dict)

class AskRequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=4, ge=1, le=20)

@router.post("/ingest")
def ingest(req: IngestRequest) -> dict:
    chunks = chunk_text(req.text, settings.chunk_size, settings.chunk_overlap)
    if not chunks:
        raise HTTPException(status_code=400, detail="No content to ingest after cleaning.")

    embeddings = embed_texts([c.text for c in chunks])

    with SessionLocal() as session:
        doc = Document(source=req.source, meta=req.metadata)
        session.add(doc)
        session.flush()  # assign doc.id

        for c, emb in zip(chunks, embeddings, strict=True):
            session.add(Chunk(document_id=doc.id, chunk_index=c.index, content=c.text, embedding=emb))

        session.commit()

    return {"ok": True, "document_source": req.source, "chunks_ingested": len(chunks), "mode": settings.mode}

@router.post("/ask")
def ask(req: AskRequest) -> dict:
    q_emb = embed_texts([req.question])[0]

    with SessionLocal() as session:
        hits = retrieve_top_k(session, q_emb, req.top_k)

    context = build_context_block(hits)
    answer = generate_answer(req.question, context)

    return {
        "answer": answer,
        "citations": [{"chunk_id": h["id"], "source": h["source"]} for h in hits],
        "mode": settings.mode,
        "top_k": req.top_k,
    }

@router.post("/ingest_dir")
def ingest_dir() -> dict:
    data_dir = Path("data")
    if not data_dir.exists():
        raise HTTPException(status_code=404, detail="data/ directory not found in container/workdir.")

    texts: list[tuple[str, str]] = []
    for p in sorted(data_dir.glob("*.txt")):
        texts.append((p.name, p.read_text(encoding="utf-8", errors="ignore")))

    if not texts:
        raise HTTPException(status_code=400, detail="No .txt files found in data/.")

    total_chunks = 0
    with SessionLocal() as session:
        for filename, body in texts:
            chunks = chunk_text(body, settings.chunk_size, settings.chunk_overlap)
            if not chunks:
                continue
            embeddings = embed_texts([c.text for c in chunks])

            doc = Document(source=f"file:{filename}", meta={"filename": filename})
            session.add(doc)
            session.flush()

            for c, emb in zip(chunks, embeddings, strict=True):
                session.add(Chunk(document_id=doc.id, chunk_index=c.index, content=c.text, embedding=emb))
            total_chunks += len(chunks)

        session.commit()

    return {"ok": True, "files": [t[0] for t in texts], "chunks_ingested": total_chunks, "mode": settings.mode}
