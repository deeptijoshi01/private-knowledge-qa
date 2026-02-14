from groq import Groq
from sentence_transformers import SentenceTransformer
from app.config import GROQ_API_KEY, MODEL

groq_client = Groq(api_key=GROQ_API_KEY)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embedding(text: str):
    embedding = embedding_model.encode(text)
    return embedding.tolist()


def generate_answer(context: str, question: str):
    prompt = f"""
You must answer ONLY using the provided context.
If the answer is not in the context, say "Not found in documents."

Context:
{context}

Question:
{question}
"""

    response = groq_client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
