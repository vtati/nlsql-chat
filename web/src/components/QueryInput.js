/**
 * Query input component for natural language questions
 */
import React, { useState, useRef } from 'react';
import './QueryInput.css';

const QueryInput = ({ onSubmit, isLoading, placeholder }) => {
  const [question, setQuestion] = useState('');
  const inputRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (question.trim() && !isLoading) {
      onSubmit(question.trim());
      setQuestion('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const exampleQuestions = [
    "Show me all customers from Germany",
    "What are the most expensive products?",
    "How many customers are there?",
    "List products by category",
    "Show orders from this year"
  ];

  const handleExampleClick = (example) => {
    setQuestion(example);
    inputRef.current?.focus();
  };

  return (
    <div className="query-input-container">
      <form onSubmit={handleSubmit} className="query-form">
        <div className="input-group">
          <textarea
            ref={inputRef}
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={placeholder || "Ask a question about your database..."}
            className="query-textarea"
            rows="2"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!question.trim() || isLoading}
            className="submit-button"
          >
            {isLoading ? (
              <span className="loading-spinner">⏳</span>
            ) : (
              <span>Send</span>
            )}
          </button>
        </div>
      </form>

      <div className="example-questions">
        <p className="example-label">Try these examples:</p>
        <div className="example-buttons">
          {exampleQuestions.map((example, index) => (
            <button
              key={index}
              onClick={() => handleExampleClick(example)}
              className="example-button"
              disabled={isLoading}
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default QueryInput;