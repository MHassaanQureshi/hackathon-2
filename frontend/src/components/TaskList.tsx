'use client';

/**
 * Task list component.
 * Displays list of tasks with empty and loading states.
 */

import { Task } from '@/types/task';
import TaskItem from './TaskItem';

interface TaskListProps {
  tasks: Task[];
  loading: boolean;
  onUpdate: (taskId: number, title: string, description: string) => Promise<void>;
  onDelete: (taskId: number) => Promise<void>;
  onToggle: (taskId: number) => Promise<void>;
}

export default function TaskList({ tasks, loading, onUpdate, onDelete, onToggle }: TaskListProps) {
  if (loading) {
    return (
      <div style={styles.emptyState}>
        <p style={styles.emptyText}>Loading tasks...</p>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div style={styles.emptyState}>
        <p style={styles.emptyText}>No tasks yet</p>
        <p style={styles.emptySubtext}>Create your first task to get started!</p>
      </div>
    );
  }

  return (
    <div style={styles.list}>
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onUpdate={onUpdate}
          onDelete={onDelete}
          onToggle={onToggle}
        />
      ))}
    </div>
  );
}

const styles = {
  list: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '1rem',
  },
  emptyState: {
    padding: '3rem',
    textAlign: 'center' as const,
    backgroundColor: 'white',
    borderRadius: '0.5rem',
    border: '2px dashed #d1d5db',
  },
  emptyText: {
    fontSize: '1.125rem',
    fontWeight: '500',
    color: '#6b7280',
    marginBottom: '0.5rem',
  },
  emptySubtext: {
    fontSize: '0.875rem',
    color: '#9ca3af',
  },
};
