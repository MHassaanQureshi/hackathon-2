/**
 * API client for backend communication.
 * Handles authentication headers, error handling, and request/response processing.
 */

import { getToken } from './auth';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public errors?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

interface RequestOptions {
  method: string;
  headers: Record<string, string>;
  body?: string;
}

/**
 * Make authenticated API request.
 */
async function request<T>(
  endpoint: string,
  options: Partial<RequestOptions> = {}
): Promise<T> {
  const token = getToken();

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  // Add authorization header if token exists
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const url = `${API_URL}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers,
  });

  // Handle non-JSON responses (like 204 No Content)
  if (response.status === 204) {
    return undefined as T;
  }

  const data = await response.json();

  if (!response.ok) {
    throw new ApiError(
      data.detail || 'An error occurred',
      response.status,
      data.errors
    );
  }

  return data;
}

/**
 * API client methods.
 */
export const apiClient = {
  /**
   * GET request.
   */
  get: <T>(endpoint: string): Promise<T> => {
    return request<T>(endpoint, { method: 'GET' });
  },

  /**
   * POST request.
   */
  post: <T>(endpoint: string, data?: any): Promise<T> => {
    return request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /**
   * PATCH request.
   */
  patch: <T>(endpoint: string, data?: any): Promise<T> => {
    return request<T>(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  },

  /**
   * DELETE request.
   */
  delete: <T>(endpoint: string): Promise<T> => {
    return request<T>(endpoint, { method: 'DELETE' });
  },
};
