from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import engine, Base, SessionLocal
from app.services.llm_service import create_embedding, generate_answer
from app.services.document_service import save_document
from app.services.rag_service import retrieve_top_chunks
from app.models import Document

# ============================================
# Initialize FastAPI app
# ============================================
app = FastAPI(title="Private Knowledge Q&A")

# ============================================
# CORS (Important for frontend)
# ============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables automatically
Base.metadata.create_all(bind=engine)

# ============================================
# Database Dependency
# ============================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================
# Root Endpoint
# ============================================
@app.get("/")
def root():
    return {"message": "Backend is running"}

# ============================================
# Status Endpoint
# ============================================
@app.get("/status")
def status(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "error"

    try:
        create_embedding("health check")
        llm_status = "connected"
    except Exception:
        llm_status = "error"

    return {
        "backend": "running",
        "database": db_status,
        "llm": llm_status
    }

# ============================================
# List Documents
# ============================================
@app.get("/documents")
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(Document).all()
    return [
        {
            "id": doc.id,
            "name": doc.name
        }
        for doc in docs
    ]

# ============================================
# Delete ALL Documents
# ============================================
@app.delete("/documents")
def delete_all_documents(db: Session = Depends(get_db)):
    try:
        deleted = db.query(Document).delete()
        db.commit()

        return {
            "message": "All documents deleted successfully",
            "deleted_count": deleted
        }

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete documents")

# ============================================
# Delete Single Document (Bonus Feature)
# ============================================
@app.delete("/documents/{doc_id}")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        db.delete(doc)
        db.commit()
        return {"message": f"Document {doc_id} deleted successfully"}

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete document")

# ============================================
# Test Embedding
# ============================================
@app.get("/test-embedding")
def test_embedding():
    emb = create_embedding("Hello world")
    return {"embedding_length": len(emb)}

# ============================================
# Upload Document
# ============================================
@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files allowed")

    content = await file.read()
    text_data = content.decode("utf-8")

    if not text_data.strip():
        raise HTTPException(status_code=400, detail="File is empty")

    try:
        document = save_document(db, file.filename, text_data)
        return {
            "message": "Document uploaded successfully",
            "document_id": document.id
        }

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to save document")

# ============================================
# Ask Question (RAG)
# ============================================
@app.post("/ask")
def ask_question(
    question: str,
    db: Session = Depends(get_db)
):
    if not question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    top_chunks = retrieve_top_chunks(db, question)

    if not top_chunks:
        raise HTTPException(status_code=400, detail="No documents uploaded yet")

    context = "\n\n".join([chunk.content for chunk in top_chunks])

    try:
        answer = generate_answer(context, question)
    except Exception:
        raise HTTPException(status_code=500, detail="LLM generation failed")

    sources = [
        {
            "document_id": chunk.document_id,
            "snippet": chunk.content[:300]
        }
        for chunk in top_chunks
    ]

    return {
        "question": question,
        "answer": answer,
        "sources": sources
    }
