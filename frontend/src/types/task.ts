/**
 * Task type definitions.
 * Matches backend Task model structure.
 */

export interface Task {
  id: number;
  userId: number;
  title: string;
  description: string | null;
  completed: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface TaskCreateRequest {
  title: string;
  description?: string;
}

export interface TaskUpdateRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}
