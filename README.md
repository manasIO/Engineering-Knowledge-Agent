# Engineering Knowledge Assistant

A lightweight engineering knowledge retrieval system built to ingest internal documentation, generate embeddings, store them in a vector database, and answer questions with grounded retrieval-augmented generation (RAG). The repository is designed to showcase an infrastructure-style architecture: data is transformed from raw documentation into searchable knowledge chunks that can be served to a local or hosted LLM for answer generation.

## Architecture Overview

The repository follows a straightforward pipeline from document intake to answer generation. A recruiter or technical reviewer should be able to understand the system in under five seconds from this flow:

```text
┌──────────────────────┐
│  Ingestion Pipeline   │
│  - read docs          │
│  - chunk text         │
│  - normalize metadata │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Embedding Generation  │
│ SentenceTransformers │
│ all-MiniLM-L6-v2     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Vector Storage        │
│ ChromaDB (persistent)│
│ indexed document     │
│ chunks + metadata    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ Retrieval + RAG / Local Model Layer   │
│ - semantic similarity retrieval       │
│ - top-k document chunk selection      │
│ - prompt assembly for answer generation│
│ - local or hosted LLM inference       │
└──────────────────────────────────────┘
```

At a high level:

- Documentation files in `data/documents/` are read and segmented into chunks.
- Each chunk is embedded with a sentence-transformer model.
- Embeddings are upserted into a persistent ChromaDB collection.
- Retrieval queries fetch the most relevant chunks.
- The retrieved context is passed into a model for answer synthesis and grounded response generation.

## Key Technical Features

- Hybrid Retrieval: Combining semantic vector search with keyword/lexical matching to improve recall and precision when a user asks targeted engineering questions. The architecture supports a weighted retrieval strategy that favors semantic similarity while still preserving exact-match and lexical signals from the source documents.

- Local LLM Integration: Designed for private, low-latency inference workflows using local model runtimes such as Ollama, llama.cpp, or custom wrappers. This enables privacy-first developer use cases and low-latency experimentation without depending exclusively on external APIs.

- Context Window Management & Chunking Strategies: Text is split into manageable, semantically meaningful chunks with controlled overlap to reduce context degradation, improve retrieval relevance, and keep prompts within a model's effective context window. The repository emphasizes chunk-level retrieval to preserve grounding and keep the answer focused on the most relevant document fragments.

- Persistent Vector Knowledge Store: ChromaDB is used as a durable, local vector index, allowing the knowledge base to be rebuilt or reused without reprocessing all raw content on every session.

- RAG-First Response Generation: Retrieved documents are assembled into a prompt context and passed to an LLM to answer questions using only available source material, reducing hallucination risk and improving trust in engineering knowledge retrieval.

## Tech Stack

The repository uses a lightweight Python-based stack optimized for local experimentation and controlled knowledge retrieval:

- Python 3.12
- Custom Python orchestration for ingestion, retrieval, and generation
- SentenceTransformers for embedding generation
- ChromaDB for persistent vector storage and similarity search
- Google GenAI SDK for model-based answer generation
- `python-dotenv` for local environment configuration
- Optional local inference backends for future/alternative deployment: Ollama, llama.cpp, or custom model wrappers
- Optional retrieval augmentation patterns aligned with LangChain or LlamaIndex concepts, but implemented here as a minimal, explicit custom pipeline

## Repository Structure

```text
.
├── app/
│   ├── ingest.py          # document ingestion and embedding creation
│   ├── retrieve.py        # vector retrieval for question answering
│   ├── generate.py        # prompt assembly and answer generation
│   └── visualize_chromadb.py
├── data/
│   └── documents/         # source documentation used for RAG ingestion
├── chroma_db/             # persistent ChromaDB storage
├── evaluation/            # validation and assessment artifacts
├── notes/                 # project notes and working documents
├── scripts/               # operational scripts and automation helpers
├── tests/                 # project validation tests
├── requirements.txt       # Python dependencies
├── README.md              # repository overview and architecture
└── .gitignore             # workspace exclusions
```

## Example Workflow

1. Add or update documents in `data/documents/`.
2. Run the ingestion pipeline to split content and generate embeddings.
3. Store the indexed chunk metadata and vectors in ChromaDB.
4. Query the vector store with a user question.
5. Pass the best matching chunks to the response model.
6. Return a grounded answer based only on the retrieved documentation.

## Operational Notes

This project is intentionally simple and transparent: the goal is to demonstrate how an engineering knowledge system can be built from raw internal docs into a searchable, retrieval-backed assistant. It is suitable for developer tooling, internal documentation search, runbooks, SRE playbooks, and other knowledge-intensive workflows.

## Getting Started

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the ingestion step:

```bash
python app/ingest.py
```

Run retrieval manually:

```bash
python app/retrieve.py
```

Run the generation flow:

```bash
python app/generate.py
```

The repository is designed to be extended with hybrid retrieval policies, local model providers, and richer chunking strategies as the knowledge base grows.
