import json
from typing import Optional

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.ai.embeddings import generate_embeddings_batch
from app.db.vector_store import vector_store
from app.models.incident import LogUploadRequest
from app.utils.preprocessing import (
    clean_text,
    parse_csv_logs,
    parse_text_logs,
    sanitize_input,
    validate_file_content,
)
from app.utils.storage import read_json, save_logs

router = APIRouter(tags=["Upload"])


@router.post("/upload_logs")
async def upload_logs(
    request: Optional[LogUploadRequest] = None,
    file: Optional[UploadFile] = File(None),
):
    """Upload logs for processing.

    Accepts:
    - JSON body with list of log strings
    - CSV file upload
    - Text file upload
    """
    logs = []

    # Handle file upload
    if file:
        content = await file.read()
        content_str = content.decode("utf-8", errors="ignore")

        if not validate_file_content(content_str):
            raise HTTPException(status_code=400, detail="Invalid or empty file content")

        content_str = sanitize_input(content_str)

        if file.filename and file.filename.endswith(".csv"):
            logs = parse_csv_logs(content_str)
        elif file.filename and file.filename.endswith(".json"):
            try:
                parsed = json.loads(content_str)
                if isinstance(parsed, list):
                    logs = [clean_text(str(item)) for item in parsed if item]
                else:
                    raise HTTPException(
                        status_code=400, detail="JSON file must contain a list of logs"
                    )
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON file")
        else:
            # Treat as plain text
            logs = parse_text_logs(content_str)

    # Handle JSON body
    elif request and request.logs:
        logs = [clean_text(sanitize_input(log)) for log in request.logs if log.strip()]

    if not logs:
        raise HTTPException(status_code=400, detail="No valid logs provided")

    # Store logs
    save_logs(logs)

    # Generate embeddings and add to FAISS
    try:
        embeddings = generate_embeddings_batch(logs)
        num_added = vector_store.add_vectors(embeddings, logs)
    except Exception as e:
        # Logs are saved but embeddings failed - still return success
        print(f"Warning: Embedding generation failed: {e}")
        num_added = 0

    return {
        "status": "success",
        "logs_received": len(logs),
        "embeddings_stored": num_added,
        "total_vectors": vector_store.get_total_vectors(),
    }


@router.post("/upload_demo_logs")
async def upload_demo_logs():
    """Load pre-built demo logs for quick demonstration."""
    demo_logs = read_json("demo_logs.json")

    if not demo_logs:
        raise HTTPException(status_code=404, detail="Demo logs not found")

    # Store logs
    save_logs(demo_logs)

    # Generate embeddings and add to FAISS
    try:
        embeddings = generate_embeddings_batch(demo_logs)
        num_added = vector_store.add_vectors(embeddings, demo_logs)
    except Exception as e:
        print(f"Warning: Embedding generation failed: {e}")
        num_added = 0

    return {
        "status": "success",
        "logs_received": len(demo_logs),
        "embeddings_stored": num_added,
        "total_vectors": vector_store.get_total_vectors(),
    }
