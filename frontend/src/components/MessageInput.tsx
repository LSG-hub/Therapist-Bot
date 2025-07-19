import React, { useState, useRef } from 'react';
import type { KeyboardEvent } from 'react';
import { Form, Button, InputGroup } from 'react-bootstrap';
import { Send } from 'react-bootstrap-icons';

interface MessageInputProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
  disabled?: boolean;
}

const MessageInput: React.FC<MessageInputProps> = ({
  onSendMessage,
  isLoading,
  disabled = false,
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
    <Form onSubmit={handleSubmit} className="mt-3">
      <InputGroup>
        <Form.Control
          ref={textareaRef}
          as="textarea"
          rows={1}
          value={message}
          onChange={handleTextareaChange}
          onKeyDown={handleKeyDown}
          placeholder={isLoading ? "Alex is responding..." : "Share what's on your mind..."}
          disabled={isLoading || disabled}
          style={{
            resize: 'none',
            minHeight: '40px',
            maxHeight: '120px',
            overflow: 'auto',
          }}
          className="border-end-0"
        />
        <Button
          type="submit"
          variant="primary"
          disabled={isDisabled}
          className="px-3"
        >
          <Send size={16} />
          <span className="visually-hidden">Send message</span>
        </Button>
      </InputGroup>
      <Form.Text className="text-muted">
        Press Enter to send, Shift+Enter for new line
      </Form.Text>
    </Form>
  );
};

export default MessageInput;