# pdf-rag-assistant — interview questions and answers

[README](README.md) · [Project architecture](PROJECT_ARCHITECTURE.md)

Answers below use this repository’s files and implementation. They distinguish existing behavior from suggested extensions; source links let you verify each walkthrough.

## 1. What problem does pdf-rag-assistant address, and what can you demonstrate?

PDF text → chunk → retrieve → answer + citation. Local hashed overlap stands in for embeddings.

I would demonstrate the linked implementation or examples and distinguish that evidence from any planned production features. Start with [`README.md`](README.md).

## 2. How is this repository organized?

- [`src/ragapp/main.py`](src/ragapp/main.py): Implementation or supporting configuration.
- [`src/ragapp/search.py`](src/ragapp/search.py): Implementation or supporting configuration.
- [`requirements.txt`](requirements.txt): Implementation or supporting configuration.
- [`tests/test_rag.py`](tests/test_rag.py): Executable checks and regression examples.
- [`.github/workflows/ci.yml`](.github/workflows/ci.yml): GitHub Actions job definitions.
- [`README.md`](README.md): Project explanations or operating notes.

[PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) contains the component diagram and the implementation walkthrough.

## 3. Can you walk through `answer` and explain the decision it makes?

The main walkthrough here is `answer(question, source=None, session_id=None, tenant=None)` in [`src/ragapp/search.py`](src/ragapp/search.py#L16).

```python
def answer(question, source=None, session_id=None, tenant=None):
    if not question or not str(question).strip():
        raise ValueError("question is empty")
    corpus = SOURCES
    if source:
        corpus = [s for s in corpus if s[0] == source]
        if not corpus:
            raise ValueError("unknown source")
    if tenant:
        corpus = [s for s in corpus if s[0].startswith(tenant) or tenant in s[0]]
    history = []
    if session_id:
        history = SESSIONS.setdefault(session_id, [])
        q = question + " " + " ".join(history[-3:])
    else:
        q = question
    scores = bm25(q, [t for _, t in corpus])
    ranked = sorted(({"source": n, "text": t, "score": sc} for (n, t), sc in zip(corpus, scores)), key=lambda x: -x["score"])
    best = ranked[0]
    if session_id:
```

This is an excerpt; follow the source link for the rest of the branches.

The implementation calls `' '.join`, `SESSIONS.setdefault`, `ValueError`, `bm25`, `history.append`, `s[0].startswith`, `sorted`, `str`, `str(question).strip`. In an interview, trace those calls in execution order using a fixture input.

## 4. What responsibility does `bm25` have?

`bm25(query, docs)` is defined in [`src/ragapp/search.py`](src/ragapp/search.py#L9).

Its return expressions include:

- `scores`

It uses `d.count`, `scores.append`, `set`, `sum`, `tokens`. This is the code path I would compare against the caller to explain responsibility boundaries.

## 5. What input validation and failure behavior are implemented?

Explicit failure paths include:

- `HTTPException(422, str(exc))` in [`src/ragapp/main.py`](src/ragapp/main.py#L14).
- `ValueError('question is empty')` in [`src/ragapp/search.py`](src/ragapp/search.py#L18).
- `ValueError('unknown source')` in [`src/ragapp/search.py`](src/ragapp/search.py#L23).

I would test both the condition that reaches each exception and the caller that translates it. An explicit raise does not mean every malformed input or dependency failure is handled.

## 6. Which test would you use to demonstrate correctness?

[`tests/test_rag.py`](tests/test_rag.py#L5) contains `test_hit_and_miss`:

```python
def test_hit_and_miss():
    hit = client.post("/ask", json={"question": 'Why does the platform refuse latest tags in production?'}).json()
    assert hit["answered"] is True
    assert hit["citation"] == 'policy.pdf'
    miss = client.post("/ask", json={"question": "orbital cafeteria soup"}).json()
    assert miss["answered"] is False
```

This is a concrete regression example from the repository. Its assertions establish that case; they do not establish behavior for every input or under production load.

## 7. What HTTP interface does the code expose?

- `GET /healthz` → `healthz` in [`src/ragapp/main.py`](src/ragapp/main.py#L6).
- `POST /ask` → `ask` in [`src/ragapp/main.py`](src/ragapp/main.py#L10).

These are literal decorators. Application/router prefixes, authentication, and middleware must be checked in the corresponding setup code.

## 8. Where does state live, and what happens with multiple workers?

Module-level containers include `STOP`, `SOURCES`, `SESSIONS` in [`src/ragapp/search.py`](src/ragapp/search.py).

These containers belong to a Python process. Inspect which are constant fixtures and which are mutated. Mutable process state needs an explicit shared-storage or synchronization strategy before multiple workers can provide consistent behavior.

## 9. How would another engineer reproduce your walkthrough?

Start from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

These commands follow repository manifests; environment setup and command results still need to be checked on the target machine.

## 10. What does automation verify, and what does it not prove?

Inspect [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for triggers, permissions, and job commands. I would name the checks that those definitions run and show the latest run separately. A workflow definition alone does not establish a successful deployment, security review, or production SLO.

## 11. How would you present this project in a Forward Deployed Engineer interview?

Start with the user and operational problem described in [`README.md`](README.md). Explain one constraint that changes the implementation, show the linked code or example, and walk through a success case and a failure case. Agree on a measurable acceptance criterion before expanding the solution, and leave a handoff with data boundaries and rollback ownership. Any proposed production or business metric should be identified as a target until measured.

## 12. What is the input-to-output contract of `answer`?

In [`src/ragapp/search.py`](src/ragapp/search.py#L16), `answer(question, source=None, session_id=None, tenant=None)` receives the inputs. The function computes these intermediate values:

- `corpus = SOURCES`
- `history = []`
- `scores = bm25(q, [t for _, t in corpus])`
- `ranked = sorted(({'source': n, 'text': t, 'score': sc} for (n, t), sc in zip(corpus, scores)), key=lambda x: -x['score'])`
- `best = ranked[0]`
- `ok = best['score'] >= 1`

Its result is defined by:

- `{'answered': ok, 'answer': best['text'] if ok else 'No passage shares enough terms.', 'citation': best['source'] if ok else None, 'passages': ranked[:5]}`

## 13. Which decision rules or boundary conditions should an interviewer challenge?

The implementation in [`src/ragapp/search.py`](src/ragapp/search.py#L16) branches on:

- `not question or not str(question).strip()`
- `source`
- `tenant`
- `session_id`
- `session_id`
- `not corpus`

A useful extension is a table-driven test that covers each condition just below, at, and above its boundary where applicable. These expressions are the current rules; changing them changes behavior and should be justified by the project’s acceptance criteria.
