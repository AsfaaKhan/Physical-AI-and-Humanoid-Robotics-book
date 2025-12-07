import React, { useState, useEffect, useRef } from 'react';
import './ChatbotWidget.css';

const ChatbotWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { id: 1, role: 'assistant', content: 'Hello! I\'m your Physical AI & Humanoid Robotics assistant. Ask me anything about the book content!' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [useSelectedText, setUseSelectedText] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const messagesEndRef = useRef(null);

  // Function to get selected text from the page
  const getSelectedText = () => {
    const text = window.getSelection().toString().trim();
    if (text) {
      setSelectedText(text);
      setUseSelectedText(true);
    }
    return text;
  };

  // Handle text selection
  useEffect(() => {
    const handleSelection = () => {
      getSelectedText();
    };

    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, []);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef?.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    // Add user message
    const userMessage = { id: Date.now(), role: 'user', content: inputValue };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInputValue('');
    setIsLoading(true);

    try {
      // Prepare the request payload
      const payload = {
        question: inputValue,
        use_selected_text_only: useSelectedText,
        selected_text: useSelectedText ? selectedText : null
      };

      // Call the backend API - Updated to match the actual backend API
      const response = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }

      const data = await response.json();

      // Add bot response
      const botMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.answer || data.response || 'Sorry, I could not process your request.',
        citations: data.citations || data.sources || [],
        confidence: data.confidence_estimate || data.confidence_estimate
      };

      setMessages(prevMessages => [...prevMessages, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: `Sorry, I encountered an error: ${error.message || 'Please try again.'}`
      };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
      if (useSelectedText) {
        setUseSelectedText(false);
        setSelectedText('');
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([{ id: 1, role: 'assistant', content: 'Hello! I\'m your Physical AI & Humanoid Robotics assistant. Ask me anything about the book content!' }]);
  };

  return (
    <div className="chatbot-widget">
      {isOpen ? (
        <div className="chatbot-container">
          <div className="chatbot-header">
            <h3>Physical AI Assistant</h3>
            <div className="header-controls">
              <button className="chatbot-clear" onClick={clearChat} title="Clear chat">
                🗑️
              </button>
              <button className="chatbot-close" onClick={toggleChat}>
                ×
              </button>
            </div>
          </div>

          <div className="chatbot-messages">
            {messages.map((msg) => (
              <div key={msg.id} className={`chatbot-message ${msg.role}`}>
                <div className="message-content">
                  {msg.content}
                  {msg.citations && Array.isArray(msg.citations) && msg.citations.length > 0 && (
                    <div className="citations">
                      <h4>Citations:</h4>
                      <ul>
                        {msg.citations.map((citation, idx) => (
                          <li key={idx}>
                            {typeof citation === 'object' && citation.metadata?.source ? (
                              <a href={citation.metadata.source} target="_blank" rel="noopener noreferrer">
                                {citation.metadata.source.includes('github') ? 'GitHub Source' : citation.metadata.source.substring(0, 50) + '...'}
                              </a>
                            ) : typeof citation === 'string' ? (
                              <span>{citation}</span>
                            ) : (
                              <span>Source document</span>
                            )}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="chatbot-message assistant">
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chatbot-input-area">
            {selectedText && useSelectedText && (
              <div className="selected-text-preview">
                <small>Using selected text: "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"</small>
              </div>
            )}

            <div className="chatbot-options">
              <label>
                <input
                  type="checkbox"
                  checked={useSelectedText}
                  onChange={(e) => setUseSelectedText(e.target.checked)}
                />
                Answer only using selected text
              </label>
            </div>

            <div className="input-container">
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about Physical AI & Robotics..."
                rows="1"
                style={{ minHeight: '10px', resize: 'vertical' }}
              />
              <button
                onClick={sendMessage}
                disabled={!inputValue.trim() || isLoading}
                className="send-button"
              >
                {isLoading ? '...' : '➤'}
              </button>
            </div>
          </div>
        </div>
      ) : null}

      <button className="chatbot-button" onClick={toggleChat}>
        <span className="chatbot-icon">🤖</span>
        {isOpen ? '' : '🤖'}
      </button>
    </div>
  );
};

export default ChatbotWidget;