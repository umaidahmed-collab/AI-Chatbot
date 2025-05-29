import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { chatService } from '../../services/chatService';
import { ChatMessage, ChatSession } from '../../types/chat';
import ChatInput from './ChatInput';
import MessageList from './MessageList';
import SessionSidebar from './SessionSidebar';
import toast from 'react-hot-toast';

const Chat: React.FC = () => {
  const { sessionId } = useParams<{ sessionId: string }>();
  const [currentSession, setCurrentSession] = useState<ChatSession | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (sessionId) {
      loadSession(parseInt(sessionId));
    }
  }, [sessionId]);

  const loadSession = async (id: number) => {
    setLoading(true);
    try {
      const [session, sessionMessages] = await Promise.all([
        chatService.getSession(id),
        chatService.getSessionMessages(id),
      ]);
      setCurrentSession(session);
      setMessages(sessionMessages);
    } catch (error) {
      toast.error('Failed to load chat session');
      console.error('Error loading session:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (message: string, useDocuments: boolean) => {
    setSending(true);
    try {
      const response = await chatService.sendMessage({
        message,
        session_id: currentSession?.id,
        use_documents: useDocuments,
      });

      // If this is a new session, update the current session
      if (!currentSession || currentSession.id !== response.session_id) {
        const newSession = await chatService.getSession(response.session_id);
        setCurrentSession(newSession);
      }

      // Reload messages to get the latest conversation
      const updatedMessages = await chatService.getSessionMessages(response.session_id);
      setMessages(updatedMessages);

    } catch (error) {
      toast.error('Failed to send message');
      console.error('Error sending message:', error);
    } finally {
      setSending(false);
    }
  };

  const handleSessionSelect = (session: ChatSession) => {
    setCurrentSession(session);
    setMessages([]);
    loadSession(session.id);
  };

  const handleNewSession = async () => {
    try {
      const newSession = await chatService.createSession();
      setCurrentSession(newSession);
      setMessages([]);
    } catch (error) {
      toast.error('Failed to create new session');
      console.error('Error creating session:', error);
    }
  };

  return (
    <div className="flex h-full bg-white rounded-lg shadow overflow-hidden">
      {/* Session Sidebar */}
      <SessionSidebar
        currentSession={currentSession}
        onSessionSelect={handleSessionSelect}
        onNewSession={handleNewSession}
      />

      {/* Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Chat Header */}
        <div className="border-b border-gray-200 p-4">
          <h2 className="text-lg font-semibold text-gray-900">
            {currentSession?.title || 'New Chat'}
          </h2>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4">
          {loading ? (
            <div className="flex items-center justify-center h-full">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
            </div>
          ) : (
            <>
              <MessageList messages={messages} />
              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        {/* Chat Input */}
        <div className="border-t border-gray-200 p-4">
          <ChatInput onSendMessage={handleSendMessage} disabled={sending} />
        </div>
      </div>
    </div>
  );
};

export default Chat;
