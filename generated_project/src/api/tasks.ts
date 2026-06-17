/**
 * Task API module
 * Provides functions to interact with the tasks backend.
 * All functions use the Fetch API and return typed results.
 */

export interface Task {
  _id: string;
  title: string;
  description?: string;
  category?: string;
  dueDate?: string;
  completed: boolean;
  reminder?: string;
}

const BASE_URL = 'http://localhost:5000/api/tasks';

/** Helper to handle fetch responses */
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`HTTP ${response.status}: ${errorText}`);
  }
  // For DELETE requests there may be no body
  if (response.status === 204) {
    // @ts-ignore – caller expects void
    return undefined as unknown as T;
  }
  return (await response.json()) as T;
}

/** Get all tasks */
export async function getTasks(): Promise<Task[]> {
  const response = await fetch(BASE_URL, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  });
  return handleResponse<Task[]>(response);
}

/** Get a single task by id */
export async function getTask(id: string): Promise<Task> {
  const response = await fetch(`${BASE_URL}/${encodeURIComponent(id)}`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  });
  return handleResponse<Task>(response);
}

/** Create a new task */
export async function createTask(task: Partial<Task>): Promise<Task> {
  const response = await fetch(BASE_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
    body: JSON.stringify(task),
  });
  return handleResponse<Task>(response);
}

/** Update an existing task */
export async function updateTask(
  id: string,
  updates: Partial<Task>
): Promise<Task> {
  const response = await fetch(`${BASE_URL}/${encodeURIComponent(id)}`, {
    method: 'PUT', // could also be PATCH depending on backend
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
    body: JSON.stringify(updates),
  });
  return handleResponse<Task>(response);
}

/** Delete a task */
export async function deleteTask(id: string): Promise<void> {
  const response = await fetch(`${BASE_URL}/${encodeURIComponent(id)}`, {
    method: 'DELETE',
    headers: {
      'Accept': 'application/json',
    },
  });
  await handleResponse<void>(response);
}
