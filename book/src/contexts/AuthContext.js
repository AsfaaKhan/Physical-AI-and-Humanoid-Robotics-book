import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { authAPI } from '../services/auth';

// Create Auth Context
const AuthContext = createContext();

// Initial state
const initialState = {
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,
  background: null
};

// Auth reducer
const authReducer = (state, action) => {
  switch (action.type) {
    case 'AUTH_START':
      return {
        ...state,
        isLoading: true,
        error: null
      };
    case 'AUTH_SUCCESS':
      return {
        ...state,
        user: action.payload.user,
        token: action.payload.token,
        isAuthenticated: true,
        isLoading: false,
        background: action.payload.background || null
      };
    case 'AUTH_FAILURE':
      return {
        ...state,
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
        error: action.payload
      };
    case 'SIGNOUT_SUCCESS':
      return {
        ...state,
        user: null,
        token: null,
        isAuthenticated: false,
        background: null
      };
    case 'UPDATE_PROFILE':
      return {
        ...state,
        user: { ...state.user, ...action.payload.user },
        background: action.payload.background || state.background
      };
    case 'SET_LOADING_FALSE':
      return {
        ...state,
        isLoading: false
      };
    default:
      return state;
  }
};

// Auth Provider Component
export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Check for existing session on app load
  useEffect(() => {
    const checkSession = async () => {
      try {
        const token = localStorage.getItem('authToken');
        if (token) {
          // Verify token and get user info
          const response = await authAPI.getProfile(token);
          if (response) {
            dispatch({
              type: 'AUTH_SUCCESS',
              payload: {
                user: response,
                token: token,
                background: response.background
              }
            });
          } else {
            // Token is invalid, clear it
            localStorage.removeItem('authToken');
            dispatch({ type: 'SET_LOADING_FALSE' });
          }
        } else {
          dispatch({ type: 'SET_LOADING_FALSE' });
        }
      } catch (error) {
        console.error('Error checking session:', error);
        localStorage.removeItem('authToken');
        dispatch({ type: 'SET_LOADING_FALSE' });
      }
    };

    checkSession();
  }, []);

  // Signup function
  const signup = async (email, password, background) => {
    dispatch({ type: 'AUTH_START' });
    try {
      const response = await authAPI.signup(email, password, background);
      if (response && response.session_token) {
        // Store token in localStorage
        localStorage.setItem('authToken', response.session_token);

        dispatch({
          type: 'AUTH_SUCCESS',
          payload: {
            user: response,
            token: response.session_token,
            background: response.background
          }
        });
        return { success: true };
      } else {
        throw new Error('Invalid response from server');
      }
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || error.message || 'Signup failed';
      dispatch({
        type: 'AUTH_FAILURE',
        payload: errorMessage
      });
      return { success: false, error: errorMessage };
    }
  };

  // Signin function
  const signin = async (email, password) => {
    dispatch({ type: 'AUTH_START' });
    try {
      const response = await authAPI.signin(email, password);
      if (response && response.session_token) {
        // Store token in localStorage
        localStorage.setItem('authToken', response.session_token);

        dispatch({
          type: 'AUTH_SUCCESS',
          payload: {
            user: response,
            token: response.session_token,
            background: response.background
          }
        });
        return { success: true };
      } else {
        throw new Error('Invalid response from server');
      }
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || error.message || 'Signin failed';
      dispatch({
        type: 'AUTH_FAILURE',
        payload: errorMessage
      });
      return { success: false, error: errorMessage };
    }
  };

  // Signout function
  const signout = async () => {
    try {
      const token = state.token;
      if (token) {
        await authAPI.signout(token);
      }
    } catch (error) {
      console.error('Signout error:', error);
      // Continue with local cleanup even if API call fails
    } finally {
      // Remove token from localStorage
      localStorage.removeItem('authToken');

      dispatch({
        type: 'SIGNOUT_SUCCESS'
      });
    }
  };

  // Update profile function
  const updateProfile = async (background) => {
    try {
      const token = state.token;
      if (!token) {
        throw new Error('Not authenticated');
      }

      const response = await authAPI.updateProfile(token, { background });

      dispatch({
        type: 'UPDATE_PROFILE',
        payload: {
          user: response,
          background: response.background
        }
      });

      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || error.message || 'Profile update failed';
      return { success: false, error: errorMessage };
    }
  };

  // Get profile function
  const getProfile = async () => {
    try {
      const token = state.token;
      if (!token) {
        throw new Error('Not authenticated');
      }

      const response = await authAPI.getProfile(token);

      dispatch({
        type: 'UPDATE_PROFILE',
        payload: {
          user: response,
          background: response.background
        }
      });

      return response;
    } catch (error) {
      console.error('Error getting profile:', error);
      throw error;
    }
  };

  // Refresh token function
  const refreshToken = async () => {
    try {
      const token = state.token;
      if (!token) {
        throw new Error('No token available');
      }

      const response = await authAPI.refreshToken(token);

      if (response && response.session_token) {
        // Update token in localStorage
        localStorage.setItem('authToken', response.session_token);

        dispatch({
          type: 'AUTH_SUCCESS',
          payload: {
            user: state.user,
            token: response.session_token,
            background: state.background
          }
        });

        return true;
      }
      return false;
    } catch (error) {
      console.error('Error refreshing token:', error);
      // If refresh fails, sign out the user
      signout();
      return false;
    }
  };

  const value = {
    ...state,
    signup,
    signin,
    signout,
    updateProfile,
    getProfile,
    refreshToken
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook to use Auth Context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;