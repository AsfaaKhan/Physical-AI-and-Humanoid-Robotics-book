# Implementation Plan: RAG Knowledge Ingestion Pipeline for Docusaurus Book

**Branch**: `001-rag-ingestion` | **Date**: 2025-12-13 | **Spec**: [link](spec.md)
**Input**: Feature specification from `/specs/001-rag-ingestion/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a complete RAG knowledge ingestion pipeline that extracts content from the deployed Docusaurus book website (https://physical-ai-and-humanoid-robotics-book-p71goqgvj.vercel.app/), chunks it for semantic retrieval, generates Cohere embeddings, and stores them in Qdrant Cloud with proper metadata for downstream RAG-based question answering.

## Technical Context

**Language/Version**: Python 3.11+ (required for uv package manager compatibility)
**Primary Dependencies**: `uv` for dependency management, `requests` for HTTP requests, `BeautifulSoup4` for HTML parsing, `cohere` for embeddings, `qdrant-client` for vector database operations, `python-dotenv` for environment configuration
**Storage**: Qdrant Cloud vector database with local configuration files
**Testing**: pytest for unit and integration testing
**Target Platform**: Linux/macOS/Windows server environment for running the ingestion pipeline
**Project Type**: Backend service (single Python application)
**Performance Goals**: Process 100+ pages within 10 minutes, generate embeddings under 1 second per chunk
**Constraints**: Must use Cohere for embeddings (not OpenAI), Qdrant Cloud Free Tier, and be compatible with future FastAPI integration
**Scale/Scope**: Handle book with 50-100 pages, 1000-5000 content chunks, each with metadata
**Target Site**:https://physical-ai-and-humanoid-robotics-book-p71goqgvj.vercel.app/
**SiteMap URL**:https://physical-ai-and-humanoid-robotics-book-p71goqgvj.vercel.app/sitemap.xml

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ **Accuracy & Reliability**: Pipeline will extract content directly from the deployed book, ensuring source accuracy
- ✅ **Reproducibility & Transparency**: Code will be well-documented with clear functions and logging
- ✅ **Technical Standards Compliance**: Will use Qdrant Cloud as specified in constitution (Section 45)
- ✅ **Unified Source of Truth**: Pipeline will only extract from the specified book website, maintaining single source of truth
- ✅ **Safety & Ethical Responsibility**: No safety concerns for ingestion pipeline itself, but will handle errors gracefully

## Project Structure

### Documentation (this feature)

```text
specs/001-rag-ingestion/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── pyproject.toml          # uv project configuration
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── main.py                # Main ingestion pipeline with: get_all_urls, extract_text_from_urls, chunk_text, embed, create_collection, save_chunks_to_qdrant
├── requirements.txt       # Dependencies list
├── config/
│   └── settings.py        # Configuration management
├── src/
│   ├── __init__.py
│   ├── crawler.py         # URL discovery and content fetching
│   ├── extractor.py       # Text extraction and cleaning
│   ├── chunker.py         # Text chunking logic
│   ├── embedder.py        # Embedding generation
│   └── storage.py         # Qdrant storage operations
└── tests/
    ├── __init__.py
    ├── test_crawler.py
    ├── test_extractor.py
    ├── test_chunker.py
    ├── test_embedder.py
    └── test_storage.py
```

**Structure Decision**: Option 2: Backend service structure chosen. The pipeline will be organized as a Python project inside a `backend/` directory as specified in user requirements, with proper separation of concerns using dedicated modules for each function.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
