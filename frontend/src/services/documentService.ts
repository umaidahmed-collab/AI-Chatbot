import api from './api';
import { Document } from '../types/document';

export const documentService = {
  async uploadDocument(file: File): Promise<Document> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post<Document>('/api/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  async getDocuments(): Promise<Document[]> {
    const response = await api.get<Document[]>('/api/documents/');
    return response.data;
  },

  async getDocument(documentId: number): Promise<Document> {
    const response = await api.get<Document>(`/api/documents/${documentId}`);
    return response.data;
  },

  async deleteDocument(documentId: number): Promise<void> {
    await api.delete(`/api/documents/${documentId}`);
  },
};
