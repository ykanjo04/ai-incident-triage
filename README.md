# AI Incident Triage

An AI-powered incident triage assistant that analyzes system logs and incident reports, clusters similar issues using embeddings and FAISS, and uses Gemini LLM to generate incident summaries, root cause hypotheses, severity classification, and recommended ownership.

Designed for fintech/trading platforms where fast incident response is critical.

## Architecture

```
Frontend (React + Vite + Tailwind CSS)
    │
    ├── Upload Logs    → POST /upload_logs
    ├── Analyze        → POST /analyze_incident
    └── View Results   → GET  /results
          │
Backend (FastAPI + Python)
    │
    ├── Log Ingestion & Preprocessing
    ├── Gemini Embedding Generation
    ├── FAISS Vector Similarity Search
    └── Gemini 2.5 Flash LLM Analysis
          │
    Returns structured JSON:
    ├── Incident Summary
    ├── Root Cause Hypothesis
    ├── Severity Level (P1-P4)
    ├── Recommended Owner
    └── Next Steps
```

## Tech Stack

- **Backend:** Python 3.11+, FastAPI, FAISS, Google Gemini API
- **Frontend:** React (Vite), Axios, Tailwind CSS
- **AI:** Gemini 2.5 Flash (analysis), Gemini Embedding (vectors)
- **Storage:** Local JSON + FAISS index files

## Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 18+
- Gemini API Key ([Get one here](https://aistudio.google.com/apikey))

### Quick Start (Single Server)

The frontend is pre-built and served directly from FastAPI — only one server needed.

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure API key
copy .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Start server (serves both API and frontend)
uvicorn app.main:app --reload
```

Open http://localhost:8000 — that's it!

### Development Mode (Two Servers)

If you want to develop the frontend with hot-reload:

```bash
# Terminal 1 — Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2 — Frontend (Vite dev server)
cd frontend
npm install
npm run dev
```

Frontend dev server: http://localhost:5173

### Rebuilding the Frontend

After making frontend changes, rebuild the production bundle:

```bash
cd frontend
npm install
npm run build
```

Then restart the backend — it automatically serves the new build.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Google Gemini API key |

## Demo Instructions

1. **Start the server** — `cd backend && uvicorn app.main:app --reload`
2. **Open the dashboard** at http://localhost:8000
3. **Click "Load Demo Logs"** to load realistic fintech incident data
4. **Click "Analyze Incidents"** to trigger AI analysis
5. **View results** — severity badges, root causes, recommended owners

The demo flow takes under 2 minutes.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload_logs` | Upload log messages (JSON body or file) |
| POST | `/upload_demo_logs` | Load pre-built demo logs |
| POST | `/analyze_incident` | Run AI analysis on logs |
| GET | `/results` | Get all analysis results |
| GET | `/results/{id}` | Get a specific analysis result |

## Project Structure

```
ai-incident-triage/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── routes/              # API endpoints
│   │   ├── ai/                  # Embeddings + LLM analysis
│   │   ├── db/                  # FAISS vector store
│   │   ├── models/              # Pydantic data models
│   │   ├── utils/               # Storage + preprocessing
│   │   └── data/                # Demo data + persisted files
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── components/          # React UI components
│       ├── services/api.js      # Backend API client
│       └── App.jsx              # Main application
├── docs/
│   └── architecture.md
└── README.md
```

## Hackathon Alignment

This project demonstrates:
- **AI workflow automation** — LLM-powered incident analysis
- **Incident management optimization** — automated triage and routing
- **Fintech reliability tooling** — trading platform-specific analysis
- **Production-style architecture** — clean separation of concerns

Positioned as: *"AI workflow assistant for engineering incident triage."*
