import React, { useState } from 'react';
import { PaperAirplaneIcon, DocumentTextIcon } from '@heroicons/react/24/outline';

interface ChatInputProps {
  onSendMessage: (message: string, useDocuments: boolean) => void;
  disabled?: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, disabled = false }) => {
  const [message, setMessage] = useState('');
  const [useDocuments, setUseDocuments] = useState(true);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message.trim(), useDocuments);
      setMessage('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      {/* Document toggle */}
      <div className="flex items-center space-x-2">
        <label className="flex items-center space-x-2 text-sm text-gray-600">
          <input
            type="checkbox"
            checked={useDocuments}
            onChange={(e) => setUseDocuments(e.target.checked)}
            className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
          />
          <DocumentTextIcon className="h-4 w-4" />
          <span>Use uploaded documents</span>
        </label>
      </div>

      {/* Message input */}
      <div className="flex space-x-3">
        <div className="flex-1">
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message here..."
            disabled={disabled}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none disabled:opacity-50"
          />
        </div>
        <button
          type="submit"
          disabled={disabled || !message.trim()}
          className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
        >
          <PaperAirplaneIcon className="h-4 w-4" />
          <span>{disabled ? 'Sending...' : 'Send'}</span>
        </button>
      </div>
    </form>
  );
};

export default ChatInput;
