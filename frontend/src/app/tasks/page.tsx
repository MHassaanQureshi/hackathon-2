'use client';

/**
 * Tasks page - Main task management dashboard.
 * Allows authenticated users to view, create, update, and delete tasks.
 */

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { isAuthenticated, removeToken } from '@/lib/auth';
import { apiClient, ApiError } from '@/lib/api';
import { Task } from '@/types/task';
import TaskForm from '@/components/TaskForm';
import TaskList from '@/components/TaskList';

export default function TasksPage() {
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Check authentication and fetch tasks on mount
  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/login');
      return;
    }

    fetchTasks();
  }, [router]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await apiClient.get<Task[]>('/tasks');
      setTasks(data);
    } catch (err: any) {
      if (err instanceof ApiError && err.status === 401) {
        // Token expired or invalid, redirect to login
        removeToken();
        router.push('/login');
      } else {
        setError(err.message || 'Failed to load tasks');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (title: string, description: string) => {
    const newTask = await apiClient.post<Task>('/tasks', {
      title,
      description: description || undefined,
    });

    // Add new task to the beginning of the list
    setTasks([newTask, ...tasks]);
  };

  const handleUpdateTask = async (taskId: number, title: string, description: string) => {
    const updatedTask = await apiClient.patch<Task>(`/tasks/${taskId}`, {
      title,
      description: description || undefined,
    });

    // Update task in list
    setTasks(tasks.map(task => task.id === taskId ? updatedTask : task));
  };

  const handleDeleteTask = async (taskId: number) => {
    await apiClient.delete(`/tasks/${taskId}`);

    // Remove task from list
    setTasks(tasks.filter(task => task.id !== taskId));
  };

  const handleToggleTask = async (taskId: number) => {
    const updatedTask = await apiClient.post<Task>(`/tasks/${taskId}/toggle`, {});

    // Update task in list
    setTasks(tasks.map(task => task.id === taskId ? updatedTask : task));
  };

  const handleLogout = () => {
    removeToken();
    router.push('/login');
  };

  if (!isAuthenticated()) {
    return null;
  }

  return (
    <div style={styles.container}>
      <div style={styles.content}>
        <div style={styles.header}>
          <h1 style={styles.title}>My Tasks</h1>
          <button onClick={handleLogout} style={styles.logoutButton}>
            Log Out
          </button>
        </div>

        {error && <div style={styles.error}>{error}</div>}

        <div style={styles.createSection}>
          <h2 style={styles.sectionTitle}>Create New Task</h2>
          <TaskForm mode="create" onSubmit={handleCreateTask} />
        </div>

        <div style={styles.listSection}>
          <h2 style={styles.sectionTitle}>
            Your Tasks ({tasks.length})
          </h2>
          <TaskList
            tasks={tasks}
            loading={loading}
            onUpdate={handleUpdateTask}
            onDelete={handleDeleteTask}
            onToggle={handleToggleTask}
          />
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: 'calc(100vh - 60px)',
    backgroundColor: '#f3f4f6',
    padding: '2rem 1rem',
  },
  content: {
    maxWidth: '800px',
    margin: '0 auto',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '2rem',
  },
  title: {
    fontSize: '2rem',
    fontWeight: 'bold',
    color: '#111827',
  },
  logoutButton: {
    padding: '0.5rem 1rem',
    backgroundColor: '#ef4444',
    color: 'white',
    border: 'none',
    borderRadius: '0.375rem',
    fontSize: '0.875rem',
    fontWeight: '500',
    cursor: 'pointer',
    transition: 'background-color 0.2s',
  },
  error: {
    padding: '1rem',
    backgroundColor: '#fee2e2',
    border: '1px solid #fca5a5',
    borderRadius: '0.375rem',
    color: '#991b1b',
    marginBottom: '1.5rem',
  },
  createSection: {
    backgroundColor: 'white',
    padding: '1.5rem',
    borderRadius: '0.5rem',
    boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
    marginBottom: '2rem',
  },
  listSection: {
    marginBottom: '2rem',
  },
  sectionTitle: {
    fontSize: '1.25rem',
    fontWeight: '600',
    color: '#111827',
    marginBottom: '1rem',
  },
};
