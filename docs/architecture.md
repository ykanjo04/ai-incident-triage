# Architecture

## System Overview

AI Incident Triage is a full-stack application with three main layers:

### 1. Frontend (React)

A single-page dashboard built with React, Vite, and Tailwind CSS. Provides:
- Log upload interface (text paste, file upload, demo data)
- One-click AI analysis trigger
- Incident result cards with severity badges

### 2. Backend API (FastAPI)

RESTful API handling:
- **Log Ingestion:** Accepts JSON, CSV, and plain text logs. Cleans and validates input.
- **Embedding Generation:** Converts log text to 768-dimensional vectors using Gemini Embedding API.
- **Vector Storage:** Stores embeddings in a FAISS index for similarity search.
- **LLM Analysis:** Sends log context + similar incidents to Gemini 2.5 Flash for structured analysis.
- **Result Storage:** Persists analysis results as JSON.

### 3. AI Layer

**Embeddings + FAISS:**
- Each log entry is converted to a vector using `models/embedding-001`
- Vectors stored in `faiss.IndexFlatL2` for L2 distance similarity search
- Similar incidents provide contextual grounding for LLM analysis

**LLM Analysis (Gemini 2.5 Flash):**
- Structured prompt with log data + similar incident context
- Returns JSON with: summary, root cause, severity (P1-P4), owner, next steps
- Low temperature (0.1) for deterministic output
- Retry logic with graceful fallback

## Data Flow

```
User uploads logs
  → Backend cleans/validates input
  → Gemini Embedding API generates vectors
  → Vectors stored in FAISS index
  → User clicks "Analyze"
  → FAISS finds similar past incidents
  → Gemini 2.5 Flash analyzes logs + context
  → Structured JSON result returned
  → Dashboard displays incident cards
```

## Storage

All data persisted locally:
- `backend/app/data/logs.json` — stored log messages
- `backend/app/data/results.json` — analysis results
- `backend/app/data/faiss_index.bin` — FAISS vector index
- `backend/app/data/faiss_metadata.json` — vector-to-text mapping
- `backend/app/data/demo_logs.json` — pre-built demo data
