// book/src/components/ChatbotWidget/ChatbotContext.js
// React context and hooks for managing chat UI state

import React, { createContext, useContext, useReducer, useCallback, useEffect } from 'react';
import { ChatSession, ChatMessage, createUserMessage, createAgentMessage } from './ChatModels';
import chatbotService from './ChatbotService';

// Load initial state from localStorage if available
const loadInitialState = () => {
  // Check if we're in a browser environment (not server-side rendering)
  if (typeof window === 'undefined' || typeof window.localStorage === 'undefined') {
    return {
      isLoading: false,
      error: null,
      messages: [],
      inputValue: '',
      selectedText: null,
      sessionId: null,
      isChatOpen: false,
      conversationHistory: []
    };
  }

  try {
    const savedState = localStorage.getItem('chatbot-state');
    if (savedState) {
      const parsed = JSON.parse(savedState);
      // Only restore certain properties, not everything
      return {
        isLoading: false,
        error: null,
        messages: parsed.messages || [],
        inputValue: '',
        selectedText: null,
        sessionId: parsed.sessionId || null,
        isChatOpen: parsed.isChatOpen || false,
        conversationHistory: []
      };
    }
  } catch (error) {
    console.error('Error loading chat state from localStorage:', error);
  }
  return {
    isLoading: false,
    error: null,
    messages: [],
    inputValue: '',
    selectedText: null,
    sessionId: null,
    isChatOpen: false,
    conversationHistory: []
  };
};

// Define initial state
const initialState = loadInitialState();

// Define action types
const actionTypes = {
  SET_LOADING: 'SET_LOADING',
  SET_ERROR: 'SET_ERROR',
  ADD_MESSAGE: 'ADD_MESSAGE',
  UPDATE_INPUT_VALUE: 'UPDATE_INPUT_VALUE',
  SET_SELECTED_TEXT: 'SET_SELECTED_TEXT',
  SET_SESSION_ID: 'SET_SESSION_ID',
  TOGGLE_CHAT: 'TOGGLE_CHAT',
  CLEAR_MESSAGES: 'CLEAR_MESSAGES',
  SET_MESSAGES: 'SET_MESSAGES',
  CLEAR_ERROR: 'CLEAR_ERROR'
};

// Reducer function
function chatReducer(state, action) {
  switch (action.type) {
    case actionTypes.SET_LOADING:
      return {
        ...state,
        isLoading: action.payload
      };
    case actionTypes.SET_ERROR:
      return {
        ...state,
        error: action.payload,
        isLoading: false
      };
    case actionTypes.ADD_MESSAGE:
      return {
        ...state,
        messages: [...state.messages, action.payload],
        isLoading: false
      };
    case actionTypes.SET_MESSAGES:
      return {
        ...state,
        messages: action.payload,
        isLoading: false
      };
    case actionTypes.UPDATE_INPUT_VALUE:
      return {
        ...state,
        inputValue: action.payload
      };
    case actionTypes.SET_SELECTED_TEXT:
      return {
        ...state,
        selectedText: action.payload
      };
    case actionTypes.SET_SESSION_ID:
      return {
        ...state,
        sessionId: action.payload
      };
    case actionTypes.TOGGLE_CHAT:
      return {
        ...state,
        isChatOpen: !state.isChatOpen
      };
    case actionTypes.CLEAR_MESSAGES:
      return {
        ...state,
        messages: [],
        sessionId: null
      };
    case actionTypes.CLEAR_ERROR:
      return {
        ...state,
        error: null
      };
    default:
      return state;
  }
}

// Create context
const ChatbotContext = createContext();

// Provider component
export const ChatbotProvider = ({ children }) => {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  // Action creators
  const setLoading = useCallback((isLoading) => {
    dispatch({ type: actionTypes.SET_LOADING, payload: isLoading });
  }, []);

  const setError = useCallback((error) => {
    dispatch({ type: actionTypes.SET_ERROR, payload: error });
  }, []);

  const addMessage = useCallback((message) => {
    dispatch({ type: actionTypes.ADD_MESSAGE, payload: message });
  }, []);

  const setMessages = useCallback((messages) => {
    dispatch({ type: actionTypes.SET_MESSAGES, payload: messages });
  }, []);

  const updateInputValue = useCallback((value) => {
    dispatch({ type: actionTypes.UPDATE_INPUT_VALUE, payload: value });
  }, []);

  const setSelectedText = useCallback((text) => {
    dispatch({ type: actionTypes.SET_SELECTED_TEXT, payload: text });
  }, []);

  const setSessionId = useCallback((id) => {
    dispatch({ type: actionTypes.SET_SESSION_ID, payload: id });
  }, []);

  const toggleChat = useCallback(() => {
    dispatch({ type: actionTypes.TOGGLE_CHAT });
  }, []);

  const clearMessages = useCallback(() => {
    dispatch({ type: actionTypes.CLEAR_MESSAGES });
  }, []);

  const clearError = useCallback(() => {
    dispatch({ type: actionTypes.CLEAR_ERROR });
  }, []);

  // Function to validate user input
  const validateInput = (input) => {
    const trimmedInput = input.trim();

    // Check if input is empty
    if (!trimmedInput) {
      return { isValid: false, error: 'Message cannot be empty' };
    }

    // Check if input is too short
    if (trimmedInput.length < 3) {
      return { isValid: false, error: 'Message is too short. Please enter at least 3 characters.' };
    }

    // Check if input is too long
    if (trimmedInput.length > 1000) {
      return { isValid: false, error: 'Message is too long. Please enter no more than 1000 characters.' };
    }

    // Check for potentially harmful content (basic XSS prevention)
    const dangerousPatterns = [
      /<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi,
      /javascript:/gi,
      /vbscript:/gi,
      /on\w+\s*=/gi,
      /<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>/gi
    ];

    for (const pattern of dangerousPatterns) {
      if (pattern.test(input)) {
        return { isValid: false, error: 'Message contains potentially harmful content and cannot be sent.' };
      }
    }

    return { isValid: true, error: null };
  };

  // Function to send a message
  const sendMessage = useCallback(async (question, selectedText = null) => {
    // Validate input before processing
    const validation = validateInput(question);
    if (!validation.isValid) {
      setError(validation.error);
      return;
    }

    try {
      setLoading(true);
      clearError();

      // Create a pending user message with isPending = true
      const pendingUserMessageId = 'user_' + Date.now();
      const pendingUserMessage = new ChatMessage(
        pendingUserMessageId,
        question,
        'user',
        new Date(),
        [],
        true // isPending = true
      );
      addMessage(pendingUserMessage);

      // Send to backend API
      const response = await chatbotService.sendQuestion(
        question,
        state.sessionId,
        selectedText || state.selectedText
      );

      // Update session ID if new one was returned
      if (response.session_id && response.session_id !== state.sessionId) {
        setSessionId(response.session_id);
      }

      // Create and add agent message with additional fields
      const agentMessage = createAgentMessage(
        response.answer,
        response.sources || [],
        null, // id - will be generated
        response.confidence_score || null,
        response.metrics || null
      );

      // Update the pending message by removing it and adding the completed version
      const updatedMessages = state.messages.filter(msg => msg.id !== pendingUserMessageId);
      // Add the completed user message (without isPending)
      const finalUserMessage = new ChatMessage(
        pendingUserMessageId,
        question,
        'user',
        new Date(),
        [],
        false // isPending = false
      );
      updatedMessages.push(finalUserMessage, agentMessage);

      // Update all messages at once
      setMessages(updatedMessages);

      // Clear input and selected text after successful send
      updateInputValue('');
      setSelectedText(null);

    } catch (error) {
      // Remove the pending message if there was an error
      const updatedMessages = state.messages.filter(msg => !(msg.content === question && msg.sender === 'user' && msg.isPending));
      setMessages(updatedMessages);

      setError(error.message || 'Failed to send message');
      console.error('Error sending message:', error);
    } finally {
      setLoading(false);
    }
  }, [state.sessionId, state.selectedText, state.messages, setLoading, addMessage, setSessionId, updateInputValue, setSelectedText, setError, clearError, setMessages]);

  // Save state to localStorage when relevant state changes
  useEffect(() => {
    // Only run in browser environment (not during server-side rendering)
    if (typeof window !== 'undefined' && window.localStorage) {
      try {
        const stateToSave = {
          messages: state.messages,
          sessionId: state.sessionId,
          isChatOpen: state.isChatOpen
        };
        localStorage.setItem('chatbot-state', JSON.stringify(stateToSave));
      } catch (error) {
        console.error('Error saving chat state to localStorage:', error);
      }
    }
  }, [state.messages, state.sessionId, state.isChatOpen]);

  // Context value
  const contextValue = {
    ...state,
    setLoading,
    setError,
    addMessage,
    setMessages,
    updateInputValue,
    setSelectedText,
    setSessionId,
    toggleChat,
    clearMessages,
    clearError,
    sendMessage
  };

  return (
    <ChatbotContext.Provider value={contextValue}>
      {children}
    </ChatbotContext.Provider>
  );
};

// Custom hook to use the chat context
export const useChatbot = () => {
  const context = useContext(ChatbotContext);
  if (!context) {
    throw new Error('useChatbot must be used within a ChatbotProvider');
  }
  return context;
};

// Export action types for potential external use
export { actionTypes };