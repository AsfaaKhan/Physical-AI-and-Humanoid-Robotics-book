// book/src/components/ChatbotWidget/ChatModels.js
// Frontend data models for chat messages and sessions

/**
 * ChatMessage model
 * Represents a single message in the chat conversation
 */
export class ChatMessage {
  constructor(id, content, sender, timestamp, sources = [], isPending = false) {
    this.id = id;
    this.content = content;
    this.sender = sender; // 'user' or 'agent'
    this.timestamp = timestamp || new Date();
    this.sources = sources; // Array of SourceReference objects
    this.isPending = isPending; // Whether the message is pending (for user messages)
  }

  // Factory method to create from API response
  static fromApiResponse(apiMessage, sender) {
    return new ChatMessage(
      apiMessage.id || Date.now().toString(),
      apiMessage.content || apiMessage.answer || apiMessage.question || '',
      sender,
      new Date(apiMessage.timestamp || Date.now()),
      apiMessage.sources || []
    );
  }

  // Validate message structure
  static isValid(message) {
    return message &&
           typeof message.content === 'string' &&
           message.content.trim().length > 0 &&
           (message.sender === 'user' || message.sender === 'agent');
  }
}

/**
 * SourceReference model
 * Represents a source reference in an agent response
 */
export class SourceReference {
  constructor(url, title, section, text, confidence) {
    this.url = url;
    this.title = title;
    this.section = section || '';
    this.text = text || '';
    this.confidence = confidence || 0; // Confidence score
  }

  // Factory method to create from API response
  static fromApiResponse(apiSource) {
    return new SourceReference(
      apiSource.url,
      apiSource.title,
      apiSource.section || apiSource.page_number || apiSource.section,
      apiSource.content || apiSource.text || '',
      apiSource.relevance_score || apiSource.confidence || 0
    );
  }
}

/**
 * ChatSession model
 * Represents a chat session with conversation history
 */
export class ChatSession {
  constructor(sessionId, messages = [], createdAt, lastActive, context = {}) {
    this.sessionId = sessionId || this.generateSessionId();
    this.messages = messages || [];
    this.createdAt = createdAt || new Date();
    this.lastActive = lastActive || new Date();
    this.context = context || {}; // Additional context like selected text
  }

  // Add a message to the session
  addMessage(message) {
    if (ChatMessage.isValid(message)) {
      this.messages.push(message);
      this.lastActive = new Date();
      return true;
    }
    return false;
  }

  // Get user messages
  getUserMessages() {
    return this.messages.filter(msg => msg.sender === 'user');
  }

  // Get agent messages
  getAgentMessages() {
    return this.messages.filter(msg => msg.sender === 'agent');
  }

  // Clear all messages
  clearMessages() {
    this.messages = [];
    this.lastActive = new Date();
  }

  // Generate a unique session ID
  generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  }

  // Factory method to create from API response
  static fromApiResponse(apiResponse) {
    const sessionId = apiResponse.session_id || apiResponse.sessionId;
    return new ChatSession(sessionId);
  }
}

// Helper function to create a new user message
export const createUserMessage = (content, id = null) => {
  return new ChatMessage(
    id || 'user_' + Date.now(),
    content,
    'user',
    new Date()
  );
};

// Helper function to create a new agent message
export const createAgentMessage = (content, sources = [], id = null, confidence_score = null, metrics = null) => {
  const message = new ChatMessage(
    id || 'agent_' + Date.now(),
    content,
    'agent',
    new Date(),
    sources
  );

  // Add additional fields from API response
  if (confidence_score !== null) {
    message.confidence_score = confidence_score;
  }
  if (metrics !== null) {
    message.metrics = metrics;
  }

  return message;
};