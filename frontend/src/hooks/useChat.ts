import { useState, useCallback } from 'react';
import type { Message, ChatState } from '../types/api';
import { apiClient, getErrorMessage } from '../utils/api';

export const useChat = () => {
  const [state, setState] = useState<ChatState>({
    messages: [],
    isLoading: false,
    error: null,
    sessionId: null,
    contextUsed: false,
  });

  const generateMessageId = (): string => {
    return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  };

  const addMessage = useCallback((message: Omit<Message, 'id' | 'timestamp'>) => {
    const newMessage: Message = {
      ...message,
      id: generateMessageId(),
      timestamp: new Date(),
    };

    setState(prev => ({
      ...prev,
      messages: [...prev.messages, newMessage],
    }));

    return newMessage;
  }, []);

  const setLoading = useCallback((loading: boolean) => {
    setState(prev => ({
      ...prev,
      isLoading: loading,
    }));
  }, []);

  const setError = useCallback((error: string | null) => {
    setState(prev => ({
      ...prev,
      error,
    }));
  }, []);

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim()) {
      setError('Please enter a message');
      return;
    }

    // Clear any previous errors
    setError(null);

    // Add user message
    addMessage({
      content: content.trim(),
      type: 'user',
    });

    // Set loading state
    setLoading(true);

    try {
      // Send message to API with current session ID
      const response = await apiClient.sendMessage(content.trim(), state.sessionId || undefined);
      
      // Update session information
      setState(prev => ({
        ...prev,
        sessionId: response.session_id,
        contextUsed: response.context_used,
      }));
      
      // Add therapist response
      addMessage({
        content: response.response,
        type: 'therapist',
      });

    } catch (error) {
      const errorMessage = getErrorMessage(error);
      
      // Add error message as therapist response
      addMessage({
        content: errorMessage,
        type: 'therapist',
        isError: true,
      });
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, [addMessage, setLoading, setError]);

  const clearChat = useCallback(() => {
    setState({
      messages: [],
      isLoading: false,
      error: null,
      sessionId: null,
      contextUsed: false,
    });
  }, []);

  const startNewSession = useCallback(() => {
    setState(prev => ({
      ...prev,
      sessionId: null,
      contextUsed: false,
      messages: [],
      error: null,
    }));
  }, []);

  return {
    messages: state.messages,
    isLoading: state.isLoading,
    error: state.error,
    sessionId: state.sessionId,
    contextUsed: state.contextUsed,
    sendMessage,
    clearChat,
    startNewSession,
  };
};