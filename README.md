# PDF RAG Assistant

<!-- project-guide:start -->
## Project guide

[Project architecture](PROJECT_ARCHITECTURE.md) · [Interview questions and answers](INTERVIEW_QA.md)

Use the architecture document for the component diagram, implementation boundaries, and verification entry points. The interview guide includes source-backed answers and project walkthroughs.

### Implementation map

| Component | Responsibility |
| --- | --- |
| [`src/ragapp/main.py`](src/ragapp/main.py) | HTTP handlers: `GET /healthz`, `POST /ask` |
| [`src/ragapp/search.py`](src/ragapp/search.py) | Functions: `tokens`, `bm25`, `answer` |
| [`requirements.txt`](requirements.txt) | Implementation or supporting configuration |
| [`tests/test_rag.py`](tests/test_rag.py) | Executable checks and regression examples |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | GitHub Actions job definitions |
| [`README.md`](README.md) | Project explanations or operating notes |

### Local setup and verification

From the repository root (the commands follow the checked-in manifests):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

To serve the FastAPI application locally, install the server separately if it is not already available:

```bash
python -m pip install uvicorn
PYTHONPATH=src python -m uvicorn ragapp.main:app --reload
```

<!-- project-guide:end -->

Phase 3

Skills: chunking, hashed retrieval, citations

PDF text → chunk → retrieve → answer + citation. Local hashed overlap stands in for embeddings.

```bash
pip install -r requirements.txt
pytest -q
```

Laptop proof. No hosted model. Cluster apply stays false until a human approves.
