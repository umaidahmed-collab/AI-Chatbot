import React, { useState, useEffect } from 'react';
import { documentService } from '../../services/documentService';
import { Document } from '../../types/document';
import DocumentUpload from './DocumentUpload';
import DocumentList from './DocumentList';
import toast from 'react-hot-toast';

const Documents: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const documentsData = await documentService.getDocuments();
      setDocuments(documentsData);
    } catch (error) {
      toast.error('Failed to load documents');
      console.error('Error loading documents:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (file: File) => {
    setUploading(true);
    try {
      const newDocument = await documentService.uploadDocument(file);
      setDocuments([newDocument, ...documents]);
      toast.success('Document uploaded successfully!');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to upload document');
      console.error('Error uploading document:', error);
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (documentId: number) => {
    if (!window.confirm('Are you sure you want to delete this document?')) {
      return;
    }

    try {
      await documentService.deleteDocument(documentId);
      setDocuments(documents.filter(doc => doc.id !== documentId));
      toast.success('Document deleted successfully!');
    } catch (error) {
      toast.error('Failed to delete document');
      console.error('Error deleting document:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Documents</h1>
        <p className="text-gray-600">
          Upload documents to enhance your AI conversations with relevant context.
        </p>
      </div>

      {/* Upload Section */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Upload New Document</h2>
        <DocumentUpload onUpload={handleUpload} uploading={uploading} />
      </div>

      {/* Documents List */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Your Documents</h2>
        </div>
        <DocumentList documents={documents} onDelete={handleDelete} />
      </div>
    </div>
  );
};

export default Documents;
