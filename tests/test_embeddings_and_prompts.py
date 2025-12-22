from app.rag import embeddings, llm, prompts
from app.rag.schema import EMBEDDING_DIM
from app.rag.settings import settings


def test_embed_texts_mock_mode_is_deterministic(monkeypatch):
    monkeypatch.setattr(settings, "openai_api_key", None)

    emb1 = embeddings.embed_texts(["hello"])[0]
    emb2 = embeddings.embed_texts(["hello"])[0]
    emb3 = embeddings.embed_texts(["world"])[0]

    assert emb1 == emb2
    assert emb1 != emb3
    assert len(emb1) == EMBEDDING_DIM
    assert all(-1.0001 <= v <= 1.0001 for v in emb1)


def test_build_context_block_formats_citations():
    chunks = [
        {"id": 1, "source": "file:a.txt", "content": "alpha"},
        {"id": 2, "source": "manual", "content": "beta"},
    ]

    block = prompts.build_context_block(chunks)

    assert block.count("[chunk:") == 2
    assert "[chunk:1] source=file:a.txt" in block
    assert "alpha" in block
    assert block.strip().endswith("beta")


def test_generate_answer_mock_uses_context_preview(monkeypatch):
    monkeypatch.setattr(settings, "openai_api_key", None)

    context = "context line " * 30
    answer = llm.generate_answer("What is this?", context)

    assert "MOCK MODE ANSWER" in answer
    assert "What is this?" in answer
    assert "Context preview" in answer
    assert context[:20].strip() in answer
