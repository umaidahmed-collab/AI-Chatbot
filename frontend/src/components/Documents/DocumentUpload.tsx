import React, { useCallback, useState } from 'react';
import { CloudArrowUpIcon, DocumentTextIcon } from '@heroicons/react/24/outline';

interface DocumentUploadProps {
  onUpload: (file: File) => void;
  uploading: boolean;
}

const DocumentUpload: React.FC<DocumentUploadProps> = ({ onUpload, uploading }) => {
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file: File) => {
    const allowedTypes = ['.pdf', '.txt', '.docx'];
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
    
    if (!allowedTypes.includes(fileExtension)) {
      alert('Please upload a PDF, TXT, or DOCX file.');
      return;
    }

    if (file.size > 10 * 1024 * 1024) { // 10MB
      alert('File size must be less than 10MB.');
      return;
    }

    onUpload(file);
  };

  return (
    <div className="space-y-4">
      {/* Drag and Drop Area */}
      <div
        className={`relative border-2 border-dashed rounded-lg p-6 transition-colors ${
          dragActive
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-300 hover:border-gray-400'
        } ${uploading ? 'opacity-50 pointer-events-none' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          type="file"
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          onChange={handleChange}
          accept=".pdf,.txt,.docx"
          disabled={uploading}
        />
        
        <div className="text-center">
          {uploading ? (
            <div className="space-y-2">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500 mx-auto"></div>
              <p className="text-sm text-gray-600">Uploading...</p>
            </div>
          ) : (
            <div className="space-y-2">
              <CloudArrowUpIcon className="h-12 w-12 text-gray-400 mx-auto" />
              <div>
                <p className="text-lg font-medium text-gray-900">
                  Drop your document here, or{' '}
                  <span className="text-primary-600">browse</span>
                </p>
                <p className="text-sm text-gray-500">
                  Supports PDF, TXT, and DOCX files up to 10MB
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Supported Formats */}
      <div className="grid grid-cols-3 gap-4">
        <div className="flex items-center space-x-2 p-3 bg-gray-50 rounded-lg">
          <DocumentTextIcon className="h-5 w-5 text-red-500" />
          <span className="text-sm font-medium text-gray-700">PDF</span>
        </div>
        <div className="flex items-center space-x-2 p-3 bg-gray-50 rounded-lg">
          <DocumentTextIcon className="h-5 w-5 text-blue-500" />
          <span className="text-sm font-medium text-gray-700">DOCX</span>
        </div>
        <div className="flex items-center space-x-2 p-3 bg-gray-50 rounded-lg">
          <DocumentTextIcon className="h-5 w-5 text-gray-500" />
          <span className="text-sm font-medium text-gray-700">TXT</span>
        </div>
      </div>
    </div>
  );
};

export default DocumentUpload;
