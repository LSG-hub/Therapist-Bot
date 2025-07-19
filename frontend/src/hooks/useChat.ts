import { useState, useCallback } from 'react';
import type { Message, ChatState } from '../types/api';
import { apiClient, getErrorMessage } from '../utils/api';
import { useSession } from '../contexts/SessionContext';

export const useChat = () => {
  const { currentSession, createNewSession, switchToSession, addMessageToSession, getSessionMessages } = useSession();
  
  const [state, setState] = useState<ChatState>({
    messages: [],
    isLoading: false,
    error: null,
    sessionId: null,
    contextUsed: false,
  });
  
  const [connectionStatus, setConnectionStatus] = useState<'connected' | 'connecting' | 'disconnected'>('connected');

  const generateMessageId = (): string => {
    return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  };

  const addMessage = useCallback((message: Omit<Message, 'id' | 'timestamp'>, sessionId?: string) => {
    const newMessage: Message = {
      ...message,
      id: generateMessageId(),
      timestamp: new Date(),
    };

    setState(prev => ({
      ...prev,
      messages: [...prev.messages, newMessage],
    }));

    // Also add to session storage - use provided sessionId or current session
    const targetSessionId = sessionId || currentSession?.id || state.sessionId;
    if (targetSessionId) {
      addMessageToSession(targetSessionId, newMessage);
    }

    return newMessage;
  }, [currentSession, addMessageToSession, state.sessionId]);

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
    setConnectionStatus('connecting');

    // Add user message
    addMessage({
      content: content.trim(),
      type: 'user',
    }, state.sessionId || undefined);

    // Set loading state
    setLoading(true);

    try {
      // Send message to API with current session ID
      const response = await apiClient.sendMessage(content.trim(), state.sessionId || undefined);
      
      setConnectionStatus('connected');
      
      // Update session information
      setState(prev => ({
        ...prev,
        sessionId: response.session_id,
        contextUsed: response.context_used,
      }));

      // If this is a new session (no current session or different session ID), create frontend session
      if (response.session_id && (!state.sessionId || state.sessionId !== response.session_id)) {
        // Check if we already have this session in our context
        const sessions = getSessionMessages ? [getSessionMessages(response.session_id)] : [];
        if (sessions[0]?.length === 0 || !sessions[0]) {
          // Create new frontend session with backend session ID
          createNewSession(response.session_id);
        }
      }

      
      // Add therapist response
      addMessage({
        content: response.response,
        type: 'therapist',
      }, response.session_id);

    } catch (error) {
      const errorMessage = getErrorMessage(error);
      setConnectionStatus('disconnected');
      
      // Add error message as therapist response
      addMessage({
        content: errorMessage,
        type: 'therapist',
        isError: true,
      }, state.sessionId || undefined);
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, [addMessage, setLoading, setError, state.sessionId]);

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
    // Don't create session context yet - wait for backend session ID
    setState(prev => ({
      ...prev,
      sessionId: null, // Let the backend create the session ID
      contextUsed: false,
      messages: [],
      error: null,
    }));
  }, []);

  const loadSession = useCallback((sessionId: string) => {
    const sessionMessages = getSessionMessages(sessionId);
    switchToSession(sessionId);
    setState(prev => ({
      ...prev,
      sessionId,
      messages: sessionMessages,
      contextUsed: sessionMessages.length > 0,
      error: null,
    }));
    
    // Log for debugging
    console.log('Loading session:', sessionId, 'with', sessionMessages.length, 'messages');
    sessionMessages.forEach((msg, i) => {
      console.log(`Message ${i + 1} (${msg.type}):`, msg.content.substring(0, 50) + '...');
    });
  }, [switchToSession, getSessionMessages]);

  // Check if this is a new session (no previous messages)
  const isNewSession = state.messages.length === 0 && !state.contextUsed;

  return {
    messages: state.messages,
    isLoading: state.isLoading,
    error: state.error,
    sessionId: state.sessionId,
    contextUsed: state.contextUsed,
    isNewSession,
    connectionStatus,
    sendMessage,
    clearChat,
    startNewSession,
    loadSession,
  };
};