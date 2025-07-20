/**
 * Custom hook for managing query operations
 */
import { useState, useCallback } from 'react';
import apiService from '../services/apiService';

export const useQuery = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastQuery, setLastQuery] = useState(null);

  const executeQuery = useCallback(async (question, schema = null) => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await apiService.executeQuery(question, schema);
      setLastQuery({
        question,
        result,
        timestamp: new Date().toISOString(),
      });
      return result;
    } catch (err) {
      const errorMessage = err.message || 'Failed to execute query';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const clearLastQuery = useCallback(() => {
    setLastQuery(null);
  }, []);

  return {
    executeQuery,
    isLoading,
    error,
    lastQuery,
    clearError,
    clearLastQuery,
  };
};