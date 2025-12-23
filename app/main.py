import logging
from fastapi import FastAPI
from app.rag.api import router as rag_router
from app.rag.settings import settings

app = FastAPI(title="rag-demo", version="0.1.0")
logger = logging.getLogger(__name__)

# Ensure our module logs show up when running under uvicorn.
logging.basicConfig(level=logging.INFO)

@app.on_event("startup")
def _startup() -> None:
    logger.info(
        "Starting with mode=%s, pinecone_index=%s, pinecone_namespace=%s",
        settings.mode,
        settings.pinecone_index,
        settings.pinecone_namespace,
    )

@app.get("/health")
def health() -> dict:
    return {"status": "ok", "mode": settings.mode}

app.include_router(rag_router)
