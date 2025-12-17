# Data Model: Vector Retrieval and RAG Pipeline Validation

## Overview
Data model for the retrieval validation system that processes queries, performs vector similarity search, and validates results against the book's vector store.

## Core Entities

### QueryRequest
- **Description**: Represents a natural language query with optional metadata filters and retrieval parameters
- **Fields**:
  - `query_text` (string): The natural language query text
  - `top_k` (integer): Number of results to retrieve (default: 5)
  - `min_score` (float): Minimum similarity score threshold (optional)
  - `filters` (dict): Metadata filters (URL, module, etc.)
  - `query_embedding` (list[float]): Vector representation of the query (generated)
  - `created_at` (datetime): Timestamp when query was created

### RetrievalResult
- **Description**: Contains relevant content chunks with similarity scores, metadata, and source information
- **Fields**:
  - `query_request` (QueryRequest): Reference to the original query
  - `retrieved_chunks` (list[ContentChunk]): List of retrieved content chunks
  - `relevance_scores` (list[float]): Similarity scores for each chunk
  - `retrieval_time_ms` (float): Time taken for retrieval in milliseconds
  - `total_candidates` (integer): Total number of candidates considered
  - `metadata_filters_applied` (dict): Filters that were applied
  - `validation_metrics` (dict): Validation metrics (precision, traceability, etc.)

### QueryEmbedding
- **Description**: Vector representation of the input query generated using the Cohere embedding model
- **Fields**:
  - `vector` (list[float]): The actual embedding vector (1024 dimensions)
  - `embedding_model` (string): Name of the model used (e.g., "embed-multilingual-v3.0")
  - `query_text` (string): Original query text that generated this embedding
  - `created_at` (datetime): Timestamp when embedding was generated

### ContentChunk
- **Description**: Retrieved text content with associated metadata (source URL, page title, chunk index, relevance score)
- **Fields**:
  - `id` (string): Unique identifier for the chunk (matches the original ingestion ID)
  - `text_content` (string): The actual text content of the chunk
  - `source_url` (string): Original URL where the content was found
  - `page_title` (string): Title of the page containing this content
  - `chunk_index` (integer): Sequential index of this chunk within the page
  - `relevance_score` (float): Similarity score to the query (0.0-1.0)
  - `metadata` (dict): Additional metadata (author, section, tags, etc.)

## Validation Entities

### ValidationResult
- **Description**: Contains validation metrics and assessment of retrieval quality
- **Fields**:
  - `retrieval_result` (RetrievalResult): Reference to the result being validated
  - `precision_score` (float): Precision metric for the results
  - `traceability_score` (float): Accuracy of source URL linking (0.0-1.0)
  - `consistency_score` (float): Consistency across multiple identical queries (0.0-1.0)
  - `latency_score` (float): Performance against latency requirements (0.0-1.0)
  - `overall_quality` (float): Overall quality score combining all metrics
  - `validation_details` (dict): Detailed breakdown of validation metrics
  - `timestamp` (datetime): When validation was performed

### MetadataFilter
- **Description**: Defines criteria for filtering retrieval results by metadata
- **Fields**:
  - `field_name` (string): Name of the metadata field to filter on (e.g., "source_url", "page_title")
  - `operator` (string): Comparison operator ("equals", "contains", "in", "not_in", etc.)
  - `value` (any): Value or values to match against
  - `filter_description` (string): Human-readable description of the filter

## Relationships
- `QueryRequest` generates one `QueryEmbedding`
- `QueryEmbedding` is used to retrieve multiple `ContentChunk` objects
- Multiple `ContentChunk` objects form one `RetrievalResult`
- One `RetrievalResult` has one `ValidationResult`
- `QueryRequest` may have multiple `MetadataFilter` objects applied

## Validation Rules
- `query_text` must be non-empty and have reasonable length (5-1000 characters)
- `top_k` must be between 1 and 100
- `min_score` must be between 0.0 and 1.0 if specified
- `relevance_scores` must correspond to the retrieved chunks in order
- `retrieval_time_ms` must be positive
- `overall_quality` must be between 0.0 and 1.0

## State Transitions
- `QueryRequest` starts in "created" state, moves to "embedding_generated" after embedding, then "retrieval_completed" after search
- `ValidationResult` starts in "pending" state, moves to "completed" after validation
- `RetrievalResult` moves to "validated" after validation is complete