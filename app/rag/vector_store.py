import os
from loguru import logger
from langchain_core.documents import Document
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter  # fallback
from app.core.config import settings


_EMBEDDING_MODEL = "models/gemini-embedding-001"


def _get_embeddings():
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    return GoogleGenerativeAIEmbeddings(
        model=_EMBEDDING_MODEL,
        google_api_key=settings.GOOGLE_API_KEY,
    )


def _get_or_create_store():
    """Load existing FAISS index or create new one."""
    try:
        from langchain_community.vectorstores import FAISS
    except ImportError:
        from langchain.vectorstores import FAISS

    path = settings.FAISS_INDEX_PATH
    embeddings = _get_embeddings()

    if os.path.exists(path) and os.path.exists(os.path.join(path, "index.faiss")):
        try:
            store = FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
            logger.info(f"Loaded existing FAISS index from {path}")
            return store
        except Exception as e:
            logger.warning(f"Failed to load FAISS index: {e}. Creating fresh index.")

    docs = [Document(page_content="Financial AI Agent initialized.", metadata={"source": "init"})]
    store = FAISS.from_documents(docs, embeddings)
    os.makedirs(path, exist_ok=True)
    store.save_local(path)
    logger.info("Created new FAISS index.")
    return store


_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
_store = None
_store_failed = False  


def _load_store():
    global _store, _store_failed
    if _store_failed:
        return None
    if _store is None:
        try:
            _store = _get_or_create_store()
        except Exception as e:
            logger.error(f"Could not initialize FAISS store: {e}. RAG will be skipped.")
            _store_failed = True 
    return _store


def ingest_text(text: str, metadata: dict = None) -> bool:
    """Add text to FAISS vector store."""
    store = _load_store()
    if store is None:
        logger.warning("FAISS store unavailable — skipping ingest.")
        return False
    try:
        docs = _splitter.create_documents([text], metadatas=[metadata or {}])
        store.add_documents(docs)
        store.save_local(settings.FAISS_INDEX_PATH)
        return True
    except Exception as e:
        logger.error(f"FAISS ingest failed: {e}")
        return False


def search(query: str, k: int = 5) -> list[dict]:
    """Search FAISS for semantically similar documents."""
    store = _load_store()
    if store is None:
        return []
    try:
        results = store.similarity_search(query, k=k)
        return [{"content": doc.page_content, "metadata": doc.metadata} for doc in results]
    except Exception as e:
        logger.error(f"FAISS search failed: {e}")
        return []
