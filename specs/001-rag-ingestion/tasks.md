# Tasks: RAG Knowledge Ingestion Pipeline for Docusaurus Book

**Feature**: RAG Knowledge Ingestion Pipeline for Docusaurus Book
**Created**: 2025-12-13
**Branch**: 001-rag-ingestion
**Input**: specs/001-rag-ingestion/spec.md, plan.md, data-model.md, research.md

## Implementation Strategy

**MVP Approach**: Implement User Story 1 (Content Extraction and Storage) first as it's the foundational capability. This will provide a working pipeline that can crawl the website, extract clean content, and store it. Subsequent stories will build upon this foundation.

**Incremental Delivery**: Each user story phase produces a testable increment of functionality that can be validated independently.

## Dependencies

- **User Story 2** (Chunking) requires User Story 1 (Content Extraction) as it depends on having content to chunk
- **User Story 3** (Embedding & Storage) requires User Story 1 and 2 as it needs both content and chunked data
- All user stories depend on foundational setup tasks

## Parallel Execution Examples

**Per Story**:
- **US1**: Crawler implementation can run in parallel with content extractor
- **US2**: Chunking algorithm can be developed in parallel with testing utilities
- **US3**: Embedding generation can run in parallel with Qdrant storage implementation

## Phase 1: Setup

**Goal**: Create project structure and configure dependencies

- [X] T001 Create backend directory structure
- [X] T002 Initialize Python project with uv
- [X] T003 [P] Create pyproject.toml with dependencies (requests, beautifulsoup4, cohere, qdrant-client, python-dotenv, pytest)
- [X] T004 [P] Create .env with required environment variables
- [X] T005 [P] Create .gitignore for Python project
- [X] T006 [P] Create requirements.txt based on pyproject.toml
- [X] T007 Create config/settings.py for environment configuration

## Phase 2: Foundational

**Goal**: Implement core configuration and utility components that all user stories depend on

- [X] T008 Create src/__init__.py
- [X] T009 Create config/settings.py with environment variable loading
- [X] T010 [P] Create src/utils.py with helper functions (logging, validation, etc.)
- [X] T011 Create tests/__init__.py
- [X] T012 Create basic test configuration for pytest

## Phase 3: User Story 1 - Content Extraction and Storage (Priority: P1)

**Goal**: Extract clean textual content from deployed Docusaurus book website and store it in structured format

**Independent Test Criteria**: Configure crawler with book website URL, run extraction process, verify output contains clean text without UI elements like navigation bars, footers, or menu items

- [X] T013 [US1] Create src/crawler.py with get_all_urls function to discover all book pages
- [X] T014 [P] [US1] Create src/extractor.py with extract_text_from_urls function
- [X] T015 [P] [US1] Implement sitemap parsing to identify all public URLs from https://physical-ai-and-humanoid-robotics-book-p71goqgvj.vercel.app/sitemap.xml
- [X] T016 [P] [US1] Implement recursive crawling to validate all public URLs of the deployed Docusaurus book
- [X] T017 [P] [US1] Implement HTML content fetching with proper headers and rate limiting
- [X] T018 [P] [US1] Implement content extraction using BeautifulSoup4 to extract main textual content only
- [X] T019 [P] [US1] Implement cleaning logic to remove navigation, headers, footers, and other UI components
- [X] T020 [P] [US1] Create ContentChunk data model based on data-model.md specifications
- [X] T021 [P] [US1] Add validation to ensure extracted text is clean (no nav, footer, or UI noise)
- [X] T022 [P] [US1] Implement error handling for website unavailability with retries
- [X] T023 [US1] Create tests for crawler functionality (test_crawler.py)
- [X] T024 [US1] Create tests for content extraction (test_extractor.py)

## Phase 4: User Story 2 - Semantic Content Chunking (Priority: P2)

**Goal**: Chunk extracted content into semantically coherent segments optimized for retrieval

**Independent Test Criteria**: Take extracted content and apply chunking algorithm, verify chunks maintain semantic coherence and logical boundaries

- [X] T025 [US2] Create src/chunker.py with chunk_text function using recursive character split
- [X] T026 [P] [US2] Implement chunking strategy with 512-1024 token size and 50-100 token overlap
- [X] T027 [P] [US2] Implement logic to respect sentence and paragraph boundaries when possible
- [X] T028 [P] [US2] Add validation to ensure chunks maintain paragraph integrity and semantic coherence
- [X] T029 [P] [US2] Add support for preserving section headings within chunks where possible
- [X] T030 [US2] Create tests for chunking functionality (test_chunker.py)
- [X] T031 [P] [US2] Validate that 90% of chunks preserve paragraph and section boundaries appropriately

## Phase 5: User Story 3 - Vector Embedding Generation and Storage (Priority: P3)

**Goal**: Generate Cohere embeddings and store in Qdrant Cloud with proper metadata

**Independent Test Criteria**: Generate embeddings for sample text chunks, store in Qdrant, perform similarity searches to verify retrieval works correctly

- [X] T032 [US3] Create src/embedder.py with embed function using Cohere embedding models
- [X] T033 [P] [US3] Implement Cohere client initialization with proper API key handling
- [X] T034 [P] [US3] Create src/storage.py with create_collection function for rag_embedding_physical_ai_book
- [X] T035 [P] [US3] Implement create_collection function to configure Qdrant with proper schema (1024 dimensions, cosine similarity)
- [X] T036 [P] [US3] Create save_chunks_to_qdrant function to store embeddings with metadata
- [X] T037 [P] [US3] Implement proper metadata storage (source URL, page title, chunk index, unique IDs)
- [X] T038 [P] [US3] Add validation to ensure embeddings have consistent dimensions
- [X] T039 [P] [US3] Implement error handling for Qdrant Cloud unavailability with retries
- [X] T040 [P] [US3] Implement batch operations for efficient storage
- [X] T041 [US3] Create tests for embedding functionality (test_embedder.py)
- [X] T042 [US3] Create tests for storage functionality (test_storage.py)

## Phase 6: Integration and Main Pipeline

**Goal**: Integrate all components into a cohesive pipeline with the main function orchestrating the entire process

- [X] T043 Create main.py with main function that orchestrates the complete pipeline
- [X] T044 [P] Integrate get_all_urls, extract_text_from_urls, chunk_text, embed, create_collection, save_chunks_to_qdrant functions
- [X] T045 [P] Add comprehensive logging throughout the pipeline
- [X] T046 [P] Add validation to ensure all major book pages and modules are successfully ingested
- [X] T047 [P] Add configuration options for re-ingestion of updated content
- [X] T048 [P] Add ingestion validation to confirm successful processing

## Phase 7: Polish & Cross-Cutting Concerns

**Goal**: Complete the implementation with proper documentation, error handling, and validation

- [X] T049 Add comprehensive error handling throughout the application
- [X] T050 Add proper logging with different levels (info, warning, error)
- [X] T051 Create README.md for the backend project
- [X] T052 Add configuration validation for all required environment variables
- [X] T053 Implement comprehensive tests covering edge cases
- [X] T054 Add documentation comments to all functions
- [X] T055 Run full pipeline test to validate all major book pages are ingested
- [X] T056 Validate extracted text achieves 95% cleanliness
- [X] T057 Validate embeddings are generated consistently with uniform dimensions
- [X] T058 Validate vector storage includes all required metadata for 100% of entries
- [X] T059 Test pipeline re-execution with configuration changes