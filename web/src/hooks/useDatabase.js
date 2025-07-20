/**
 * Custom hook for managing database information
 */
import { useState, useEffect, useCallback } from 'react';
import apiService from '../services/apiService';

export const useDatabase = () => {
  const [databaseInfo, setDatabaseInfo] = useState(null);
  const [schema, setSchema] = useState(null);
  const [healthStatus, setHealthStatus] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchDatabaseInfo = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const info = await apiService.getDatabaseInfo();
      setDatabaseInfo(info);
      return info;
    } catch (err) {
      const errorMessage = err.message || 'Failed to fetch database info';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const fetchSchema = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const schemaData = await apiService.getSchema();
      setSchema(schemaData);
      return schemaData;
    } catch (err) {
      const errorMessage = err.message || 'Failed to fetch schema';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const fetchHealthStatus = useCallback(async () => {
    try {
      const health = await apiService.getHealthStatus();
      setHealthStatus(health);
      return health;
    } catch (err) {
      const errorMessage = err.message || 'Failed to fetch health status';
      setError(errorMessage);
      setHealthStatus({
        status: 'unhealthy',
        database: 'disconnected',
        database_type: 'unknown',
        version: 'unknown',
      });
      throw new Error(errorMessage);
    }
  }, []);

  const refreshAll = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      await Promise.all([
        fetchDatabaseInfo(),
        fetchSchema(),
        fetchHealthStatus(),
      ]);
    } catch (err) {
      console.error('Error refreshing database information:', err);
    } finally {
      setIsLoading(false);
    }
  }, [fetchDatabaseInfo, fetchSchema, fetchHealthStatus]);

  // Auto-fetch on mount
  useEffect(() => {
    refreshAll();
  }, [refreshAll]);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    databaseInfo,
    schema,
    healthStatus,
    isLoading,
    error,
    fetchDatabaseInfo,
    fetchSchema,
    fetchHealthStatus,
    refreshAll,
    clearError,
  };
};