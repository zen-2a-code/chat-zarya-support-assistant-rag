# Chat Support Assistant

A customer-support chatbot for a telecom, built with RAG (retrieval-augmented generation).
It answers questions about plans, bills, roaming, devices and router problems from the
company's own PDF documents, shows the page behind every answer, and says "I don't know"
instead of guessing when the answer isn't in the documents.

> **Status: in progress.** I'm building this step by step to learn how RAG systems work
> end to end, and to measure them, not just demo them. Progress is tracked below.

> Zarya Telecom is a made-up company. All documents, plans and prices are fictional.

<!-- Add when ready: live demo link · CI badge · demo GIF -->

## Why I built this

I work as a process automation engineer at a telecom. A lot of customer questions
("Why is my first bill so high?", "Do I pay extra for data in Italy?", "How much is the
new iPhone with my plan?") already have answers somewhere in a PDF. I wanted to see what
it takes to build an assistant that finds those answers reliably, cites them, and knows
when to stay quiet, and to prove it with numbers instead of a few lucky screenshots.

## What it does

- **Answers from documents only:** 6 PDFs (22 pages) covering plans, device prices per
  plan, billing, roaming, technical support and terms of service.
- **Cites its sources:** every answer links back to the file and page it came from.
- **Hybrid search:** combines vector search (meaning) with BM25 keyword search (exact
  plan names, codes and prices), merged with Reciprocal Rank Fusion.
- **Refuses safely:** a similarity check stops off-topic questions before they reach the
  LLM, and the prompt tells the model to admit when it doesn't know.
- **Shows the vectors:** an embedding map plots every chunk in 2D, so you can see where
  a question lands and why it retrieves what it does.
- **Measured:** a hand-labelled test set checks retrieval quality, and CI fails the build
  if it drops.
- **Runs locally for free:** Ollama + Qdrant in Docker. OpenAI can be switched on with
  one setting for the hosted demo.

## How it works

```
INGESTION (runs once)
  PDFs -> remove headers/footers -> split into ~800-char chunks
       -> embed (all-MiniLM-L6-v2, 384 dims) -> store in Qdrant with source + page

QUERY (every question)
  question -> embed -> similarity check (refuse if off-topic)
           -> hybrid search: vector + BM25, fused with RRF -> top 4 chunks
           -> prompt with numbered sources -> LLM (Ollama or OpenAI)
           -> answer + citations in a Streamlit chat
```

## Tech stack

| Part | Tool |
|---|---|
| Embeddings | fastembed, `all-MiniLM-L6-v2` |
| Vector database | Qdrant (Docker locally, Qdrant Cloud for the demo) |
| Keyword search | rank-bm25 |
| LLM | Ollama with Llama 3.2 (local), OpenAI (hosted demo) |
| UI | Streamlit |
| Evaluation | Custom hit rate @4, MRR and refusal checks |
| Ops | Docker Compose, GitHub Actions, pytest, ruff |

## Results

<!-- Fill in with real numbers from `python eval/evaluate.py` and `python eval/refusal.py` -->

Retrieval quality on 27 hand-labelled questions (is the right page in the top 4?):

| Search mode | Hit rate @4 | MRR |
|---|---|---|
| Keyword (BM25) | _coming soon_ | |
| Vector | _coming soon_ | |
| Hybrid (RRF) | _coming soon_ | |

Refusal: _coming soon_ (off-topic questions refused, real questions wrongly refused).

### Where it fails, and why

_Coming soon. I'll list the real misses from the evaluation here, with the reason for each._

## Decisions and trade-offs

_Coming soon: chunk size, hybrid search, the refusal threshold and the local LLM, each
with the reasoning and the numbers behind it._

## Progress

- [ ] Setup: Python venv, Qdrant in Docker, Ollama
- [ ] Ingestion: load, clean, chunk, embed, store
- [ ] Retrieval: vector, keyword and hybrid search
- [ ] Generation with citations and a refusal guardrail
- [ ] Streamlit chat UI with a sources panel
- [ ] Embedding map
- [ ] Evaluation: hit rate, MRR, refusal threshold
- [ ] Docker Compose, CI with a retrieval quality gate
- [ ] Live demo
- [ ] Results and lessons learned in this README

## Run it locally

Requirements: Python 3.12, Docker Desktop, Ollama.
Full setup instructions, including venv and troubleshooting: [docs/SETUP.md](docs/SETUP.md).

**With Docker Compose:**

```bash
cp .env.example .env
ollama pull llama3.2                               # Ollama runs natively on the Mac
docker compose up -d qdrant
docker compose run --rm app python -m src.ingest
docker compose up -d app                           # http://localhost:8501
```

**With a Python virtual environment:**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant
python -m src.ingest
streamlit run src/app.py
```

**Tests and evaluation:**

```bash
pytest -q
python eval/evaluate.py
python eval/refusal.py
```

## Project structure

```
src/        ingestion, embeddings, retrieval, generation, Streamlit app
eval/       test questions, retrieval evaluation, refusal check
tests/      unit tests
data/pdfs/  the Zarya Telecom documents
tools/      script that generates the PDFs
docs/       setup instructions
```

## What's next

- Query rewriting, so follow-up questions like "and in Switzerland?" search correctly
- A reranker for more precise top results
- Answer-level evaluation, not just retrieval
- Bulgarian documents with a multilingual embedding model
- A Java version with LangChain4j

## Author

Stoyan Hristov · [GitHub](https://github.com/zen-2a-code)
