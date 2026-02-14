import json
from sqlalchemy.orm import Session
from app.models import Document, Chunk
from app.utils.text_splitter import split_text
from app.services.llm_service import create_embedding


def save_document(db: Session, file_name: str, text: str):
    # Save document record
    document = Document(name=file_name)
    db.add(document)
    db.commit()
    db.refresh(document)

    # Split into chunks
    chunks = split_text(text)

    for chunk_text in chunks:
        embedding = create_embedding(chunk_text)

        chunk = Chunk(
            document_id=document.id,
            content=chunk_text,
            embedding=json.dumps(embedding)
        )

        db.add(chunk)

    db.commit()

    return document
