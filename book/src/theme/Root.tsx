import React from 'react';
import { ChatbotProvider } from '../components/ChatbotWidget/ChatbotContext';
import ChatbotWidget from '../components/ChatbotWidget/ChatbotWidget';
import { AuthProvider } from '../contexts/AuthContext';

// Default wrapper for the whole Docusaurus site
export default function Root({ children }) {
  return (
    <AuthProvider>
      <ChatbotProvider>
        {children}
        <ChatbotWidget />
      </ChatbotProvider>
    </AuthProvider>
  );
}