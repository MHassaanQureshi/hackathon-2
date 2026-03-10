'use client';

/**
 * Task item component.
 * Displays individual task with edit, delete, and toggle actions.
 */

import { useState } from 'react';
import { Task } from '@/types/task';
import TaskForm from './TaskForm';

interface TaskItemProps {
  task: Task;
  onUpdate: (taskId: number, title: string, description: string) => Promise<void>;
  onDelete: (taskId: number) => Promise<void>;
  onToggle: (taskId: number) => Promise<void>;
}

export default function TaskItem({ task, onUpdate, onDelete, onToggle }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const handleUpdate = async (title: string, description: string) => {
    await onUpdate(task.id, title, description);
    setIsEditing(false);
  };

  const handleDelete = async () => {
    await onDelete(task.id);
    setShowDeleteConfirm(false);
  };

  const handleToggle = async () => {
    await onToggle(task.id);
  };

  if (isEditing) {
    return (
      <div style={styles.card}>
        <TaskForm
          mode="edit"
          initialData={task}
          onSubmit={handleUpdate}
          onCancel={() => setIsEditing(false)}
        />
      </div>
    );
  }

  return (
    <div style={styles.card}>
      <div style={styles.content}>
        <div style={styles.checkbox}>
          <input
            type="checkbox"
            checked={task.completed}
            onChange={handleToggle}
            style={styles.checkboxInput}
          />
        </div>

        <div style={styles.details}>
          <h3 style={{
            ...styles.title,
            textDecoration: task.completed ? 'line-through' : 'none',
            color: task.completed ? '#9ca3af' : '#111827',
          }}>
            {task.title}
          </h3>
          {task.description && (
            <p style={{
              ...styles.description,
              color: task.completed ? '#9ca3af' : '#6b7280',
            }}>
              {task.description}
            </p>
          )}
          <div style={styles.meta}>
            <span style={styles.date}>
              Created: {new Date(task.createdAt).toLocaleDateString()}
            </span>
            {task.completed && (
              <span style={styles.completedBadge}>Completed</span>
            )}
          </div>
        </div>

        <div style={styles.actions}>
          <button
            onClick={() => setIsEditing(true)}
            style={styles.editButton}
            title="Edit task"
          >
            Edit
          </button>
          <button
            onClick={() => setShowDeleteConfirm(true)}
            style={styles.deleteButton}
            title="Delete task"
          >
            Delete
          </button>
        </div>
      </div>

      {showDeleteConfirm && (
        <div style={styles.confirmDialog}>
          <p style={styles.confirmText}>Are you sure you want to delete this task?</p>
          <div style={styles.confirmButtons}>
            <button onClick={handleDelete} style={styles.confirmDelete}>
              Yes, Delete
            </button>
            <button onClick={() => setShowDeleteConfirm(false)} style={styles.confirmCancel}>
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

const styles = {
  card: {
    backgroundColor: 'white',
    padding: '1rem',
    borderRadius: '0.5rem',
    border: '1px solid #e5e7eb',
    boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
  },
  content: {
    display: 'flex',
    gap: '1rem',
    alignItems: 'flex-start',
  },
  checkbox: {
    paddingTop: '0.25rem',
  },
  checkboxInput: {
    width: '1.25rem',
    height: '1.25rem',
    cursor: 'pointer',
  },
  details: {
    flex: 1,
    minWidth: 0,
  },
  title: {
    fontSize: '1.125rem',
    fontWeight: '600',
    marginBottom: '0.5rem',
    wordBreak: 'break-word' as const,
  },
  description: {
    fontSize: '0.875rem',
    marginBottom: '0.5rem',
    lineHeight: '1.5',
    wordBreak: 'break-word' as const,
  },
  meta: {
    display: 'flex',
    gap: '1rem',
    alignItems: 'center',
    flexWrap: 'wrap' as const,
  },
  date: {
    fontSize: '0.75rem',
    color: '#9ca3af',
  },
  completedBadge: {
    fontSize: '0.75rem',
    padding: '0.25rem 0.5rem',
    backgroundColor: '#d1fae5',
    color: '#065f46',
    borderRadius: '0.25rem',
    fontWeight: '500',
  },
  actions: {
    display: 'flex',
    gap: '0.5rem',
  },
  editButton: {
    padding: '0.5rem 1rem',
    backgroundColor: '#3b82f6',
    color: 'white',
    border: 'none',
    borderRadius: '0.375rem',
    fontSize: '0.875rem',
    fontWeight: '500',
    cursor: 'pointer',
  },
  deleteButton: {
    padding: '0.5rem 1rem',
    backgroundColor: '#ef4444',
    color: 'white',
    border: 'none',
    borderRadius: '0.375rem',
    fontSize: '0.875rem',
    fontWeight: '500',
    cursor: 'pointer',
  },
  confirmDialog: {
    marginTop: '1rem',
    padding: '1rem',
    backgroundColor: '#fef2f2',
    border: '1px solid #fca5a5',
    borderRadius: '0.375rem',
  },
  confirmText: {
    fontSize: '0.875rem',
    color: '#991b1b',
    marginBottom: '1rem',
  },
  confirmButtons: {
    display: 'flex',
    gap: '0.5rem',
  },
  confirmDelete: {
    flex: 1,
    padding: '0.5rem',
    backgroundColor: '#ef4444',
    color: 'white',
    border: 'none',
    borderRadius: '0.375rem',
    fontSize: '0.875rem',
    fontWeight: '500',
    cursor: 'pointer',
  },
  confirmCancel: {
    flex: 1,
    padding: '0.5rem',
    backgroundColor: '#6b7280',
    color: 'white',
    border: 'none',
    borderRadius: '0.375rem',
    fontSize: '0.875rem',
    fontWeight: '500',
    cursor: 'pointer',
  },
};
