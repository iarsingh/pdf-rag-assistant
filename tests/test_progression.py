from ragapp.progression import pdf_rag

def test_pdf_rag_cites_chunk():
    out = pdf_rag("latest image tags", ["The platform refuses latest image tags in production."])
    assert out["answered"] is True
    assert out["citation"]
    assert out["hosted_llm"] is False

