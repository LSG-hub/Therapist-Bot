import React, { useState, useRef } from 'react';
import type { KeyboardEvent } from 'react';
import { Send } from 'react-bootstrap-icons';
import '../styles/MessageInput.css';

interface MessageInputProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
  disabled?: boolean;
  placeholder?: string;
}

const MessageInput: React.FC<MessageInputProps> = ({
  onSendMessage,
  isLoading,
  disabled = false,
  placeholder = "Share what's on your mind...",
}) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isLoading && !disabled) {
      onSendMessage(message.trim());
      setMessage('');
      
      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleTextareaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
    
    // Auto-resize textarea
    const textarea = e.target;
    textarea.style.height = 'auto';
    textarea.style.height = `${Math.min(textarea.scrollHeight, 120)}px`;
  };

  const isDisabled = isLoading || disabled || !message.trim();

  return (
    <form onSubmit={handleSubmit} className="message-input-form">
      <div className="message-input-group">
        <textarea
          ref={textareaRef}
          rows={1}
          value={message}
          onChange={handleTextareaChange}
          onKeyDown={handleKeyDown}
          placeholder={isLoading ? "Alex is responding..." : placeholder}
          disabled={isLoading || disabled}
          className="message-textarea"
        />
        <button
          type="submit"
          disabled={isDisabled}
          className="send-button"
          aria-label="Send message"
        >
          <Send size={18} />
        </button>
      </div>
      <div className="input-help-text">
        Press Enter to send, Shift+Enter for new line
      </div>
    </form>
  );
};

export default MessageInput;