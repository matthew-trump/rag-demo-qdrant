from app.rag.chunking import chunk_text


def test_chunk_text_overlapping_slices():
    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chunks = chunk_text(text, chunk_size=8, overlap=2)

    assert [c.index for c in chunks] == [0, 1, 2, 3]
    assert [c.text for c in chunks] == [
        "ABCDEFGH",
        "GHIJKLMN",
        "MNOPQRST",
        "STUVWXYZ",
    ]


def test_chunk_text_handles_large_overlap():
    text = "abcdefghij"
    chunks = chunk_text(text, chunk_size=5, overlap=50)

    assert len(chunks) == 3
    assert chunks[0].text == "abcde"
    assert chunks[-1].text == "ij"


def test_chunk_text_empty_is_safe():
    assert chunk_text("", chunk_size=10, overlap=2) == []
    assert chunk_text("   ", chunk_size=10, overlap=2) == []
