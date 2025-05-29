import api from './api';
import { ChatSession, ChatMessage, ChatRequest, ChatResponse } from '../types/chat';

export const chatService = {
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    const response = await api.post<ChatResponse>('/api/chat/', request);
    return response.data;
  },

  async getSessions(): Promise<ChatSession[]> {
    const response = await api.get<ChatSession[]>('/api/chat/sessions');
    return response.data;
  },

  async getSession(sessionId: number): Promise<ChatSession> {
    const response = await api.get<ChatSession>(`/api/chat/sessions/${sessionId}`);
    return response.data;
  },

  async getSessionMessages(sessionId: number): Promise<ChatMessage[]> {
    const response = await api.get<ChatMessage[]>(`/api/chat/sessions/${sessionId}/messages`);
    return response.data;
  },

  async createSession(title?: string): Promise<ChatSession> {
    const response = await api.post<ChatSession>('/api/chat/sessions', null, {
      params: { title: title || 'New Chat' },
    });
    return response.data;
  },
};
