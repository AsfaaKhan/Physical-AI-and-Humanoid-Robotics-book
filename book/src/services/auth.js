// API service for authentication
const API_BASE_URL = typeof process !== 'undefined' && process.env && process.env.REACT_APP_AUTH_API_URL
  ? process.env.REACT_APP_AUTH_API_URL
  : 'http://localhost:5000/api/v1';

// Generic API call function with error handling
const apiCall = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;

  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  // Add authorization header if token is provided
  if (options.token) {
    defaultOptions.headers['Authorization'] = `Bearer ${options.token}`;
    delete options.token; // Remove token from options to avoid passing it in the request body
  }

  const config = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers,
    },
  };

  // If body is provided and is an object, stringify it
  if (config.body && typeof config.body === 'object') {
    config.body = JSON.stringify(config.body);
  }

  try {
    const response = await fetch(url, config);

    // Handle different response status codes
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw {
        status: response.status,
        message: errorData.error?.message || `HTTP error! status: ${response.status}`,
        data: errorData
      };
    }

    // Return JSON response
    return await response.json();
  } catch (error) {
    // Handle network errors or other exceptions
    if (error.status) {
      // This is an HTTP error with status and message from server
      throw error;
    } else {
      // This is a network error or other exception
      throw {
        status: null,
        message: error.message || 'Network error or server not responding',
        data: {}
      };
    }
  }
};

// Auth API service object
export const authAPI = {
  // Signup a new user
  signup: async (email, password, background) => {
    return apiCall('/auth/signup', {
      method: 'POST',
      body: {
        email,
        password,
        background
      }
    });
  },

  // Sign in existing user
  signin: async (email, password) => {
    return apiCall('/auth/signin', {
      method: 'POST',
      body: {
        email,
        password
      }
    });
  },

  // Sign out user
  signout: async (token) => {
    return apiCall('/auth/signout', {
      method: 'POST',
      token: token
    });
  },

  // Get user profile
  getProfile: async (token) => {
    return apiCall('/auth/profile', {
      method: 'GET',
      token: token
    });
  },

  // Update user profile
  updateProfile: async (token, profileData) => {
    return apiCall('/auth/profile', {
      method: 'PUT',
      token: token,
      body: profileData
    });
  },

  // Refresh authentication token
  refreshToken: async (token) => {
    return apiCall('/auth/refresh', {
      method: 'POST',
      token: token
    });
  }
};

export default authAPI;