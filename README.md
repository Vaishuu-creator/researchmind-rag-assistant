# AI Research Paper Assistant (RAG + LLM)

An AI-powered research assistant that can read research papers and answer questions with citations.

## Features

- Upload research papers
- Ask questions about papers
- Multi-document retrieval
- Paper comparison
- Citation tracking
- Chat-style UI

## Tech Stack

- Python
- LangChain
- OpenAI GPT-4o-mini
- FAISS Vector Database
- Streamlit
- Retrieval-Augmented Generation (RAG)

## Architecture

PDF → Chunking → Embeddings → Vector Database → Retriever → LLM → Answer

```mermaid
flowchart TD

A[User - Streamlit UI] --> B[Question Input]

B --> C[Retriever]
C --> D[FAISS Vector Database]

subgraph Document Ingestion Pipeline
E[PDF]
E --> F[Text Extraction]
F --> G[Text Chunking]
G --> H[OpenAI Embeddings]
H --> D
end

D --> I[Relevant Paper Chunks]

I --> J[LLM - GPT-4o-mini]

J --> K[Answer Generation]

K --> L[Answer + Citations]
```

