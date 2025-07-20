/**
 * Main application component
 */
import React, { useState } from 'react';
import QueryInput from './components/QueryInput';
import ResultsTable from './components/ResultsTable';
import DatabaseStatus from './components/DatabaseStatus';
import { useQuery } from './hooks/useQuery';
import { useDatabase } from './hooks/useDatabase';
import './App.css';

function App() {
  const [currentResults, setCurrentResults] = useState(null);
  const { executeQuery, isLoading: queryLoading, error: queryError } = useQuery();
  const { 
    databaseInfo, 
    healthStatus, 
    refreshAll, 
    isLoading: dbLoading 
  } = useDatabase();

  const handleQuerySubmit = async (question) => {
    try {
      const results = await executeQuery(question);
      setCurrentResults(results);
    } catch (error) {
      console.error('Query execution failed:', error);
      setCurrentResults(null);
    }
  };

  const handleRefreshDatabase = () => {
    refreshAll();
  };

  const getDatabaseTypeDisplay = () => {
    const dbType = databaseInfo?.database_type || healthStatus?.database_type;
    return dbType ? `(${dbType})` : '';
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>Natural Language to SQL</h1>
          <p className="header-subtitle">
            Ask questions about your database in plain English {getDatabaseTypeDisplay()}
          </p>
        </div>
      </header>

      <main className="app-main">
        <div className="main-content">
          {/* Database Status Section */}
          <DatabaseStatus
            databaseInfo={databaseInfo}
            healthStatus={healthStatus}
            onRefresh={handleRefreshDatabase}
            isLoading={dbLoading}
          />

          {/* Query Input Section */}
          <QueryInput
            onSubmit={handleQuerySubmit}
            isLoading={queryLoading}
            placeholder="Ask a question about your database..."
          />

          {/* Error Display */}
          {queryError && (
            <div className="error-message">
              <h3>Query Error</h3>
              <p>{queryError}</p>
            </div>
          )}

          {/* Results Display */}
          {currentResults && (
            <ResultsTable
              results={currentResults.results}
              columns={currentResults.columns}
              sqlQuery={currentResults.sql_query}
              executionTime={currentResults.execution_time_ms}
              rowCount={currentResults.row_count}
            />
          )}

          {/* Welcome Message */}
          {!currentResults && !queryError && !queryLoading && (
            <div className="welcome-message">
              <h2>Welcome to Natural Language SQL</h2>
              <p>
                Start by asking a question about your database. Here are some examples:
              </p>
              <ul>
                <li>"Show me all customers from Germany"</li>
                <li>"What are the most expensive products?"</li>
                <li>"How many orders were placed this year?"</li>
                <li>"List products by category"</li>
              </ul>
              <p>
                The system will automatically generate SQL queries and execute them safely 
                against your database.
              </p>
            </div>
          )}
        </div>
      </main>

      <footer className="app-footer">
        <div className="footer-content">
          <p>
            Natural Language to SQL v2.0 - 
            Enhanced with multi-database support
          </p>
          <div className="footer-links">
            <a href="/docs" target="_blank" rel="noopener noreferrer">
              API Documentation
            </a>
            <span>•</span>
            <a href="https://github.com" target="_blank" rel="noopener noreferrer">
              GitHub
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;