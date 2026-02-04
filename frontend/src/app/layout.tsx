import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Todo App - Phase II',
  description: 'Full-stack todo application with authentication',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body style={{ margin: 0, fontFamily: 'system-ui, sans-serif' }}>
        <nav style={styles.nav}>
          <div style={styles.navContainer}>
            <Link href="/" style={styles.logo}>
              Todo App
            </Link>
            <div style={styles.navLinks}>
              <Link href="/login" style={styles.navLink}>
                Log In
              </Link>
              <Link href="/signup" style={styles.navLink}>
                Sign Up
              </Link>
              <Link href="/tasks" style={styles.navLink}>
                Tasks
              </Link>
            </div>
          </div>
        </nav>
        {children}
      </body>
    </html>
  );
}

const styles = {
  nav: {
    backgroundColor: '#1f2937',
    borderBottom: '1px solid #374151',
  },
  navContainer: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '1rem',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  logo: {
    fontSize: '1.25rem',
    fontWeight: 'bold',
    color: 'white',
    textDecoration: 'none',
  },
  navLinks: {
    display: 'flex',
    gap: '1.5rem',
  },
  navLink: {
    color: '#d1d5db',
    textDecoration: 'none',
    fontSize: '0.875rem',
    fontWeight: '500',
    transition: 'color 0.2s',
  },
};
