import React from 'react';
import ChatbotWidget from '../ChatbotWidget';

const LayoutWrapper = ({ children }) => {
  return (
    <>
      {children}
      <ChatbotWidget />
    </>
  );
};

export default LayoutWrapper;