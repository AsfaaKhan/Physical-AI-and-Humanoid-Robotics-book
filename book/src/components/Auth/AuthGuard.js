import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import GuestExperience from './GuestExperience';
import SignupPrompt from './SignupPrompt';

const AuthGuard = ({
  children,
  fallback = null,
  requireAuth = true,
  showGuestExperience = false,
  showSignupPrompt = true,
  signupPromptMessage = "Sign up to get personalized content based on your technical background!",
  signupPromptActionText = "Sign Up Now"
}) => {
  const { isAuthenticated, loading, user } = useAuth();

  // While loading auth state, show nothing or a loading indicator
  if (loading) {
    return (
      <div className="auth-guard-loading">
        <div className="loading-spinner">Loading...</div>
      </div>
    );
  }

  // If authentication is required but user is not authenticated
  if (requireAuth && !isAuthenticated) {
    if (showGuestExperience) {
      return (
        <div className="auth-guard-guest">
          <GuestExperience
            onAuthAction={(action) => {
              // This could trigger modal or navigation based on action
              console.log(`Auth action requested: ${action}`);
            }}
          />
          {children}
        </div>
      );
    } else if (showSignupPrompt) {
      return (
        <div className="auth-guard-prompt">
          <SignupPrompt
            message={signupPromptMessage}
            actionText={signupPromptActionText}
            onAction={() => {
              // This could trigger signup modal or redirect
              console.log('Signup action requested');
            }}
            position="inline"
          />
          {fallback}
        </div>
      );
    }
    return fallback;
  }

  // If authentication is NOT required but user IS authenticated, and we want to show different content
  if (!requireAuth && isAuthenticated) {
    // Return children or alternative content for authenticated users
    return children;
  }

  // If auth not required or user is authenticated (and that's what we want)
  if (!requireAuth || isAuthenticated) {
    return children;
  }

  // Default fallback
  return fallback;
};

// Convenience components for common use cases

// Protects content - shows only to authenticated users
export const ProtectedRoute = ({ children, fallback = null }) => (
  <AuthGuard requireAuth={true} fallback={fallback}>
    {children}
  </AuthGuard>
);

// Shows different content based on auth status
export const ConditionalContent = ({
  authenticatedContent,
  unauthenticatedContent,
  loadingContent = null
}) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return loadingContent || <div>Loading...</div>;
  }

  return isAuthenticated ? authenticatedContent : unauthenticatedContent;
};

// Wrapper that shows guest experience for unauthenticated users
export const GuestAwareWrapper = ({ children }) => (
  <AuthGuard showGuestExperience={true}>
    {children}
  </AuthGuard>
);

// Wrapper that shows signup prompt for unauthenticated users
export const SignupAwareWrapper = ({
  children,
  message = "Sign up to unlock personalized content!",
  actionText = "Sign Up"
}) => (
  <AuthGuard
    showSignupPrompt={true}
    signupPromptMessage={message}
    signupPromptActionText={actionText}
  >
    {children}
  </AuthGuard>
);

export default AuthGuard;