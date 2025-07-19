import React from 'react';
import { 
  Robot, 
  Plus, 
  ThreeDotsVertical,
  SunFill,
  ArrowLeft
} from 'react-bootstrap-icons';
import '../styles/ChatHeader.css';

interface ChatHeaderProps {
  sessionId: string | null;
  contextUsed: boolean;
  isNewSession: boolean;
  onNewSession: () => void;
  isLoading: boolean;
  connectionStatus: 'connected' | 'connecting' | 'disconnected';
}

const ChatHeader: React.FC<ChatHeaderProps> = ({
  onNewSession,
  isLoading,
  connectionStatus
}) => {
  return (
    <header className="chat-header">
      <div className="header-left">
        {/* Mobile menu button - hidden on desktop */}
        <button className="mobile-menu-btn">
          <ArrowLeft size={20} />
        </button>
        
        <div className="alex-info">
          <div className="alex-avatar">
            <Robot size={24} />
            <div className={`status-indicator ${connectionStatus}`}></div>
          </div>
          
          <div className="alex-details">
            <h1 className="alex-name">Alex</h1>
            <p className="alex-status">
              {connectionStatus === 'connected' && (
                <span className="status-text online">
                  Online • CBT Therapist
                </span>
              )}
              {connectionStatus === 'connecting' && (
                <span className="status-text connecting">
                  Connecting...
                </span>
              )}
              {connectionStatus === 'disconnected' && (
                <span className="status-text offline">
                  Offline
                </span>
              )}
            </p>
          </div>
        </div>
      </div>

      <div className="header-right">
        <button 
          className="header-action-btn new-session-btn"
          onClick={onNewSession}
          disabled={isLoading}
          title="Start New Session"
        >
          <Plus size={18} />
          <span className="btn-text">New</span>
        </button>
        
        <button 
          className="header-action-btn theme-toggle"
          title="Toggle Theme"
        >
          <SunFill size={18} />
        </button>
        
        <button 
          className="header-action-btn menu-btn"
          title="More Options"
        >
          <ThreeDotsVertical size={18} />
        </button>
      </div>
    </header>
  );
};

export default ChatHeader;