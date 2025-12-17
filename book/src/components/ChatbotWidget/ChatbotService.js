// book/src/components/ChatbotWidget/ChatbotService.js
// API client service to communicate with backend API

class ChatbotService {
  constructor() {
    // In development, backend might run on localhost:5000
    // In production (GitHub Pages), the API URL should be configured via environment variable
    // This allows flexibility for different deployment scenarios
    // Check if process.env is available (it's not available during SSR)
    const envVar = typeof process !== 'undefined' && process.env ? process.env.REACT_APP_CHATBOT_API_URL : undefined;
    this.baseURL = envVar || 'http://localhost:5000';

    // For GitHub Pages deployment, you would set the environment variable during build:
    // REACT_APP_CHATBOT_API_URL=https://your-backend-api.com npm run build
  }

  /**
   * Send a question to the chatbot API
   * @param {string} question - The question of user
   * @param {string} sessionId - Optional session ID for conversation continuity
   * @param {string} selectedText - Optional selected text to provide context
   * @returns {Promise<Object>} The API response containing answer and sources
   */
  async sendQuestion(question, sessionId = null, selectedText = null, retries = 3) {
    const requestBody = {
      question: question,
      session_id: sessionId,
      selected_text: selectedText || null,
      metadata: {}
    };

    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

        const response = await fetch(`${this.baseURL}/api/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
          signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
          // Handle different types of errors
          if (response.status === 400) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(`Bad request: ${errorData.error || 'Invalid input parameters'}`);
          } else if (response.status === 401) {
            throw new Error('Unauthorized: Please check your API credentials');
          } else if (response.status === 403) {
            throw new Error('Forbidden: Access denied');
          } else if (response.status === 429) {
            throw new Error('Rate limited: Too many requests, please try again later');
          } else if (response.status >= 500) {
            // These are server errors that might be retried
            if (attempt < retries) {
              // Wait before retrying (exponential backoff)
              await this.delay(Math.pow(2, attempt) * 1000); // 2^attempt * 1000ms
              continue;
            } else {
              throw new Error(`Server error (${response.status}): The server encountered an error, please try again later`);
            }
          } else {
            throw new Error(`API request failed with status ${response.status}`);
          }
        }

        const data = await response.json();
        return data;
      } catch (error) {
        // Handle network errors, timeout errors, etc.
        if (error.name === 'AbortError') {
          console.error(`Request timeout error on attempt ${attempt}/${retries}:`, error);
          if (attempt < retries) {
            // Wait before retrying
            await this.delay(Math.pow(2, attempt) * 1000); // 2^attempt * 1000ms
            continue;
          } else {
            throw new Error('Request timeout: The server took too long to respond');
          }
        } else if (error.name === 'TypeError' && error.message.includes('fetch')) {
          console.error(`Network error on attempt ${attempt}/${retries}:`, error);
          if (attempt < retries) {
            // Wait before retrying
            await this.delay(Math.pow(2, attempt) * 1000); // 2^attempt * 1000ms
            continue;
          } else {
            throw new Error('Network error: Unable to connect to the server. Please check your internet connection and try again.');
          }
        } else {
          console.error(`Error sending question to chatbot API on attempt ${attempt}/${retries}:`, error);
          if (attempt < retries && error.message.includes('Network error') || error.message.includes('timeout')) {
            // Only retry for network-related errors
            await this.delay(Math.pow(2, attempt) * 1000); // 2^attempt * 1000ms
            continue;
          } else {
            throw error;
          }
        }
      }
    }
  }

  // Helper function for delay
  async delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Test the API connection
   * @returns {Promise<boolean>} Whether the API is accessible
   */
  async testConnection() {
    try {
      const response = await fetch(`${this.baseURL}/`);
      return response.ok;
    } catch (error) {
      console.error('API connection test failed:', error);
      return false;
    }
  }
}

// Export a singleton instance
const chatbotService = new ChatbotService();
export default chatbotService;

// Also export the class for testing purposes if needed
export { ChatbotService };