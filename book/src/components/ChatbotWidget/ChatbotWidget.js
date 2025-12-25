import React, { useEffect, useRef, useState } from 'react';
import { useChatbot } from './ChatbotContext';
import TextSelectionContextMenu from './TextSelectionContextMenu';
import './ChatbotWidget.css';

const ChatbotWidget = () => {
  const {
    messages,
    inputValue,
    isLoading,
    error,
    isChatOpen,
    selectedText,
    updateInputValue,
    toggleChat,
    sendMessage,
    clearMessages,
    setSelectedText,
    clearError
  } = useChatbot();

  const messagesEndRef = useRef(null);
  const [contextMenu, setContextMenu] = useState({ visible: false, x: 0, y: 0 });

  // Function to get selected text from the page
  const getSelectedText = () => {
    const selection = window.getSelection();
    const text = selection.toString().trim();
    if (text) {
      setSelectedText(text);
    }
    return text;
  };

  // Handle context menu for selected text
  const handleContextMenu = (e) => {
    const selectedText = window.getSelection().toString().trim();
    if (selectedText) {
      e.preventDefault();
      setContextMenu({
        visible: true,
        x: e.clientX,
        y: e.clientY
      });
    } else {
      setContextMenu({ visible: false, x: 0, y: 0 });
    }
  };

  // Handle explaining selected text
  const handleExplainText = () => {
    const selectedText = window.getSelection().toString().trim();
    if (selectedText) {
      // Set the input value to a specific prompt for explaining the selected text
      updateInputValue(`Explain this: ${selectedText}`);
      // Close the context menu
      setContextMenu({ visible: false, x: 0, y: 0 });
      // Focus the chat if it's not open
      if (!isChatOpen) {
        toggleChat();
      }
    }
  };

  // Handle text selection and context menu
  useEffect(() => {
    const handleSelection = () => {
      const text = getSelectedText();
      // Don't show context menu on selection, only on right-click
    };

    const handleClickOutside = () => {
      setContextMenu({ visible: false, x: 0, y: 0 });
    };

    // Add event listeners
    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('contextmenu', handleContextMenu);
    document.addEventListener('click', handleClickOutside);

    // Clean up event listeners
    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('contextmenu', handleContextMenu);
      document.removeEventListener('click', handleClickOutside);
    };
  }, []);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef?.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading) {
      // Check if this is an "Explain this" command and prioritize the selected text
      const isExplainCommand = inputValue.trim().startsWith('Explain this: ');
      let textToSend = inputValue;
      let contextText = selectedText || null;

      // If it's an explain command, we'll send a specific prompt to focus on explaining
      if (isExplainCommand) {
        // Extract the selected text from the command if available, otherwise use selectedText state
        const extractedText = inputValue.substring('Explain this: '.length).trim();
        contextText = extractedText || selectedText || null;
        // Create a specific question to focus the AI on explaining
        textToSend = `Please explain the following text in simple language: ${extractedText || selectedText}`;
      }

      await sendMessage(textToSend, contextText);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (inputValue.trim() && !isLoading) {
        handleSendMessage(e);
      }
    }
  };

  const clearChat = () => {
    clearMessages();
  };

  // Function to handle keyboard navigation
  const handleKeyDown = (e) => {
    // Close chat with Escape key
    if (e.key === 'Escape') {
      toggleChat();
    }
  };

  return (
    <div
      className="chatbot-widget"
      role="complementary"
      aria-label="Book Assistant Chatbot"
    >
      {/* Floating chat button */}
      <button
        className={`chatbot-toggle-button ${isChatOpen ? 'hidden' : 'visible'}`}
        onClick={toggleChat}
        aria-label="Open chatbot"
        aria-expanded={isChatOpen}
        onKeyDown={handleKeyDown}
        tabIndex={0}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
        >
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
        </svg>
      </button>

      {/* Chat container */}
      <div
        className={`chatbot-container ${isChatOpen ? 'open' : 'closed'}`}
        role="dialog"
        aria-modal="true"
        aria-label="Book Assistant Chat"
        onKeyDown={handleKeyDown}
        tabIndex={-1}
      >
        {/* Chat header */}
        <div className="chatbot-header" role="banner">
          <div className="chatbot-header-content">
            <h3 tabIndex={0}>Book Assistant</h3>
            <div className="chatbot-header-actions" role="toolbar">
              <button
                className="chatbot-clear-button"
                onClick={clearChat}
                title="Clear conversation"
                aria-label="Clear conversation"
                disabled={messages.length === 0}
                tabIndex={0}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  aria-hidden="true"
                >
                  <path d="M3 6h18M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                </svg>
              </button>
              <button
                className="chatbot-close-button"
                onClick={toggleChat}
                title="Close chat"
                aria-label="Close chat"
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    toggleChat();
                  }
                }}
                tabIndex={0}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  aria-hidden="true"
                >
                  <line x1="18" y1="6" x2="6" y2="18" />
                  <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        {/* Chat messages area */}
        <div
          className="chatbot-messages"
          role="log"
          aria-live="polite"
          aria-label="Chat messages"
          tabIndex={0}
        >
          {messages.length === 0 ? (
            <div
              className="chatbot-welcome-message"
              role="status"
              aria-live="polite"
            >
              <p>Hello! I'm your book assistant.</p>
              <p>Ask me anything about the content in this book, and I'll provide answers with source references.</p>
            </div>
          ) : (
            messages.map((message, index) => (
              <div
                key={message.id}
                className={`chatbot-message ${message.sender}-message`}
                role="listitem"
                aria-label={`${message.sender === 'user' ? 'User' : 'Assistant'} message: ${message.content.substring(0, 50)}${message.content.length > 50 ? '...' : ''}`}
                tabIndex={0}
              >
                <div className="chatbot-message-content">
                  {message.sender === 'user' ? (
                    <div className="user-message-bubble">
                      <p>{message.content}</p>
                      {message.isPending && (
                        <div className="message-status">
                          <span className="status-indicator" aria-label="Sending message">
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                              <circle cx="12" cy="12" r="10" opacity="0.3"></circle>
                              <path d="M12 6v6l4 2" opacity="0.8"></path>
                            </svg>
                          </span>
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="agent-message-bubble">
                      <p>{message.content}</p>
                      {message.sources && message.sources.length > 0 && (
                        <div
                          className="message-sources"
                          role="region"
                          aria-label="Sources for this response"
                        >
                          <h4 tabIndex={0}>Sources:</h4>
                          <ul role="list">
                            {message.sources.map((source, sourceIndex) => (
                              <li
                                key={sourceIndex}
                                tabIndex={0}
                              >
                                <a
                                  href={source.url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  onKeyDown={(e) => {
                                    if (e.key === 'Enter' || e.key === ' ') {
                                      e.currentTarget.click();
                                    }
                                  }}
                                >
                                  {source.title}
                                </a>
                                {source.section && (
                                  <span className="source-section"> - {source.section}</span>
                                )}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
          {isLoading && (
            <div
              className="chatbot-message agent-message"
              role="status"
              aria-live="polite"
              aria-label="Assistant is typing"
            >
              <div className="chatbot-message-content">
                <div className="agent-message-bubble">
                  <div className="typing-indicator">
                    <span aria-hidden="true"></span>
                    <span aria-hidden="true"></span>
                    <span aria-hidden="true"></span>
                  </div>
                  <div className="typing-text">Assistant is typing...</div>
                </div>
              </div>
            </div>
          )}
          {error && (
            <div
              className="chatbot-error"
              role="alert"
              aria-live="assertive"
            >
              <p>Error: {error}</p>
              <button
                onClick={() => {
                  // Clear error by calling clearError from context
                  clearError();
                }}
                className="retry-button"
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    // Clear error by calling clearError from context
                    clearError();
                  }
                }}
                tabIndex={0}
              >
                Retry
              </button>
            </div>
          )}
          <div ref={messagesEndRef} aria-hidden="true" />
        </div>

        {/* Chat input area */}
        <form
          className="chatbot-input-form"
          onSubmit={handleSendMessage}
          role="form"
          aria-label="Chat input form"
        >
          {selectedText && (
            <div
              className="selected-text-preview"
              role="status"
              aria-live="polite"
            >
              <small>Using selected text: "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"</small>
            </div>
          )}
          <div className="chatbot-input-area">
            <div className="input-container">
              <textarea
                value={inputValue}
                onChange={(e) => updateInputValue(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="Ask a question about the book..."
                disabled={isLoading}
                rows="1"
                className="chatbot-input"
                style={{ minHeight: '10px', resize: 'vertical' }}
                aria-label="Type your message"
                aria-describedby={selectedText ? "selected-text-preview" : undefined}
                autoFocus={isChatOpen}
                tabIndex={0}
              />
              <button
                type="submit"
                disabled={!inputValue.trim() || isLoading}
                className="chatbot-send-button"
                aria-label="Send message"
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    if (!inputValue.trim() || isLoading) return;
                    handleSendMessage(e);
                  }
                }}
                tabIndex={0}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  aria-hidden="true"
                >
                  <line x1="22" y1="2" x2="11" y2="13" />
                  <polygon points="22 2 15 22 11 13 2 9 22 2" />
                </svg>
              </button>
            </div>
          </div>
        </form>
      </div>

      {/* Context menu for explaining selected text */}
      <TextSelectionContextMenu
        isVisible={contextMenu.visible}
        position={{ x: contextMenu.x, y: contextMenu.y }}
        onExplainText={handleExplainText}
      />
    </div>
  );

};


export default ChatbotWidget;