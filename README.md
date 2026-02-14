# Private Knowledge Q&A
A mini workspace web application built using FastAPI and a Retrieval-Augmented Generation (RAG) pipeline.

This project allows users to upload documents, ask questions about them, and see exactly which document snippet contributed to the answer.

Built as part of a Full-stack Developer evaluation task.

---

# 🌐 Live Demo

Live App: <ADD YOUR LIVE LINK HERE>  
GitHub Repo: <ADD YOUR REPO LINK HERE>

---

# 🚀 Features

## ✅ Core Requirements (Problem Statement A)

✔ Upload text documents (.txt)  
✔ View list of uploaded documents  
✔ Ask a question  
✔ Generate AI-based answer  
✔ Show sources (document ID + snippet)  
✔ Home page with clear steps  
✔ System status page (Backend, DB, LLM health)  
✔ Basic error handling (empty input, invalid file)  
✔ Clear document list  
✔ Clean and aesthetic UI  

---

# 🧠 Architecture Overview

This application uses a Retrieval-Augmented Generation (RAG) pattern.

### Flow:

1. User uploads a document
2. Document is split into chunks
3. Embeddings are generated for each chunk
4. Chunks are stored in database
5. User asks a question
6. Question embedding is generated
7. Most relevant chunks are retrieved
8. Context is sent to LLM
9. Answer is generated
10. Sources are returned

---

# 🏗️ Tech Stack

## Backend
- FastAPI
- SQLAlchemy
- SQLite
- Groq LLM API
- Embedding-based similarity retrieval

## Frontend
- HTML
- CSS (Neon Black + Sky Blue UI)
- Vanilla JavaScript (Fetch API)

---

# 📂 Project Structure
backend/
app/
database.py
models.py
services/
llm_service.py
document_service.py
rag_service.py
text_splitter.py
main.py

frontend/
index.html
script.js
style.css

.env.example
requirements.txt
README.md
AI_NOTES.md
ABOUTME.md
PROMPTS_USED.md


---

# ⚙️ How to Run Locally

## 1️⃣ Clone Repository

```bash
git clone <repo-url>
cd <repo-folder>

python -m venv venv
venv\Scripts\activate   # Windows


INSTALL DEPENDENCIES
pip install -r requirements.txt

Setup Environment Variables
create .env 

GROQ_API_KEY=your_key_here
DATABASE_URL=sqlite:///./app.db

RUN COMMAND - BACKEND
uvicorn app.main:app --reload

FRONTEND - frontend/index.html



