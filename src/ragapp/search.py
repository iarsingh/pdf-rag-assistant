import hashlib, math, re
STOP = set("the a an is of and to in what why does how".split())
SOURCES = [('policy.pdf', 'The platform refuses latest image tags in production deploys.'), ('other.pdf', 'The lobby wifi password is written on the fridge.')]
SESSIONS = {}

def tokens(text):
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOP]

def bm25(query, docs):
    q, scores = set(tokens(query)), []
    for doc in docs:
        d = tokens(doc)
        scores.append(sum(d.count(t) for t in q))
    return scores

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
    history = SESSIONS.setdefault(session_id or "_", [])
    q = question + " " + " ".join(history[-3:])
    scores = bm25(q, [t for _, t in corpus])
    ranked = sorted(({"source": n, "text": t, "score": sc} for (n, t), sc in zip(corpus, scores)), key=lambda x: -x["score"])
    best = ranked[0]
    history.append(question)
    ok = best["score"] >= 2
    return {"answered": ok, "answer": best["text"] if ok else "No passage shares enough terms.", "citation": best["source"] if ok else None, "passages": ranked[:5]}
