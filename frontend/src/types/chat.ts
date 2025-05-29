export interface ChatMessage {
  id: number;
  session_id: number;
  content: string;
  role: 'user' | 'assistant';
  timestamp: string;
}

export interface ChatSession {
  id: number;
  title?: string;
  user_id: number;
  created_at: string;
  updated_at?: string;
  messages: ChatMessage[];
}

export interface ChatRequest {
  message: string;
  session_id?: number;
  use_documents: boolean;
}

export interface ChatResponse {
  message: string;
  session_id: number;
  sources?: string[];
}
