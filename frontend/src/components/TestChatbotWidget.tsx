// Simple test component to verify ChatbotWidget functionality
import React from 'react';
import ChatbotWidget from './ChatbotWidget';

const TestComponent: React.FC = () => {
  return (
    <div style={{ padding: '20px' }}>
      <h1>Test Page</h1>
      <p>This is a test page to verify the ChatbotWidget component.</p>
      <ChatbotWidget />
    </div>
  );
};

export default TestComponent;