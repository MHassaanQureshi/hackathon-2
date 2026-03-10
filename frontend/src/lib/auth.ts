/**
 * Authentication utilities.
 * Manages JWT token storage and retrieval from localStorage.
 */

const TOKEN_KEY = 'auth_token';

/**
 * Get JWT token from localStorage.
 */
export function getToken(): string | null {
  if (typeof window === 'undefined') {
    return null;
  }
  return localStorage.getItem(TOKEN_KEY);
}

/**
 * Store JWT token in localStorage.
 */
export function setToken(token: string): void {
  if (typeof window === 'undefined') {
    return;
  }
  localStorage.setItem(TOKEN_KEY, token);
}

/**
 * Remove JWT token from localStorage.
 */
export function removeToken(): void {
  if (typeof window === 'undefined') {
    return;
  }
  localStorage.removeItem(TOKEN_KEY);
}

/**
 * Check if user is authenticated (has token).
 */
export function isAuthenticated(): boolean {
  return getToken() !== null;
}
