import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

load_dotenv()

from app.db.vector_store import vector_store  # noqa: E402
from app.routes.upload import router as upload_router  # noqa: E402
from app.routes.analysis import router as analysis_router  # noqa: E402
from app.routes.results import router as results_router  # noqa: E402

# Path to frontend build
FRONTEND_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "frontend",
    "dist",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load FAISS index if it exists
    vector_store.load_index()
    yield
    # Shutdown: save FAISS index
    vector_store.save_index()


app = FastAPI(
    title="AI Incident Triage",
    description="AI-powered incident triage assistant for fintech/trading platforms",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS (still useful during development with separate Vite dev server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers (must be BEFORE the frontend catch-all)
app.include_router(upload_router)
app.include_router(analysis_router)
app.include_router(results_router)


@app.get("/api/health")
async def health():
    return {"message": "AI Incident Triage API is running"}


# Serve frontend static files from the Vite build output
if os.path.exists(FRONTEND_DIR):
    # Mount the assets directory for JS/CSS bundles
    assets_dir = os.path.join(FRONTEND_DIR, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="static-assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve the React SPA — any non-API route returns index.html."""
        # Try to serve the exact file first (e.g. vite.svg, favicon)
        file_path = os.path.join(FRONTEND_DIR, full_path)
        if full_path and os.path.isfile(file_path):
            return FileResponse(file_path)
        # Otherwise serve the SPA entry point
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
