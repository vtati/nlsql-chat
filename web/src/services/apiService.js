/**
 * API service for communicating with the backend
 */
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => {
        console.error('API Request Error:', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => {
        console.log(`API Response: ${response.status} ${response.config.url}`);
        return response;
      },
      (error) => {
        console.error('API Response Error:', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  /**
   * Execute a natural language query
   * @param {string} question - Natural language question
   * @param {string} schema - Optional database schema override
   * @returns {Promise<Object>} Query results
   */
  async executeQuery(question, schema = null) {
    try {
      const response = await this.client.post('/query', {
        question,
        schema,
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to execute query');
    }
  }

  /**
   * Get database schema information
   * @returns {Promise<Object>} Schema information
   */
  async getSchema() {
    try {
      const response = await this.client.get('/schema');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get schema');
    }
  }

  /**
   * Get database information
   * @returns {Promise<Object>} Database information
   */
  async getDatabaseInfo() {
    try {
      const response = await this.client.get('/database-info');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get database info');
    }
  }

  /**
   * Check API health status
   * @returns {Promise<Object>} Health status
   */
  async getHealthStatus() {
    try {
      const response = await this.client.get('/health');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get health status');
    }
  }

  /**
   * Get API root information
   * @returns {Promise<Object>} API information
   */
  async getApiInfo() {
    try {
      const response = await this.client.get('/');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get API info');
    }
  }
}

// Export singleton instance
export default new ApiService();