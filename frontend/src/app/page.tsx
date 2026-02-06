import Link from 'next/link';

/**
 * Home/landing page.
 * Welcome message with links to authentication pages.
 */

export default function HomePage() {
  return (
    <div style={styles.container}>
      <div style={styles.content}>
        <h1 style={styles.title}>Welcome to Todo App</h1>
        <p style={styles.description}>
          A simple and powerful task management application.
          <br />
          Organize your tasks, track your progress, and stay productive.
        </p>

        <div style={styles.buttons}>
          <Link href="/signup" style={styles.primaryButton}>
            Get Started
          </Link>
          <Link href="/login" style={styles.secondaryButton}>
            Log In
          </Link>
        </div>

        <div style={styles.features}>
          <h2 style={styles.featuresTitle}>Features</h2>
          <ul style={styles.featureList}>
            <li style={styles.featureItem}>✓ Secure authentication with JWT</li>
            <li style={styles.featureItem}>✓ Create and manage personal tasks</li>
            <li style={styles.featureItem}>✓ Track task completion</li>
            <li style={styles.featureItem}>✓ User-scoped data isolation</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    minHeight: 'calc(100vh - 60px)',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#f9fafb',
    padding: '2rem 1rem',
  },
  content: {
    textAlign: 'center' as const,
    maxWidth: '600px',
  },
  title: {
    fontSize: '3rem',
    fontWeight: 'bold',
    marginBottom: '1rem',
    color: '#111827',
  },
  description: {
    fontSize: '1.125rem',
    color: '#6b7280',
    marginBottom: '2rem',
    lineHeight: '1.75',
  },
  buttons: {
    display: 'flex',
    gap: '1rem',
    justifyContent: 'center',
    marginBottom: '3rem',
  },
  primaryButton: {
    display: 'inline-block',
    padding: '0.75rem 2rem',
    backgroundColor: '#3b82f6',
    color: 'white',
    textDecoration: 'none',
    borderRadius: '0.375rem',
    fontWeight: '500',
    transition: 'background-color 0.2s',
  },
  secondaryButton: {
    display: 'inline-block',
    padding: '0.75rem 2rem',
    backgroundColor: 'white',
    color: '#3b82f6',
    textDecoration: 'none',
    border: '1px solid #3b82f6',
    borderRadius: '0.375rem',
    fontWeight: '500',
    transition: 'all 0.2s',
  },
  features: {
    backgroundColor: 'white',
    padding: '2rem',
    borderRadius: '0.5rem',
    boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
  },
  featuresTitle: {
    fontSize: '1.5rem',
    fontWeight: 'bold',
    marginBottom: '1rem',
    color: '#111827',
  },
  featureList: {
    listStyle: 'none',
    padding: 0,
    margin: 0,
  },
  featureItem: {
    padding: '0.5rem 0',
    color: '#374151',
    fontSize: '1rem',
  },
};
