from __future__ import annotations

import hashlib
from functools import lru_cache
from typing import Iterable

from pinecone import Pinecone, ServerlessSpec

from app.rag.schema import EMBEDDING_DIM
from app.rag.settings import settings
from app.rag.chunking import ChunkedText


class PineconeNotConfiguredError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def _client() -> Pinecone:
    if not settings.pinecone_api_key:
        raise PineconeNotConfiguredError("PINECONE_API_KEY is not set")
    return Pinecone(api_key=settings.pinecone_api_key)


@lru_cache(maxsize=1)
def get_index():
    pc = _client()
    indexes = {idx["name"]: idx for idx in pc.list_indexes()}
    if settings.pinecone_index not in indexes:
        pc.create_index(
            name=settings.pinecone_index,
            dimension=EMBEDDING_DIM,
            metric="cosine",
            spec=ServerlessSpec(cloud=settings.pinecone_cloud, region=settings.pinecone_region),
        )
    return pc.Index(settings.pinecone_index)


def _chunk_id(source: str, chunk: ChunkedText) -> str:
    digest = hashlib.sha1(f"{source}-{chunk.index}-{chunk.text}".encode("utf-8")).hexdigest()[:12]
    return f"{source}-{chunk.index}-{digest}"


def upsert_chunks(chunks: Iterable[ChunkedText], embeddings: list[list[float]], source: str, metadata: dict) -> int:
    index = get_index()
    vectors = []
    for chunk, emb in zip(chunks, embeddings, strict=True):
        vectors.append(
            {
                "id": _chunk_id(source, chunk),
                "values": emb,
                "metadata": {
                    "content": chunk.text,
                    "source": source,
                    "chunk_index": chunk.index,
                    **(metadata or {}),
                },
            }
        )
    if not vectors:
        return 0
    index.upsert(vectors=vectors, namespace=settings.pinecone_namespace)
    return len(vectors)


def query_top_k(query_embedding: list[float], top_k: int) -> list[dict]:
    index = get_index()
    res = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        namespace=settings.pinecone_namespace,
    )
    hits: list[dict] = []
    for match in res.matches or []:
        md = match.metadata or {}
        hits.append(
            {
                "id": match.id,
                "content": md.get("content", ""),
                "source": md.get("source", "unknown"),
                "score": match.score,
            }
        )
    return hits
