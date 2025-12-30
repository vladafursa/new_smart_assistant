# Real-Time Smart Support Assistant

> RAG-powered support platform for real-time knowledgebase automation.

---
## Problem

Support services process thousands of requests each day. \
Agents have to find answers in huge knowledgebases quickly. \
Manual knowledgebase search is slow, inconsistent, and expensive.

---

## Solution

LLM-powered RAG system that:

- Extracts key entities  
- Classifies user requests  
- Summarises incoming questions  
- Retrieves relevant knowledgebase documents 
- Generates contextual responses in real-time
- Provides sources of original documents where the information came from

---

## Architecture Overview

| Layer | Stack |
|-----|-----|
Frontend | React, Tailwind (branch `frontend`) |
Backend | FastAPI, Pinecone, Supabase (branch `backend`) |
ML | HuggingFace APIs + local fallbacks |
Vector DB | Pinecone |
Storage | Supabase |
Configuration | Pydantic Settings (env-driven) |
Observability | Logging, metrics *(in progress)* |

---

## Key Features

- Semantic search & Retrieval-Augmented Generation (RAG)
- CSV / DOCX / PDF document ingestion
- Supabase Dropbox-like storage and web access to documents
- FastAPI production-ready backend
- React + Tailwind frontend UI
- Environment-driven configuration via **Pydantic Settings**
- Local ML fallbacks 
- Chunk deduplication & namespace isolation

---

## Current Status

| Status | Module |
|------|------|
| Completed | File ingestion pipeline |
| Completed | Embeddings & classification |
| Completed | RAG retriever + generator |
| Completed | Supabase storage integration |
| In Progress | Observability & metrics |
| In Progress | Async ingestion workers |
| Planned | Authentication & RBAC (Admin / User / Assistant) |
| Planned | Admin panel |
| Planned | Ticketing system |
| Planned | Response rating & feedback loop |

---

## Screenshots
> *current UI state* \
> *For demonstration purposes only, later it will be updated and made more user-friendly.*

main page:

<img width="1439" height="808" alt="Screenshot 2025-12-31 at 00 50 11" src="https://github.com/user-attachments/assets/dc311eeb-3cd7-4a24-a356-4b72d86b1457" />


dropbox and file storage page:

<img width="1324" height="701" alt="Screenshot 2025-12-31 at 00 50 32" src="https://github.com/user-attachments/assets/1cdc24e0-ca09-4549-a80d-9147de5aafdc" />


---

## Planned Refactoring

- Clean architecture refactor
- Docstrings & typing cleanup
- Centralized exception handling
- Pytest integration & CI pipelines
- Async background workers
- Rate limiting & idempotency keys
- Model versioning & reindex pipelines

---

## Performance Impact

| Metric | Before | After |
|-----|------|------|
Average KB lookup | Minutes | Seconds |
Manual support workload | High | Automated |
Response consistency | Low | High |

---

## Roadmap

| Phase | Focus |
|----|----|
Phase 1 | Production hardening & observability |
Phase 2 | Auth, RBAC, tickets |
Phase 3 | SaaS scaling |

---

## Author - Vlada Fursa
