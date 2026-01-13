'use client';

/**
 * Task form component.
 * Used for creating and editing tasks.
 */

import { useState, FormEvent } from 'react';
import { Task } from '@/types/task';

interface TaskFormProps {
  mode: 'create' | 'edit';
  initialData?: Task;
  onSubmit: (title: string, description: string) => Promise<void>;
  onCancel?: () => void;
}

export default function TaskForm({ mode, initialData, onSubmit, onCancel }: TaskFormProps) {
  const [title, setTitle] = useState(initialData?.title || '');
  const [description, setDescription] = useState(initialData?.description || '');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await onSubmit(title, description);
      if (mode === 'create') {
        // Reset form after successful creation
        setTitle('');
        setDescription('');
      }
    } catch (err: any) {
      setError(err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <div style={styles.field}>
        <label htmlFor="title" style={styles.label}>
          Title <span style={styles.required}>*</span>
        </label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          maxLength={100}
          disabled={loading}
          style={styles.input}
          placeholder="Enter task title"
        />
        <div style={styles.charCount}>
          {title.length}/100 characters
        </div>
      </div>

      <div style={styles.field}>
        <label htmlFor="description" style={styles.label}>
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          maxLength={500}
          disabled={loading}
          style={styles.textarea}
          placeholder="Enter task description (optional)"
          rows={4}
        />
        <div style={styles.charCount}>
          {description.length}/500 characters
        </div>
      </div>

      {error && <div style={styles.error}>{error}</div>}

      <div style={styles.buttons}>
        <button type="submit" disabled={loading} style={styles.submitButton}>
          {loading ? 'Saving...' : mode === 'create' ? 'Create Task' : 'Save Changes'}
        </button>
        {mode === 'edit' && onCancel && (
          <button type="button" onClick={onCancel} disabled={loading} style={styles.cancelButton}>
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}

const styles = {
  form: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '1rem',
  },
  field: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '0.5rem',
  },
  label: {
    fontSize: '0.875rem',
    fontWeight: '500',
    color: '#374151',
  },
  required: {
    color: '#ef4444',
  },
  input: {
    padding: '0.75rem',
    border: '1px solid #d1d5db',
    borderRadius: '0.375rem',
    fontSize: '1rem',
    outline: 'none',
  },
  textarea: {
    padding: '0.75rem',
    border: '1px solid #d1d5db',
    borderRadius: '0.375rem',
    fontSize: '1rem',
    outline: 'none',
    resize: 'vertical' as const,
    fontFamily: 'inherit',
  },
  charCount: {
    fontSize: '0.75rem',
    color: '#6b7280',
    textAlign: 'right' as const,
  },
  error: {
    padding: '0.75rem',
    backgroundColor: '#fee2e2',
    border: '1px solid #fca5a5',
    borderRadius: '0.375rem',
    color: '#991b1b',
    fontSize: '0.875rem',
  },
  buttons: {
    display: 'flex',
    gap: '0.5rem',
  },
  submitButton: {
    flex: 1,
    padding: '0.75rem',
    backgroundColor: '#3b82f6',
    color: 'white',
    border: 'none',
    borderRadius: '0.375rem',
    fontSize: '1rem',
    fontWeight: '500',
    cursor: 'pointer',
  },
  cancelButton: {
    flex: 1,
    padding: '0.75rem',
    backgroundColor: '#6b7280',
    color: 'white',
    border: 'none',
    borderRadius: '0.375rem',
    fontSize: '1rem',
    fontWeight: '500',
    cursor: 'pointer',
  },
};
