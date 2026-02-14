# AI Usage Notes

This project was built with the assistance of AI tools, as allowed in the assignment instructions.

The goal was not to copy-paste blindly, but to accelerate development while fully understanding the implementation.

---

## 🤖 AI Tools Used

- ChatGPT (architecture guidance, debugging support, UI improvements)
- LLM provider used in application: Groq (LLaMA 3.3 70B)

---

## 🧠 Where AI Was Used

AI assistance was used for:

- Designing the Retrieval-Augmented Generation (RAG) architecture
- Structuring FastAPI endpoints
- Debugging circular import and dependency issues
- Improving frontend UI aesthetics
- Refining documentation structure
- Suggesting clean error handling patterns
- Preparing deployment-ready README

---

## 🔍 What Was Manually Verified

The following were manually implemented, tested, and verified:

- All endpoints tested via Swagger and frontend
- File upload and validation logic
- Embedding generation
- Cosine similarity retrieval logic
- Correct document-source attribution
- Error handling for invalid inputs
- CORS configuration
- Environment variable protection
- No API keys stored in repository

---

## 🏗️ LLM & Embedding Choice

### LLM Provider: Groq (LLaMA 3.3 70B)

Reason:
- Fast inference
- Cost-effective
- Good reasoning performance
- Simple API integration

### Embeddings

- Local embedding generation using sentence-transformers
- Avoided external embedding API to reduce cost and complexity

---

## 🎯 Development Approach

The objective was to:

- Maintain clean separation of services
- Keep code modular and readable
- Ensure the project works end-to-end
- Avoid over-engineering beyond assignment scope
- Demonstrate understanding of RAG principles

---

## ⚠️ Transparency Statement

AI was used as a development assistant, not as a replacement for understanding.

All major architectural decisions and integrations were reviewed, tested, and validated manually.

