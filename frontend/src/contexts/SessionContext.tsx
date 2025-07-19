import { createContext, useContext, useState, useCallback } from 'react';
import type { ReactNode } from 'react';

import type { Message } from '../types/api';

export interface ChatSession {
  id: string;
  title: string;
  createdAt: Date;
  lastActivity: Date;
  messageCount: number;
  summary?: string;
  messages: Message[];
}

export interface SessionContextType {
  sessions: ChatSession[];
  currentSession: ChatSession | null;
  isLoading: boolean;
  createNewSession: (sessionId?: string) => string;
  switchToSession: (sessionId: string) => void;
  updateSessionTitle: (sessionId: string, title: string) => void;
  deleteSession: (sessionId: string) => void;
  updateSessionActivity: (sessionId: string) => void;
  addMessageToSession: (sessionId: string, message: Message) => void;
  getSessionMessages: (sessionId: string) => Message[];
  loadSession: (sessionId: string) => void;
  setLoadSessionCallback: (callback: (sessionId: string) => void) => void;
}

const SessionContext = createContext<SessionContextType | undefined>(undefined);

interface SessionProviderProps {
  children: ReactNode;
}

export function SessionProvider({ children }: SessionProviderProps) {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [currentSession, setCurrentSession] = useState<ChatSession | null>(null);
  const [isLoading] = useState(false);
  const [loadSessionCallback, setLoadSessionCallback] = useState<((sessionId: string) => void) | null>(null);

  const generateSessionId = useCallback(() => {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }, []);

  const generateSessionTitle = useCallback((messageCount: number = 0) => {
    const now = new Date();
    const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const dateStr = now.toLocaleDateString([], { month: 'short', day: 'numeric' });
    
    if (messageCount === 0) {
      return `New Session - ${dateStr} ${timeStr}`;
    }
    return `Session ${dateStr} ${timeStr}`;
  }, []);

  const createNewSession = useCallback((providedSessionId?: string): string => {
    const sessionId = providedSessionId || generateSessionId();
    const now = new Date();
    
    const newSession: ChatSession = {
      id: sessionId,
      title: generateSessionTitle(),
      createdAt: now,
      lastActivity: now,
      messageCount: 0,
      messages: [],
    };

    setSessions(prev => [newSession, ...prev]);
    setCurrentSession(newSession);
    
    return sessionId;
  }, [generateSessionId, generateSessionTitle]);

  const switchToSession = useCallback((sessionId: string) => {
    const session = sessions.find(s => s.id === sessionId);
    if (session) {
      setCurrentSession(session);
      updateSessionActivity(sessionId);
    }
  }, [sessions]);

  const updateSessionTitle = useCallback((sessionId: string, title: string) => {
    setSessions(prev => prev.map(session => 
      session.id === sessionId 
        ? { ...session, title }
        : session
    ));
    
    if (currentSession?.id === sessionId) {
      setCurrentSession(prev => prev ? { ...prev, title } : null);
    }
  }, [currentSession]);

  const deleteSession = useCallback((sessionId: string) => {
    setSessions(prev => prev.filter(session => session.id !== sessionId));
    
    if (currentSession?.id === sessionId) {
      const remainingSessions = sessions.filter(s => s.id !== sessionId);
      if (remainingSessions.length > 0) {
        setCurrentSession(remainingSessions[0]);
      } else {
        // Create a new session if no sessions remain
        createNewSession();
      }
    }
  }, [currentSession, sessions, createNewSession]);

  const updateSessionActivity = useCallback((sessionId: string) => {
    const now = new Date();
    
    setSessions(prev => prev.map(session => 
      session.id === sessionId 
        ? { 
            ...session, 
            lastActivity: now,
            // Don't increment messageCount here - addMessageToSession handles it
          }
        : session
    ));
    
    if (currentSession?.id === sessionId) {
      setCurrentSession(prev => prev ? { 
        ...prev, 
        lastActivity: now,
        // Don't increment messageCount here - addMessageToSession handles it
      } : null);
    }
  }, [currentSession]);

  const addMessageToSession = useCallback((sessionId: string, message: Message) => {
    setSessions(prev => prev.map(session => 
      session.id === sessionId 
        ? { 
            ...session, 
            messages: [...session.messages, message],
            lastActivity: new Date(),
            messageCount: session.messages.length + 1
          }
        : session
    ));
    
    if (currentSession?.id === sessionId) {
      setCurrentSession(prev => prev ? { 
        ...prev, 
        messages: [...prev.messages, message],
        lastActivity: new Date(),
        messageCount: prev.messages.length + 1
      } : null);
    }
  }, [currentSession]);

  const getSessionMessages = useCallback((sessionId: string): Message[] => {
    const session = sessions.find(s => s.id === sessionId);
    return session?.messages || [];
  }, [sessions]);

  const loadSession = useCallback((sessionId: string) => {
    if (loadSessionCallback) {
      loadSessionCallback(sessionId);
    }
  }, [loadSessionCallback]);

  const value: SessionContextType = {
    sessions,
    currentSession,
    isLoading,
    createNewSession,
    switchToSession,
    updateSessionTitle,
    deleteSession,
    updateSessionActivity,
    addMessageToSession,
    getSessionMessages,
    loadSession,
    setLoadSessionCallback: (callback) => setLoadSessionCallback(() => callback),
  };

  return (
    <SessionContext.Provider value={value}>
      {children}
    </SessionContext.Provider>
  );
}

export function useSession() {
  const context = useContext(SessionContext);
  if (context === undefined) {
    throw new Error('useSession must be used within a SessionProvider');
  }
  return context;
}