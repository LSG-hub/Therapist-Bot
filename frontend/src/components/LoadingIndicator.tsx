import React from 'react';
import { Robot } from 'react-bootstrap-icons';
import '../styles/LoadingIndicator.css';

interface LoadingIndicatorProps {
  variant?: 'typing' | 'thinking' | 'processing';
  size?: 'sm' | 'md' | 'lg';
  showText?: boolean;
}

const LoadingIndicator: React.FC<LoadingIndicatorProps> = ({
  variant = 'typing',
  size = 'md',
  showText = true
}) => {
  const getLoadingText = () => {
    switch (variant) {
      case 'thinking':
        return 'Alex is thinking...';
      case 'processing':
        return 'Processing your message...';
      default:
        return 'Alex is typing...';
    }
  };

  return (
    <div className={`loading-indicator ${variant} ${size}`}>
      <div className="loading-avatar">
        <Robot size={24} />
        <div className="loading-pulse"></div>
      </div>
      
      <div className="loading-content">
        {showText && (
          <div className="loading-text">
            {getLoadingText()}
          </div>
        )}
        
        <div className="loading-animation">
          {variant === 'typing' && (
            <div className="typing-dots">
              <div className="dot"></div>
              <div className="dot"></div>
              <div className="dot"></div>
            </div>
          )}
          
          {variant === 'thinking' && (
            <div className="thinking-bubbles">
              <div className="bubble"></div>
              <div className="bubble"></div>
              <div className="bubble"></div>
              <div className="bubble"></div>
            </div>
          )}
          
          {variant === 'processing' && (
            <div className="processing-spinner">
              <div className="spinner"></div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LoadingIndicator;