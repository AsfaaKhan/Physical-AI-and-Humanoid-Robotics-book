# Research: RAG Knowledge Ingestion Pipeline

## Overview
Research document for the RAG knowledge ingestion pipeline that extracts content from the Docusaurus book website, chunks it, generates Cohere embeddings, and stores in Qdrant Cloud.

## Target Website Analysis
- **URL**: https://physical-ai-and-humanoid-robotics-book-p71goqgvj.vercel.app/
- **Type**: Docusaurus documentation site
- **Structure**: Hierarchical with navigation sidebar
- **Content**: Technical content about Physical AI and Humanoid Robotics

## Technology Decisions

### Decision: Use BeautifulSoup4 for HTML parsing
- **Rationale**: Best-in-class Python library for parsing HTML content, handles malformed HTML well, and is perfect for web scraping/crawling
- **Alternatives considered**:
  - Selenium: Too heavy for simple content extraction
  - Scrapy: Overkill for single site extraction
  - lxml: Good but BeautifulSoup has better API for this use case

### Decision: Use Cohere embeddings (embed-multilingual-v3.0)
- **Rationale**: Required by constraints, excellent for technical content, multilingual support may be useful
- **Alternatives considered**:
  - OpenAI embeddings: Explicitly prohibited by constraints
  - Sentence Transformers: Free but may not be as accurate as Cohere
  - Hugging Face models: Free but requires more infrastructure

### Decision: Qdrant Cloud Free Tier for vector storage
- **Rationale**: Required by constraints, good performance, managed service, Python client available
- **Alternatives considered**:
  - Pinecone: Alternative managed vector DB but not specified in constraints
  - Weaviate: Open source alternative but Qdrant was specified
  - ChromaDB: Local option but cloud service was specified

### Decision: Recursive URL discovery approach
- **Rationale**: Docusaurus sites have predictable structure with sitemaps, can also crawl links to find all pages
- **Implementation**: Either parse sitemap.xml or recursively follow internal links up to a depth limit

## Content Extraction Strategy
- **Primary target**: `<main>` content area or `.markdown` class divs (typical Docusaurus selectors)
- **To exclude**: Navigation, headers, footers, sidebar, table of contents
- **Selectors to use**:
  - Main content: `main div[class*="docItem"]` or `article` tags
  - Avoid: `nav`, `.navbar`, `.sidebar`, `.theme-doc-sidebar`, `.table-of-contents`

## Text Chunking Strategy
- **Approach**: Recursive character split with overlap
- **Size**: 512-1024 tokens (approximately 300-800 words)
- **Overlap**: 50-100 tokens to maintain context
- **Boundaries**: Respect sentence and paragraph boundaries when possible
- **Rationale**: Maintains semantic coherence while fitting embedding model limits

## Environment Configuration
- **Variables needed**:
  - `COHERE_API_KEY`: API key for Cohere embeddings
  - `QDRANT_URL`: URL for Qdrant Cloud instance
  - `QDRANT_API_KEY`: API key for Qdrant Cloud
  - `BOOK_BASE_URL`: Base URL of the book website
  - `QDRANT_COLLECTION_NAME`: Name of collection (rag_embedding_physical_ai_book)

## Error Handling Strategy
- **Website unavailable**: Retry with exponential backoff
- **Rate limiting**: Implement proper delays between requests
- **Embedding failures**: Log and continue with other chunks
- **Qdrant storage failures**: Batch operations with retry logic