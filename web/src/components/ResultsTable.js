/**
 * Results table component for displaying query results
 */
import React, { useState } from 'react';
import './ResultsTable.css';

const ResultsTable = ({ results, columns, sqlQuery, executionTime, rowCount }) => {
  const [showSql, setShowSql] = useState(false);

  if (!results || results.length === 0) {
    return (
      <div className="results-container">
        <div className="no-results">
          <p>No results found</p>
        </div>
      </div>
    );
  }

  const exportToCSV = () => {
    const csvContent = [
      columns.join(','),
      ...results.map(row => 
        columns.map(col => {
          const value = row[col];
          // Escape quotes and wrap in quotes if contains comma
          const stringValue = String(value || '');
          return stringValue.includes(',') || stringValue.includes('"') 
            ? `"${stringValue.replace(/"/g, '""')}"` 
            : stringValue;
        }).join(',')
      )
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `query_results_${new Date().toISOString().slice(0, 10)}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  const exportToJSON = () => {
    const jsonContent = JSON.stringify(results, null, 2);
    const blob = new Blob([jsonContent], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `query_results_${new Date().toISOString().slice(0, 10)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="results-container">
      <div className="results-header">
        <div className="results-info">
          <h3>Query Results</h3>
          <div className="results-meta">
            <span className="row-count">{rowCount} rows</span>
            {executionTime && (
              <span className="execution-time">{executionTime}ms</span>
            )}
          </div>
        </div>
        
        <div className="results-actions">
          <button
            onClick={() => setShowSql(!showSql)}
            className="action-button sql-button"
          >
            {showSql ? 'Hide SQL' : 'Show SQL'}
          </button>
          <button onClick={exportToCSV} className="action-button export-button">
            Export CSV
          </button>
          <button onClick={exportToJSON} className="action-button export-button">
            Export JSON
          </button>
        </div>
      </div>

      {showSql && sqlQuery && (
        <div className="sql-display">
          <h4>Generated SQL:</h4>
          <pre className="sql-code">{sqlQuery}</pre>
        </div>
      )}

      <div className="table-container">
        <table className="results-table">
          <thead>
            <tr>
              {columns.map((column, index) => (
                <th key={index} className="table-header">
                  {column}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {results.map((row, rowIndex) => (
              <tr key={rowIndex} className="table-row">
                {columns.map((column, colIndex) => (
                  <td key={colIndex} className="table-cell">
                    {row[column] !== null && row[column] !== undefined 
                      ? String(row[column]) 
                      : '—'
                    }
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ResultsTable;