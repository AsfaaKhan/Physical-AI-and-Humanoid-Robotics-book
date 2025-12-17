import React from 'react';
import { useAuth } from '../../contexts/AuthContext';

const SignupPrompt = ({ message, actionText, onAction, position = 'inline' }) => {
  const { isAuthenticated } = useAuth();

  if (isAuthenticated) {
    return null; // Don't show signup prompt to authenticated users
  }

  const handleAction = () => {
    if (onAction) {
      onAction();
    }
  };

  const containerClass = `signup-prompt signup-prompt-${position}`;

  return (
    <div className={containerClass}>
      <div className="signup-prompt-content">
        <p>{message || "Sign up to get personalized content based on your technical background!"}</p>
        <button onClick={handleAction} className="signup-prompt-button">
          {actionText || "Sign Up Now"}
        </button>
      </div>
    </div>
  );
};

// Common preset components
export const ContentSignupPrompt = ({ onAction }) => (
  <SignupPrompt
    message="Unlock personalized content by signing up. We'll adapt explanations based on your technical background."
    actionText="Sign Up"
    onAction={onAction}
    position="inline"
  />
);

export const HeaderSignupPrompt = ({ onAction }) => (
  <SignupPrompt
    message="Get personalized learning experience"
    actionText="Sign Up"
    onAction={onAction}
    position="header"
  />
);

export const FooterSignupPrompt = ({ onAction }) => (
  <SignupPrompt
    message="Sign up to save your progress and get personalized recommendations"
    actionText="Create Account"
    onAction={onAction}
    position="footer"
  />
);

export default SignupPrompt;