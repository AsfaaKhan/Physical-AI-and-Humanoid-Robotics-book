import React, { useState, useEffect } from 'react';
import './TextSelectionContextMenu.css';

const TextSelectionContextMenu = ({ onExplainText, isVisible, position }) => {
  if (!isVisible) return null;

  const handleExplain = () => {
    onExplainText();
  };

  const handleContextMenu = (e) => {
    e.preventDefault();
  };

  return (
    <div
      className="text-selection-context-menu"
      style={{
        position: 'fixed',
        left: `${position.x}px`,
        top: `${position.y}px`,
        zIndex: 10000,
      }}
      onContextMenu={handleContextMenu}
    >
      <button
        className="context-menu-option"
        onClick={handleExplain}
        aria-label="Explain selected text"
      >
        <span className="menu-icon">💡</span>
        <span>Explain this</span>
      </button>
    </div>
  );
};

export default TextSelectionContextMenu;