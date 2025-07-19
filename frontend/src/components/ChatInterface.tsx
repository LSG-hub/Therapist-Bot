import React from 'react';
import { Container, Row, Col, Card, Alert, Button } from 'react-bootstrap';
import { ArrowClockwise, Heart } from 'react-bootstrap-icons';
import { useChat } from '../hooks/useChat';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import LoadingIndicator from './LoadingIndicator';

const ChatInterface: React.FC = () => {
  const { messages, isLoading, error, sendMessage, clearChat } = useChat();

  return (
    <Container fluid className="h-100 py-3">
      <Row className="h-100 justify-content-center">
        <Col xs={12} md={10} lg={8} xl={6}>
          <Card className="h-100 shadow">
            {/* Header */}
            <Card.Header className="bg-primary text-white">
              <div className="d-flex justify-content-between align-items-center">
                <div className="d-flex align-items-center">
                  <Heart className="me-2" size={20} />
                  <h5 className="mb-0">Alex - Your CBT Assistant</h5>
                </div>
                <Button
                  variant="outline-light"
                  size="sm"
                  onClick={clearChat}
                  disabled={isLoading || messages.length === 0}
                  className="d-flex align-items-center"
                >
                  <ArrowClockwise size={14} className="me-1" />
                  New Session
                </Button>
              </div>
            </Card.Header>

            {/* Messages Area */}
            <Card.Body className="d-flex flex-column p-0" style={{ height: 'calc(100vh - 200px)' }}>
              {/* Error Alert */}
              {error && (
                <Alert variant="danger" className="m-3 mb-0" dismissible>
                  <strong>Connection Issue:</strong> {error}
                </Alert>
              )}

              {/* Messages */}
              <MessageList messages={messages} />

              {/* Loading Indicator */}
              {isLoading && (
                <div className="px-3 pb-2">
                  <LoadingIndicator />
                </div>
              )}
            </Card.Body>

            {/* Input Area */}
            <Card.Footer className="bg-light">
              <MessageInput
                onSendMessage={sendMessage}
                isLoading={isLoading}
              />
              
              {/* Disclaimer */}
              <div className="mt-2">
                <small className="text-muted">
                  <strong>Note:</strong> This is an AI assistant for support and guidance. 
                  For crisis situations, please contact a mental health professional or call 988.
                </small>
              </div>
            </Card.Footer>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default ChatInterface;