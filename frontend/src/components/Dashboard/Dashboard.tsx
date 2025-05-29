import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { chatService } from '../../services/chatService';
import { documentService } from '../../services/documentService';
import { ChatSession } from '../../types/chat';
import { Document } from '../../types/document';
import {
  ChatBubbleLeftRightIcon,
  DocumentTextIcon,
  PlusIcon,
  ClockIcon,
} from '@heroicons/react/24/outline';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [recentSessions, setRecentSessions] = useState<ChatSession[]>([]);
  const [recentDocuments, setRecentDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [sessions, documents] = await Promise.all([
          chatService.getSessions(),
          documentService.getDocuments(),
        ]);
        
        setRecentSessions(sessions.slice(0, 5));
        setRecentDocuments(documents.slice(0, 5));
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-white rounded-lg shadow p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          Welcome back, {user?.full_name || user?.username}!
        </h1>
        <p className="text-gray-600">
          Start a new conversation or continue where you left off.
        </p>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Link
          to="/chat"
          className="bg-primary-50 border border-primary-200 rounded-lg p-6 hover:bg-primary-100 transition-colors group"
        >
          <div className="flex items-center">
            <div className="bg-primary-500 rounded-lg p-3 group-hover:bg-primary-600 transition-colors">
              <ChatBubbleLeftRightIcon className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Start New Chat</h3>
              <p className="text-sm text-gray-600">Begin a conversation with the AI</p>
            </div>
          </div>
        </Link>

        <Link
          to="/documents"
          className="bg-green-50 border border-green-200 rounded-lg p-6 hover:bg-green-100 transition-colors group"
        >
          <div className="flex items-center">
            <div className="bg-green-500 rounded-lg p-3 group-hover:bg-green-600 transition-colors">
              <DocumentTextIcon className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Upload Document</h3>
              <p className="text-sm text-gray-600">Add documents for AI analysis</p>
            </div>
          </div>
        </Link>
      </div>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Chat Sessions */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-medium text-gray-900">Recent Chats</h2>
              <Link
                to="/chat"
                className="text-sm text-primary-600 hover:text-primary-500"
              >
                View all
              </Link>
            </div>
          </div>
          <div className="p-6">
            {recentSessions.length > 0 ? (
              <div className="space-y-3">
                {recentSessions.map((session) => (
                  <Link
                    key={session.id}
                    to={`/chat/${session.id}`}
                    className="block p-3 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="text-sm font-medium text-gray-900">
                          {session.title || `Chat ${session.id}`}
                        </h4>
                        <div className="flex items-center mt-1 text-xs text-gray-500">
                          <ClockIcon className="h-3 w-3 mr-1" />
                          {new Date(session.updated_at || session.created_at).toLocaleDateString()}
                        </div>
                      </div>
                      <ChatBubbleLeftRightIcon className="h-4 w-4 text-gray-400" />
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <ChatBubbleLeftRightIcon className="h-12 w-12 text-gray-300 mx-auto mb-3" />
                <p className="text-sm text-gray-500">No chat sessions yet</p>
                <Link
                  to="/chat"
                  className="inline-flex items-center mt-2 text-sm text-primary-600 hover:text-primary-500"
                >
                  <PlusIcon className="h-4 w-4 mr-1" />
                  Start your first chat
                </Link>
              </div>
            )}
          </div>
        </div>

        {/* Recent Documents */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-medium text-gray-900">Recent Documents</h2>
              <Link
                to="/documents"
                className="text-sm text-primary-600 hover:text-primary-500"
              >
                View all
              </Link>
            </div>
          </div>
          <div className="p-6">
            {recentDocuments.length > 0 ? (
              <div className="space-y-3">
                {recentDocuments.map((document) => (
                  <div
                    key={document.id}
                    className="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50"
                  >
                    <div className="flex items-center">
                      <DocumentTextIcon className="h-5 w-5 text-gray-400 mr-3" />
                      <div>
                        <h4 className="text-sm font-medium text-gray-900">
                          {document.original_filename}
                        </h4>
                        <div className="flex items-center mt-1 text-xs text-gray-500">
                          <ClockIcon className="h-3 w-3 mr-1" />
                          {new Date(document.created_at).toLocaleDateString()}
                        </div>
                      </div>
                    </div>
                    <div className={`px-2 py-1 rounded-full text-xs ${
                      document.processed 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {document.processed ? 'Processed' : 'Processing'}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <DocumentTextIcon className="h-12 w-12 text-gray-300 mx-auto mb-3" />
                <p className="text-sm text-gray-500">No documents uploaded yet</p>
                <Link
                  to="/documents"
                  className="inline-flex items-center mt-2 text-sm text-primary-600 hover:text-primary-500"
                >
                  <PlusIcon className="h-4 w-4 mr-1" />
                  Upload your first document
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
