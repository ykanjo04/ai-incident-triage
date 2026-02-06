import uuid
from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException

from app.ai.embeddings import generate_query_embedding
from app.ai.llm_analysis import analyze_incident
from app.db.vector_store import vector_store
from app.models.incident import AnalysisResult, AnalyzeRequest
from app.utils.storage import read_logs, save_result

router = APIRouter(tags=["Analysis"])


@router.post("/analyze_incident")
async def analyze(request: AnalyzeRequest):
    """Analyze an incident using AI.

    Flow:
    1. Retrieve logs (from request or storage)
    2. Find similar incidents using FAISS
    3. Send context to Gemini LLM
    4. Return structured analysis
    """
    # Determine logs to analyze
    logs: List[str] = []

    if request.logs:
        logs = request.logs
    elif request.query:
        logs = [request.query]
    else:
        # Use the most recent stored logs
        stored_logs = read_logs()
        if stored_logs:
            logs = stored_logs[-20:]  # Last 20 logs
        else:
            raise HTTPException(
                status_code=400,
                detail="No logs provided and no stored logs found. Upload logs first.",
            )

    # Find similar incidents using FAISS
    similar_incidents = []
    if vector_store.get_total_vectors() > 0:
        try:
            # Create a combined query from logs
            query_text = " ".join(logs[:5])  # Use first 5 logs for query
            query_embedding = generate_query_embedding(query_text)
            similar_results = vector_store.search_similar(query_embedding, k=5)
            similar_incidents = [text for text, _ in similar_results]
        except Exception as e:
            print(f"Warning: FAISS search failed: {e}")

    # Analyze with LLM
    analysis = analyze_incident(logs, similar_incidents if similar_incidents else None)

    # Build result
    result = AnalysisResult(
        id=str(uuid.uuid4()),
        logs=logs,
        similar_incidents=similar_incidents if similar_incidents else None,
        analysis=analysis,
        created_at=datetime.now().isoformat(),
    )

    # Persist result
    save_result(result.model_dump())

    return result
