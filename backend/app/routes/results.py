from fastapi import APIRouter

from app.db.vector_store import vector_store
from app.utils.storage import read_results

router = APIRouter(tags=["Results"])


@router.get("/results")
async def get_results():
    """Return all stored analysis results."""
    results = read_results()
    return {
        "results": results,
        "total": len(results),
        "total_vectors": vector_store.get_total_vectors(),
    }


@router.get("/results/{result_id}")
async def get_result_by_id(result_id: str):
    """Return a specific analysis result by ID."""
    results = read_results()
    for result in results:
        if result.get("id") == result_id:
            return result
    return {"error": "Result not found"}
