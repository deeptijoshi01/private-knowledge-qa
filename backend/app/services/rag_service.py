import json
import numpy as np
from sqlalchemy.orm import Session
from app.models import Chunk
from app.services.llm_service import create_embedding


def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def retrieve_top_chunks(db: Session, question: str, top_k: int = 3):
    question_embedding = create_embedding(question)

    chunks = db.query(Chunk).all()

    if not chunks:
        return []

    scored_chunks = []

    for chunk in chunks:
        stored_embedding = json.loads(chunk.embedding)
        score = cosine_similarity(question_embedding, stored_embedding)

        scored_chunks.append((chunk, score))

    scored_chunks.sort(key=lambda x: x[1], reverse=True)

    top_chunks = [chunk for chunk, _ in scored_chunks[:top_k]]

    return top_chunks
