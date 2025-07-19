import React, { useEffect } from 'react';
import { Alert } from 'react-bootstrap';
import { 
  Robot, 
  Wifi, 
  WifiOff,
  ExclamationTriangle,
  CheckCircle
} from 'react-bootstrap-icons';
import { useChat } from '../hooks/useChat';
import { useSession } from '../contexts/SessionContext';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import LoadingIndicator from './LoadingIndicator';
import ChatHeader from './ChatHeader';
import '../styles/ChatInterface.css';

const ChatInterface: React.FC = () => {
  const { 
    messages, 
    isLoading, 
    error, 
    sessionId, 
    contextUsed, 
    isNewSession,
    sendMessage, 
    startNewSession,
    loadSession,
    connectionStatus 
  } = useChat();
  
  const { updateSessionActivity, setLoadSessionCallback } = useSession();

  // Register loadSession callback
  useEffect(() => {
    setLoadSessionCallback(loadSession);
  }, [loadSession, setLoadSessionCallback]);

  // Update session activity when messages change
  useEffect(() => {
    if (sessionId && messages.length > 0) {
      updateSessionActivity(sessionId);
    }
  }, [messages.length, sessionId, updateSessionActivity]);

  const getConnectionStatusIcon = () => {
    switch (connectionStatus) {
      case 'connected':
        return <Wifi className="status-icon connected" size={16} />;
      case 'disconnected':
        return <WifiOff className="status-icon disconnected" size={16} />;
      case 'connecting':
        return <Wifi className="status-icon connecting" size={16} />;
      default:
        return <Wifi className="status-icon" size={16} />;
    }
  };

  const getMemoryStatusIndicator = () => {
    if (isNewSession) {
      return (
        <div className="memory-status new-session">
          <div className="status-dot new"></div>
          <span>New Session</span>
        </div>
      );
    }
    
    if (contextUsed) {
      return (
        <div className="memory-status active">
          <CheckCircle className="status-icon" size={14} />
          <span>Memory Active</span>
        </div>
      );
    }
    
    return (
      <div className="memory-status inactive">
        <div className="status-dot inactive"></div>
        <span>No Context</span>
      </div>
    );
  };

  return (
    <div className="chat-interface">
      {/* Header */}
      <ChatHeader 
        sessionId={sessionId}
        contextUsed={contextUsed}
        isNewSession={isNewSession}
        onNewSession={startNewSession}
        isLoading={isLoading}
        connectionStatus={connectionStatus}
      />

      {/* Main Chat Area */}
      <div className="chat-body">
        {/* Connection Status Bar */}
        <div className={`connection-bar ${connectionStatus}`}>
          {getConnectionStatusIcon()}
          <span className="connection-text">
            {connectionStatus === 'connected' && 'Connected to Alex'}
            {connectionStatus === 'connecting' && 'Connecting...'}
            {connectionStatus === 'disconnected' && 'Connection lost - Check your internet'}
          </span>
          {getMemoryStatusIndicator()}
        </div>

        {/* Error Alert */}
        {error && (
          <div className="error-container">
            <Alert variant="danger" className="error-alert animate-slide-up">
              <ExclamationTriangle size={16} className="me-2" />
              <div>
                <strong>Connection Issue</strong>
                <p className="mb-0 mt-1">{error}</p>
              </div>
            </Alert>
          </div>
        )}

        {/* Messages Container */}
        <div className="messages-container">
          <MessageList messages={messages} isLoading={isLoading} />
          
          {/* Typing Indicator */}
          {isLoading && (
            <div className="typing-container">
              <LoadingIndicator />
            </div>
          )}
        </div>
      </div>

      {/* Input Area - Always at bottom */}
      <MessageInput
        onSendMessage={sendMessage}
        isLoading={isLoading}
        placeholder="Share what's on your mind..."
      />

      {/* Welcome Screen for Empty State */}
      {messages.length === 0 && !isLoading && (
        <div className="welcome-screen">
          <div className="welcome-content animate-fade-in">
            <div className="welcome-avatar">
              <Robot size={48} />
            </div>
            <h2 className="welcome-title">Hi! I'm Alex</h2>
            <p className="welcome-subtitle">
              Your personal CBT assistant here to help with anxiety, stress, and emotional well-being.
            </p>
            <div className="welcome-features">
              <div className="feature">
                <CheckCircle size={16} />
                <span>Evidence-based CBT techniques</span>
              </div>
              <div className="feature">
                <CheckCircle size={16} />
                <span>Personalized conversation memory</span>
              </div>
              <div className="feature">
                <CheckCircle size={16} />
                <span>Professional safety guardrails</span>
              </div>
            </div>
            <p className="welcome-prompt">
              What would you like to talk about today?
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatInterface;