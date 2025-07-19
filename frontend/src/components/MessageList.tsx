import React, { useEffect, useRef } from 'react';
import { Card, Badge } from 'react-bootstrap';
import { PersonCircle, ChatDots, ExclamationTriangle } from 'react-bootstrap-icons';
import type { Message } from '../types/api';

interface MessageListProps {
  messages: Message[];
  isLoading?: boolean;
}

const MessageBubble: React.FC<{ message: Message }> = ({ message }) => {
  const isUser = message.type === 'user';
  const isError = message.isError;

  const formatTime = (timestamp: Date) => {
    return timestamp.toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className={`d-flex mb-3 ${isUser ? 'justify-content-end' : 'justify-content-start'}`}>
      <div className={`d-flex ${isUser ? 'flex-row-reverse' : 'flex-row'} align-items-start`}>
        {/* Avatar */}
        <div className={`${isUser ? 'ms-2' : 'me-2'} text-${isUser ? 'primary' : isError ? 'danger' : 'success'}`}>
          {isUser ? (
            <PersonCircle size={32} />
          ) : isError ? (
            <ExclamationTriangle size={32} />
          ) : (
            <ChatDots size={32} />
          )}
        </div>

        {/* Message bubble */}
        <Card
          className={`border-0 shadow-sm ${isUser ? 'bg-primary text-white' : isError ? 'bg-light border-danger' : 'bg-light'}`}
          style={{ maxWidth: '70%', minWidth: '120px' }}
        >
          <Card.Body className="py-2 px-3">
            {!isUser && (
              <div className="d-flex align-items-center mb-1">
                <Badge 
                  bg={isError ? 'danger' : 'success'} 
                  className="me-2"
                  style={{ fontSize: '0.7rem' }}
                >
                  {isError ? 'Error' : 'Alex'}
                </Badge>
              </div>
            )}
            
            <div 
              className={`${isUser ? 'text-white' : isError ? 'text-danger' : 'text-dark'}`}
              style={{ 
                whiteSpace: 'pre-wrap', 
                wordWrap: 'break-word',
                lineHeight: '1.4'
              }}
            >
              {message.content}
            </div>
            
            <div 
              className={`mt-1 ${isUser ? 'text-white-50' : 'text-muted'}`}
              style={{ fontSize: '0.7rem' }}
            >
              {formatTime(message.timestamp)}
            </div>
          </Card.Body>
        </Card>
      </div>
    </div>
  );
};

const MessageList: React.FC<MessageListProps> = ({ messages }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className="text-center text-muted py-5">
        <ChatDots size={48} className="mb-3 text-muted" />
        <h5 className="mb-2">Welcome to your therapy session</h5>
        <p className="mb-0">
          Hi! I'm Alex, your CBT assistant. I'm here to help you work through your thoughts and feelings. 
          What would you like to talk about today?
        </p>
      </div>
    );
  }

  return (
    <div 
      className="flex-grow-1 overflow-auto px-3 py-2"
      style={{ maxHeight: '60vh', minHeight: '400px' }}
    >
      {messages.map((message) => (
        <MessageBubble key={message.id} message={message} />
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;