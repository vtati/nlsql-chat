import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './ChatInterface.css';

const API_BASE_URL = 'http://localhost:8000';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [schema, setSchema] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Load schema on component mount
    loadSchema();
  }, []);

  const loadSchema = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/schema`);
      setSchema(response.data.schema);
    } catch (error) {
      console.error('Error loading schema:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/query`, {
        question: inputValue,
        schema: schema
      });

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.data,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'error',
        content: error.response?.data?.detail || 'An error occurred',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const renderTable = (data) => {
    if (!data.results || data.results.length === 0) {
      return <p>No results found.</p>;
    }

    return (
      <div className="table-container">
        <table className="results-table">
          <thead>
            <tr>
              {data.columns.map((column, index) => (
                <th key={index}>{column}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.results.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {data.columns.map((column, colIndex) => (
                  <td key={colIndex}>{row[column]?.toString() || ''}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        <p className="result-count">Showing {data.row_count} rows</p>
      </div>
    );
  };

  const renderMessage = (message) => {
    switch (message.type) {
      case 'user':
        return (
          <div key={message.id} className="message user-message">
            <div className="message-content">
              <p>{message.content}</p>
            </div>
            <div className="message-time">
              {message.timestamp.toLocaleTimeString()}
            </div>
          </div>
        );
      
      case 'bot':
        return (
          <div key={message.id} className="message bot-message">
            <div className="message-content">
              <div className="sql-query">
                <strong>Generated SQL:</strong>
                <pre>{message.content.sql_query}</pre>
              </div>
              <div className="query-results">
                <strong>Results:</strong>
                {renderTable(message.content)}
              </div>
            </div>
            <div className="message-time">
              {message.timestamp.toLocaleTimeString()}
            </div>
          </div>
        );
      
      case 'error':
        return (
          <div key={message.id} className="message error-message">
            <div className="message-content">
              <p><strong>Error:</strong> {message.content}</p>
            </div>
            <div className="message-time">
              {message.timestamp.toLocaleTimeString()}
            </div>
          </div>
        );
      
      default:
        return null;
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h1>Natural Language to SQL</h1>
        <p>Ask questions about your database in plain English</p>
      </div>
      
      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="welcome-message">
            <h3>Welcome! Try asking questions like:</h3>
            <ul>
              <li>"Show me all customers"</li>
              <li>"How many orders were placed last month?"</li>
              <li>"List products with price greater than 50"</li>
              <li>"Show customer names and their total orders"</li>
            </ul>
          </div>
        )}
        
        {messages.map(renderMessage)}
        
        {isLoading && (
          <div className="message bot-message loading">
            <div className="message-content">
              <p>Generating SQL query and fetching results...</p>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      <form onSubmit={handleSubmit} className="chat-input-form">
        <div className="input-container">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Ask a question about your database..."
            disabled={isLoading}
            className="chat-input"
          />
          <button 
            type="submit" 
            disabled={isLoading || !inputValue.trim()}
            className="send-button"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatInterface;