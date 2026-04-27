from fastapi import APIRouter
from app.schemas import RAGIngestRequest, RAGSearchRequest
from app.rag.vector_store import ingest_text, search

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.post("/ingest")
def ingest(req: RAGIngestRequest):
    success = ingest_text(req.text, req.metadata)
    return {"success": success, "message": "Ingested" if success else "FAISS unavailable"}


@router.post("/search")
def rag_search(req: RAGSearchRequest):
    results = search(req.query, k=req.k)
    return {"query": req.query, "results": results, "count": len(results)}
