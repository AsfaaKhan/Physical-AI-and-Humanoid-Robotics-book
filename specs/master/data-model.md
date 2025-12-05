# Data Model: Physical AI & Humanoid Robotics Book + RAG System

## Core Entities

### Book Content
- **Entity**: BookContent
- **Fields**:
  - id (string): Unique identifier for each content piece
  - title (string): Title of the chapter/section
  - module (string): Module identifier (e.g., "module-1-ros2", "module-2-gazebo-unity")
  - path (string): File path in the book structure
  - content (text): Raw text content of the section
  - word_count (integer): Number of words in the content
  - authors (array): List of authors/contributors
  - created_date (datetime): Date of creation
  - last_modified (datetime): Date of last modification
  - tags (array): List of tags for categorization
  - references (array): APA-formatted citations used in the content
- **Relationships**:
  - One-to-many with ContentChunk (one book section can be chunked into multiple vectors)
  - One-to-many with Diagram (one section can have multiple diagrams)

### Content Chunk
- **Entity**: ContentChunk
- **Fields**:
  - id (string): Unique identifier for each chunk
  - book_content_id (string): Reference to parent BookContent
  - chunk_text (text): The actual text chunk
  - chunk_index (integer): Order of the chunk within the parent content
  - token_count (integer): Number of tokens in the chunk
  - embedding_id (string): Reference to the vector embedding in Qdrant
  - metadata (object): Additional metadata (section, page, etc.)
- **Relationships**:
  - Many-to-one with BookContent (multiple chunks per content piece)
  - One-to-one with VectorEmbedding (each chunk maps to one embedding)

### Vector Embedding
- **Entity**: VectorEmbedding
- **Fields**:
  - id (string): Qdrant collection ID
  - content_chunk_id (string): Reference to the source chunk
  - vector_data (array): The actual embedding vector
  - model_used (string): Model used for embedding generation
  - created_date (datetime): When the embedding was created
- **Relationships**:
  - One-to-one with ContentChunk (each embedding corresponds to one chunk)

### User Query
- **Entity**: UserQuery
- **Fields**:
  - id (string): Unique identifier for the query
  - query_text (text): The original user question
  - session_id (string): ID of the chat session
  - user_id (string): Optional user identifier
  - timestamp (datetime): When the query was made
  - source_context (text): Any highlighted text or context provided
  - processed (boolean): Whether the query has been processed
- **Relationships**:
  - One-to-many with QueryResponse (one query can generate one response)
  - One-to-many with QueryLog (for analytics)

### Query Response
- **Entity**: QueryResponse
- **Fields**:
  - id (string): Unique identifier for the response
  - query_id (string): Reference to the original query
  - response_text (text): The generated response
  - source_documents (array): List of source document IDs used
  - confidence_score (float): Confidence in the response (0-1)
  - timestamp (datetime): When the response was generated
  - citations (array): Specific citations to book sections
  - was_fallback (boolean): Whether this was a "not in book" response
- **Relationships**:
  - Many-to-one with UserQuery (response to a specific query)

### Query Log
- **Entity**: QueryLog
- **Fields**:
  - id (string): Unique identifier for the log entry
  - query_id (string): Reference to the query
  - response_id (string): Reference to the response
  - user_id (string): Optional user identifier
  - session_id (string): Chat session identifier
  - query_text (text): The original query
  - response_text (text): The response given
  - response_time_ms (integer): Time taken to generate response
  - timestamp (datetime): When the query was processed
  - rating (integer): Optional user rating (1-5)
  - feedback (text): Optional user feedback
- **Relationships**:
  - Many-to-one with UserQuery and QueryResponse

### Diagram
- **Entity**: Diagram
- **Fields**:
  - id (string): Unique identifier for the diagram
  - title (string): Title of the diagram
  - description (text): Description of what the diagram shows
  - file_path (string): Path to the image file
  - alt_text (string): Accessibility alt text
  - caption (text): Caption to display with the diagram
  - book_content_id (string): Reference to the book content that uses this diagram
  - type (string): Type of diagram (e.g., "architecture", "workflow", "code")
- **Relationships**:
  - Many-to-one with BookContent (multiple diagrams per content piece)

### Code Example
- **Entity**: CodeExample
- **Fields**:
  - id (string): Unique identifier for the code example
  - title (string): Title/description of the code example
  - language (string): Programming language (e.g., "python", "bash", "yaml")
  - code (text): The actual code content
  - description (text): Explanation of what the code does
  - book_content_id (string): Reference to the book content that uses this example
  - execution_context (string): Where the code should run (e.g., "ros2", "isaac-sim")
- **Relationships**:
  - Many-to-one with BookContent (multiple code examples per content piece)

## Relationships Summary

1. BookContent → ContentChunk (1:M)
2. ContentChunk → VectorEmbedding (1:1)
3. UserQuery → QueryResponse (1:1)
4. UserQuery → QueryLog (1:M)
5. QueryResponse → QueryLog (1:M)
6. BookContent → Diagram (1:M)
7. BookContent → CodeExample (1:M)

## Validation Rules

### BookContent Validation
- Title must be 5-200 characters
- Content must have at least 100 words
- Module must be one of: "intro", "module-1-ros2", "module-2-gazebo-unity", "module-3-isaac", "module-4-vla", "capstone", "appendix", "references"
- At least one reference required if content mentions technical claims
- Path must follow the defined directory structure

### ContentChunk Validation
- Chunk text must be 50-2000 characters
- Token count must be less than model context window
- Must have valid reference to parent BookContent
- Chunk index must be unique within parent content

### UserQuery Validation
- Query text must be 5-1000 characters
- Session ID must be present
- Timestamp must be within reasonable bounds

### QueryResponse Validation
- Response text must be provided
- Confidence score must be between 0 and 1
- If was_fallback is true, response text must contain standard fallback message
- Citations must reference valid book content

## State Transitions

### Content Review States
- DRAFT → REVIEW_PENDING → APPROVED → PUBLISHED
- DRAFT → REJECTED → DRAFT (with changes)

### Query Processing States
- RECEIVED → PROCESSING → COMPLETED
- RECEIVED → ERROR (if processing fails)

## Indexes

### BookContent
- Index on module field for fast filtering
- Index on path for fast lookups
- Index on tags for search

### ContentChunk
- Index on book_content_id for joins
- Index on embedding_id for vector lookups

### QueryLog
- Index on timestamp for analytics
- Index on session_id for session tracking
- Index on user_id for user analytics