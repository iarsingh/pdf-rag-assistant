# PDF RAG Assistant

Phase 3

Skills: chunking, hashed retrieval, citations

PDF text → chunk → retrieve → answer + citation. Local hashed overlap stands in for embeddings.

```bash
pip install -r requirements.txt
pytest -q
```

Laptop proof. No hosted model. Cluster apply stays false until a human approves.
