import React from 'react';
import { useAuth } from '../../contexts/AuthContext';

const GuestExperience = ({ onAuthAction }) => {
  const { isAuthenticated } = useAuth();

  if (isAuthenticated) {
    return null; // Don't show guest experience to authenticated users
  }

  return (
    <div className="guest-experience">
      <div className="guest-message">
        <h3>Enhance Your Learning Experience</h3>
        <p>
          Sign up or sign in to get personalized content based on your technical background.
          We'll adapt explanations, examples, and difficulty levels to match your experience.
        </p>
        <div className="auth-options">
          <button
            onClick={() => onAuthAction && onAuthAction('signup')}
            className="auth-button signup-button"
          >
            Sign Up
          </button>
          <button
            onClick={() => onAuthAction && onAuthAction('signin')}
            className="auth-button signin-button"
          >
            Sign In
          </button>
        </div>
      </div>
    </div>
  );
};

export default GuestExperience;