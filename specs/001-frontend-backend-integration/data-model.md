# Data Model: Frontend ↔ Backend Chatbot Integration

## Frontend Data Models

### ChatMessage
- **id**: string (unique identifier for the message)
- **content**: string (the actual message text)
- **sender**: "user" | "agent" (who sent the message)
- **timestamp**: Date (when the message was created)
- **sources**: Array<SourceReference> (source references for agent responses)

### ChatSession
- **sessionId**: string (unique session identifier)
- **messages**: Array<ChatMessage> (conversation history)
- **createdAt**: Date (when session started)
- **lastActive**: Date (last message timestamp)
- **context**: Object (additional context like selected text)

### SourceReference
- **url**: string (source URL for the information)
- **title**: string (title of the source)
- **section**: string (specific section/chapter reference)
- **text**: string (relevant text snippet)
- **confidence**: number (confidence score of the source relevance)

### QueryRequest
- **question**: string (user's question)
- **sessionId**: string (current session ID)
- **selectedText**: string (optional selected text context)
- **context**: Object (additional context parameters)

### QueryResponse
- **answer**: string (the agent's response)
- **sources**: Array<SourceReference> (sources used in the response)
- **sessionId**: string (session identifier)
- **timestamp**: Date (when response was generated)

## Backend API Data Models

### ChatRequest (Backend Input)
- **question**: string (required, user's question)
- **session_id**: string (optional, existing session identifier)
- **selected_text**: string (optional, user-selected text as context)
- **metadata**: Object (optional, additional metadata for query processing)

### ChatResponse (Backend Output)
- **answer**: string (required, the agent's answer)
- **sources**: Array<SourceReference> (required, source references)
- **session_id**: string (required, session identifier for follow-up)
- **timestamp**: string (ISO date string for response time)
- **status**: "success" | "error" (required, response status)

### SourceReference (Backend)
- **url**: string (required, source location)
- **title**: string (required, source title)
- **content**: string (required, relevant content snippet)
- **page_number**: number (optional, page reference)
- **section**: string (optional, section reference)
- **relevance_score**: number (required, confidence/relevance score)

## State Management Models

### ChatUIState
- **isLoading**: boolean (whether a query is currently being processed)
- **error**: string | null (any error messages)
- **messages**: Array<ChatMessage> (current conversation)
- **inputValue**: string (current text in input field)
- **selectedText**: string | null (currently selected text on page)
- **sessionId**: string | null (current session identifier)
- **isChatOpen**: boolean (whether chat widget is visible)