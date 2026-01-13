'use client';

/**
 * Login page.
 * Allows existing users to authenticate.
 */

import { useRouter } from 'next/navigation';
import Link from 'next/link';
import AuthForm from '@/components/AuthForm';
import { apiClient } from '@/lib/api';
import { setToken } from '@/lib/auth';
import { AuthResponse } from '@/types/user';

export default function LoginPage() {
  const router = useRouter();

  const handleLogin = async (email: string, password: string) => {
    // Call login API
    const response = await apiClient.post<AuthResponse>('/auth/login', {
      email,
      password,
    });

    // Store token
    setToken(response.access_token);

    // Redirect to tasks page
    router.push('/tasks');
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Log In</h1>
        <p style={styles.subtitle}>Welcome back! Please log in to continue</p>

        <AuthForm mode="login" onSubmit={handleLogin} />

        <p style={styles.footer}>
          Don't have an account?{' '}
          <Link href="/signup" style={styles.link}>
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    minHeight: '100vh',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#f3f4f6',
    padding: '1rem',
  },
  card: {
    backgroundColor: 'white',
    padding: '2rem',
    borderRadius: '0.5rem',
    boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
    width: '100%',
    maxWidth: '28rem',
  },
  title: {
    fontSize: '1.875rem',
    fontWeight: 'bold',
    textAlign: 'center' as const,
    marginBottom: '0.5rem',
    color: '#111827',
  },
  subtitle: {
    textAlign: 'center' as const,
    color: '#6b7280',
    marginBottom: '2rem',
  },
  footer: {
    marginTop: '1.5rem',
    textAlign: 'center' as const,
    fontSize: '0.875rem',
    color: '#6b7280',
  },
  link: {
    color: '#3b82f6',
    textDecoration: 'none',
    fontWeight: '500',
  },
};
