/**
 * Database status component showing connection and database information
 */
import React from 'react';
import './DatabaseStatus.css';

const DatabaseStatus = ({ databaseInfo, healthStatus, onRefresh, isLoading }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy':
        return '#28a745';
      case 'unhealthy':
        return '#dc3545';
      default:
        return '#6c757d';
    }
  };

  const getConnectionStatus = () => {
    if (!healthStatus) return 'Unknown';
    return healthStatus.database === 'connected' ? 'Connected' : 'Disconnected';
  };

  const getDatabaseType = () => {
    return databaseInfo?.database_type || healthStatus?.database_type || 'Unknown';
  };

  const getFeatures = () => {
    if (!databaseInfo?.supported_features) return [];
    
    return Object.entries(databaseInfo.supported_features).map(([key, value]) => ({
      name: key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
      supported: value
    }));
  };

  return (
    <div className="database-status">
      <div className="status-header">
        <h3>Database Status</h3>
        <button 
          onClick={onRefresh} 
          disabled={isLoading}
          className="refresh-button"
        >
          {isLoading ? '⟳' : '↻'}
        </button>
      </div>

      <div className="status-grid">
        <div className="status-item">
          <span className="status-label">Status:</span>
          <span 
            className="status-value"
            style={{ color: getStatusColor(healthStatus?.status) }}
          >
            ● {healthStatus?.status || 'Unknown'}
          </span>
        </div>

        <div className="status-item">
          <span className="status-label">Connection:</span>
          <span className="status-value">{getConnectionStatus()}</span>
        </div>

        <div className="status-item">
          <span className="status-label">Database Type:</span>
          <span className="status-value database-type">{getDatabaseType()}</span>
        </div>

        <div className="status-item">
          <span className="status-label">API Version:</span>
          <span className="status-value">{healthStatus?.version || 'Unknown'}</span>
        </div>
      </div>

      {databaseInfo?.supported_features && (
        <div className="features-section">
          <h4>Database Features</h4>
          <div className="features-grid">
            {getFeatures().map((feature, index) => (
              <div key={index} className="feature-item">
                <span className={`feature-indicator ${feature.supported ? 'supported' : 'not-supported'}`}>
                  {feature.supported ? '✓' : '✗'}
                </span>
                <span className="feature-name">{feature.name}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {healthStatus?.timestamp && (
        <div className="last-updated">
          Last updated: {new Date(healthStatus.timestamp).toLocaleString()}
        </div>
      )}
    </div>
  );
};

export default DatabaseStatus;