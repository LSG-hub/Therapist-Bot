import React from 'react';
import { Spinner } from 'react-bootstrap';

interface LoadingIndicatorProps {
  text?: string;
}

const LoadingIndicator: React.FC<LoadingIndicatorProps> = ({ 
  text = 'Alex is thinking...' 
}) => {
  return (
    <div className="d-flex align-items-center text-muted py-2">
      <Spinner
        animation="border"
        size="sm"
        className="me-2"
        variant="primary"
      />
      <small className="fst-italic">{text}</small>
    </div>
  );
};

export default LoadingIndicator;