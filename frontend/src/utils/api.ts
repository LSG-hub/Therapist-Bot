import type { MessageRequest, MessageResponse, HealthResponse, ApiError } from '../types/api';

const API_BASE_URL = 'https://jcirzukmgu.us-east-1.awsapprunner.com';

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async makeRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const defaultHeaders = {
      'Content-Type': 'application/json',
    };

    const config: RequestInit = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData: ApiError = await response.json().catch(() => ({
          detail: `HTTP ${response.status}: ${response.statusText}`
        }));
        throw new Error(errorData.detail || 'An error occurred');
      }

      return await response.json();
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('Network error occurred');
    }
  }

  async sendMessage(message: string, sessionId?: string): Promise<MessageResponse> {
    const requestData: MessageRequest = { 
      message,
      session_id: sessionId 
    };
    
    return this.makeRequest<MessageResponse>('/respond', {
      method: 'POST',
      body: JSON.stringify(requestData),
    });
  }

  async getHealth(): Promise<HealthResponse> {
    return this.makeRequest<HealthResponse>('/health');
  }
}

// Export singleton instance
export const apiClient = new ApiClient();

// Utility functions for error handling
export const isApiError = (error: unknown): error is Error => {
  return error instanceof Error;
};

export const getErrorMessage = (error: unknown): string => {
  if (isApiError(error)) {
    return error.message;
  }
  return 'An unexpected error occurred';
};