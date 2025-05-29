import React from 'react';
import { ChatMessage } from '../../types/chat';
import { UserIcon, CpuChipIcon } from '@heroicons/react/24/outline';

interface MessageListProps {
  messages: ChatMessage[];
}

const MessageList: React.FC<MessageListProps> = ({ messages }) => {
  if (messages.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        <div className="text-center">
          <CpuChipIcon className="h-12 w-12 mx-auto mb-3 text-gray-300" />
          <p>Start a conversation with the AI assistant</p>
          <p className="text-sm mt-1">Ask questions or upload documents for analysis</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {messages.map((message) => (
        <div
          key={message.id}
          className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
        >
          <div
            className={`flex max-w-3xl ${
              message.role === 'user' ? 'flex-row-reverse' : 'flex-row'
            }`}
          >
            {/* Avatar */}
            <div
              className={`flex-shrink-0 ${
                message.role === 'user' ? 'ml-3' : 'mr-3'
              }`}
            >
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  message.role === 'user'
                    ? 'bg-primary-500 text-white'
                    : 'bg-gray-200 text-gray-600'
                }`}
              >
                {message.role === 'user' ? (
                  <UserIcon className="h-4 w-4" />
                ) : (
                  <CpuChipIcon className="h-4 w-4" />
                )}
              </div>
            </div>

            {/* Message Content */}
            <div
              className={`px-4 py-2 rounded-lg ${
                message.role === 'user'
                  ? 'bg-primary-500 text-white'
                  : 'bg-gray-100 text-gray-900'
              }`}
            >
              <div className="whitespace-pre-wrap">{message.content}</div>
              <div
                className={`text-xs mt-1 ${
                  message.role === 'user' ? 'text-primary-100' : 'text-gray-500'
                }`}
              >
                {new Date(message.timestamp).toLocaleTimeString()}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default MessageList;
