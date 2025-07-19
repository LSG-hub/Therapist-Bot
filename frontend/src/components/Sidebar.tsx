import React, { useState } from 'react';
import { 
  ChatDots, 
  Plus, 
  List, 
  Gear, 
  ChevronLeft, 
  ChevronRight,
  Trash3,
  Clock,
  Chat
} from 'react-bootstrap-icons';
import { useSession } from '../contexts/SessionContext';
import '../styles/Sidebar.css';

interface SidebarProps {
  collapsed: boolean;
  onToggle: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ collapsed, onToggle }) => {
  const { 
    sessions, 
    currentSession, 
    createNewSession, 
    deleteSession,
    loadSession
  } = useSession();
  
  const [showDeleteConfirm, setShowDeleteConfirm] = useState<string | null>(null);

  const handleNewSession = () => {
    // Create a new frontend session and switch to it
    const newSessionId = createNewSession();
    loadSession(newSessionId);
  };

  const handleDeleteSession = (sessionId: string, event: React.MouseEvent) => {
    event.stopPropagation();
    if (showDeleteConfirm === sessionId) {
      deleteSession(sessionId);
      setShowDeleteConfirm(null);
    } else {
      setShowDeleteConfirm(sessionId);
    }
  };

  const formatRelativeTime = (date: Date) => {
    const now = new Date();
    const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
    
    const diffInHours = Math.floor(diffInMinutes / 60);
    if (diffInHours < 24) return `${diffInHours}h ago`;
    
    const diffInDays = Math.floor(diffInHours / 24);
    if (diffInDays < 7) return `${diffInDays}d ago`;
    
    return date.toLocaleDateString();
  };

  return (
    <aside className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      {/* Header */}
      <div className="sidebar-header">
        <div className="sidebar-brand">
          <div className="brand-icon">
            <ChatDots size={24} />
          </div>
          {!collapsed && (
            <div className="brand-text">
              <h1 className="brand-title">Alex</h1>
              <p className="brand-subtitle">CBT Assistant</p>
            </div>
          )}
        </div>
        
        <button 
          className="sidebar-toggle"
          onClick={onToggle}
          aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {collapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
        </button>
      </div>

      {/* New Session Button */}
      <div className="sidebar-actions">
        <button 
          className="new-session-btn"
          onClick={handleNewSession}
          title={collapsed ? 'New Session' : undefined}
        >
          <Plus size={20} />
          {!collapsed && <span>New Session</span>}
        </button>
      </div>

      {/* Sessions List */}
      <div className="sidebar-content">
        {!collapsed && (
          <div className="section-header">
            <List size={16} />
            <span>Recent Sessions</span>
          </div>
        )}
        
        <div className="sessions-list">
          {sessions.length === 0 ? (
            !collapsed && (
              <div className="empty-state">
                <Chat size={32} className="empty-icon" />
                <p className="empty-text">No sessions yet</p>
                <p className="empty-subtext">Start a conversation to begin</p>
              </div>
            )
          ) : (
            sessions.map((session) => (
              <div
                key={session.id}
                className={`session-item ${
                  currentSession?.id === session.id ? 'active' : ''
                }`}
                onClick={() => loadSession(session.id)}
              >
                <div className="session-content">
                  <div className="session-icon">
                    <ChatDots size={16} />
                  </div>
                  
                  {!collapsed && (
                    <div className="session-info">
                      <h3 className="session-title">{session.title}</h3>
                      <div className="session-meta">
                        <span className="session-time">
                          <Clock size={12} />
                          {formatRelativeTime(session.lastActivity)}
                        </span>
                        <span className="session-count">
                          {session.messageCount} messages
                        </span>
                      </div>
                    </div>
                  )}
                </div>
                
                {!collapsed && sessions.length > 1 && (
                  <button
                    className={`delete-session-btn ${
                      showDeleteConfirm === session.id ? 'confirm' : ''
                    }`}
                    onClick={(e) => handleDeleteSession(session.id, e)}
                    title={
                      showDeleteConfirm === session.id 
                        ? 'Click again to confirm' 
                        : 'Delete session'
                    }
                  >
                    <Trash3 size={14} />
                  </button>
                )}
              </div>
            ))
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="sidebar-footer">
        <button 
          className="settings-btn"
          title={collapsed ? 'Settings' : undefined}
        >
          <Gear size={20} />
          {!collapsed && <span>Settings</span>}
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;