import React from 'react';
import { Document } from '../../types/document';
import {
  DocumentTextIcon,
  TrashIcon,
  ClockIcon,
  CheckCircleIcon,
} from '@heroicons/react/24/outline';

interface DocumentListProps {
  documents: Document[];
  onDelete: (documentId: number) => void;
}

const DocumentList: React.FC<DocumentListProps> = ({ documents, onDelete }) => {
  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getFileIcon = (contentType: string) => {
    if (contentType.includes('pdf')) {
      return <DocumentTextIcon className="h-8 w-8 text-red-500" />;
    } else if (contentType.includes('word') || contentType.includes('docx')) {
      return <DocumentTextIcon className="h-8 w-8 text-blue-500" />;
    } else {
      return <DocumentTextIcon className="h-8 w-8 text-gray-500" />;
    }
  };

  if (documents.length === 0) {
    return (
      <div className="p-6 text-center">
        <DocumentTextIcon className="h-12 w-12 text-gray-300 mx-auto mb-3" />
        <p className="text-gray-500">No documents uploaded yet</p>
        <p className="text-sm text-gray-400 mt-1">
          Upload your first document to get started
        </p>
      </div>
    );
  }

  return (
    <div className="divide-y divide-gray-200">
      {documents.map((document) => (
        <div key={document.id} className="p-6 hover:bg-gray-50 transition-colors">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              {/* File Icon */}
              <div className="flex-shrink-0">
                {getFileIcon(document.content_type)}
              </div>

              {/* File Info */}
              <div className="flex-1 min-w-0">
                <h3 className="text-sm font-medium text-gray-900 truncate">
                  {document.original_filename}
                </h3>
                <div className="flex items-center space-x-4 mt-1 text-xs text-gray-500">
                  <span>{formatFileSize(document.file_size)}</span>
                  <div className="flex items-center space-x-1">
                    <ClockIcon className="h-3 w-3" />
                    <span>{new Date(document.created_at).toLocaleDateString()}</span>
                  </div>
                </div>
              </div>

              {/* Processing Status */}
              <div className="flex-shrink-0">
                {document.processed ? (
                  <div className="flex items-center space-x-1 text-green-600">
                    <CheckCircleIcon className="h-4 w-4" />
                    <span className="text-xs font-medium">Processed</span>
                  </div>
                ) : (
                  <div className="flex items-center space-x-1 text-yellow-600">
                    <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-yellow-600"></div>
                    <span className="text-xs font-medium">Processing</span>
                  </div>
                )}
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center space-x-2 ml-4">
              <button
                onClick={() => onDelete(document.id)}
                className="p-2 text-gray-400 hover:text-red-600 transition-colors"
                title="Delete document"
              >
                <TrashIcon className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default DocumentList;
