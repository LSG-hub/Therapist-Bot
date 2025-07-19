// API Types for Therapist Bot Frontend

export interface Message {
  id: string;
  content: string;
  timestamp: Date;
  type: 'user' | 'therapist';
  isError?: boolean;
}

export interface MessageRequest {
  message: string;
}

export interface MessageResponse {
  response: string;
  timestamp: string;
  conversation_id?: string;
}

export interface ApiError {
  detail: string;
  timestamp?: string;
  request_id?: string;
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  version: string;
  service: string;
}

export interface ChatState {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
}

// API Configuration
export const API_CONFIG = {
  BASE_URL: 'http://127.0.0.1:8000',
  ENDPOINTS: {
    RESPOND: '/respond',
    HEALTH: '/health'
  }
} as const;