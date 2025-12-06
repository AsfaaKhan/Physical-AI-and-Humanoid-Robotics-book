import React, { useState, useEffect } from 'react';
import './ChatbotWidget.css';

const ChatbotWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [useSelectedText, setUseSelectedText] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [backendUrl, setBackendUrl] = useState('http://localhost:8000'); // Default local URL

  // Function to get selected text from the page
  const getSelectedText = () => {
    const text = window.getSelection().toString().trim();
    if (text) {
      setSelectedText(text);
      setUseSelectedText(true);
      console.log('Selected text:', text); // For debugging
    }
    return text;
  };

  // Handle text selection
  useEffect(() => {
    const handleSelection = () => {
      const text = getSelectedText();
      if (text && !isOpen) {
        // Optionally open the chat if text is selected
        // setIsOpen(true);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, []);

  // Update backend URL when component mounts
  useEffect(() => {
    // Check if we're on GitHub Pages or other deployment
    const currentOrigin = window.location.origin;
    if (currentOrigin.includes('github.io')) {
      // For GitHub Pages, use your deployed backend URL
      // Replace with your actual deployed backend URL
      setBackendUrl('https://your-rag-backend.onrender.com'); // Update this with your actual backend URL
    } else {
      // For local development
      setBackendUrl('http://localhost:8000');
    }
  }, []);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = { role: 'user', content: inputValue };
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

      console.log('Sending request:', payload); // For debugging

      // Call the backend API
      const response = await fetch(`${backendUrl}/api/v1/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      console.log('Response status:', response.status); // For debugging

      if (!response.ok) {
        const errorText = await response.text();
        console.error('API error response:', errorText);
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }

      const data = await response.json();
      console.log('API response:', data); // For debugging

      const botMessage = {
        role: 'assistant',
        content: data.answer,
        citations: data.citations,
        confidence: data.confidence_estimate
      };

      setMessages([...newMessages, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        role: 'assistant',
        content: `Sorry, I encountered an error: ${error.message || 'Please try again.'}`
      };
      setMessages([...newMessages, errorMessage]);
    } finally {
      setIsLoading(false);
      // Only reset if we used selected text
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
    setMessages([]);
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
            {messages.length === 0 ? (
              <div className="chatbot-welcome">
                <p>Hello! I'm your Physical AI & Humanoid Robotics assistant.</p>
                <p>Ask me anything about the book content!</p>
                <p><small>Select text on the page and ask questions about it!</small></p>
              </div>
            ) : (
              messages.map((msg, index) => (
                <div key={index} className={`chatbot-message ${msg.role}`}>
                  <div className="message-content">
                    {msg.content}
                    {msg.citations && msg.citations.length > 0 && (
                      <div className="citations">
                        <h4>Citations:</h4>
                        <ul>
                          {msg.citations.map((citation, idx) => (
                            <li key={idx}>
                              {citation.metadata?.source ? (
                                <a href={citation.metadata.source} target="_blank" rel="noopener noreferrer">
                                  {citation.metadata.source.includes('github') ? 'GitHub Source' : citation.metadata.source.substring(0, 30) + '...'}
                                </a>
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
              ))
            )}

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
                  disabled={!!selectedText && !useSelectedText} // Only disable if we have selected text but haven't enabled the option yet
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
                rows="2"
              />
              <button
                onClick={sendMessage}
                disabled={!inputValue.trim() || isLoading}
                className="send-button"
              >
                {isLoading ? 'Sending...' : 'Send'}
              </button>
            </div>
          </div>
        </div>
      ) : null}

      <button className="chatbot-button" onClick={toggleChat}>
        <span className="chatbot-icon">🤖</span>
        {isOpen ? '' : 'AI Assistant'}
      </button>
    </div>
  );
};

export default ChatbotWidget;