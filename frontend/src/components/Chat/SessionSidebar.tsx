import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { chatService } from '../../services/chatService';
import { ChatSession } from '../../types/chat';
import { PlusIcon, ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';

interface SessionSidebarProps {
  currentSession: ChatSession | null;
  onSessionSelect: (session: ChatSession) => void;
  onNewSession: () => void;
}

const SessionSidebar: React.FC<SessionSidebarProps> = ({
  currentSession,
  onSessionSelect,
  onNewSession,
}) => {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = async () => {
    try {
      const sessionsData = await chatService.getSessions();
      setSessions(sessionsData);
    } catch (error) {
      toast.error('Failed to load chat sessions');
      console.error('Error loading sessions:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSessionClick = (session: ChatSession) => {
    onSessionSelect(session);
    navigate(`/chat/${session.id}`);
  };

  const handleNewSessionClick = async () => {
    try {
      const newSession = await chatService.createSession();
      setSessions([newSession, ...sessions]);
      onNewSession();
      navigate(`/chat/${newSession.id}`);
    } catch (error) {
      toast.error('Failed to create new session');
      console.error('Error creating session:', error);
    }
  };

  return (
    <div className="w-64 bg-gray-50 border-r border-gray-200 flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <button
          onClick={handleNewSessionClick}
          className="w-full flex items-center justify-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
        >
          <PlusIcon className="h-4 w-4 mr-2" />
          New Chat
        </button>
      </div>

      {/* Sessions List */}
      <div className="flex-1 overflow-y-auto p-2">
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-500"></div>
          </div>
        ) : sessions.length > 0 ? (
          <div className="space-y-1">
            {sessions.map((session) => (
              <button
                key={session.id}
                onClick={() => handleSessionClick(session)}
                className={`w-full text-left p-3 rounded-lg transition-colors ${
                  currentSession?.id === session.id
                    ? 'bg-primary-100 text-primary-900 border border-primary-200'
                    : 'hover:bg-gray-100 text-gray-700'
                }`}
              >
                <div className="flex items-start space-x-3">
                  <ChatBubbleLeftRightIcon className="h-4 w-4 mt-0.5 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium truncate">
                      {session.title || `Chat ${session.id}`}
                    </div>
                    <div className="text-xs text-gray-500 mt-1">
                      {new Date(session.updated_at || session.created_at).toLocaleDateString()}
                    </div>
                  </div>
                </div>
              </button>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <ChatBubbleLeftRightIcon className="h-8 w-8 mx-auto mb-2 text-gray-300" />
            <p className="text-sm">No chat sessions yet</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default SessionSidebar;
