// src/components/TaskItem.tsx

import React from "react";
import { Task } from "../api/tasks";

/**
 * Props for the TaskItem component.
 */
interface TaskItemProps {
  /** The task object to display */
  task: Task;
  /** Called when the user toggles the completed checkbox */
  onToggleComplete: (id: string) => void;
  /** Called when the user clicks the Edit button */
  onEdit: (task: Task) => void;
  /** Called when the user clicks the Delete button */
  onDelete: (id: string) => void;
}

/**
 * Functional component that renders a single task row.
 * It displays a checkbox, title, optional category & due date,
 * and Edit / Delete actions.
 */
const TaskItem: React.FC<TaskItemProps> = ({
  task,
  onToggleComplete,
  onEdit,
  onDelete,
}) => {
  const handleCheckboxChange = () => {
    onToggleComplete(task._id);
  };

  const handleEdit = () => {
    onEdit(task);
  };

  const handleDelete = () => {
    // Confirm deletion for a better UX
    if (window.confirm("Are you sure you want to delete this task?")) {
      onDelete(task._id);
    }
  };

  // Simple inline styles to keep the UI clean without external CSS
  const containerStyle: React.CSSProperties = {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "8px",
    borderBottom: "1px solid #e0e0e0",
    backgroundColor: task.completed ? "#f5f5f5" : "#fff",
  };

  const infoStyle: React.CSSProperties = {
    display: "flex",
    flexDirection: "column",
    marginLeft: "8px",
    flexGrow: 1,
  };

  const titleStyle: React.CSSProperties = {
    fontWeight: task.completed ? "normal" : "bold",
    textDecoration: task.completed ? "line-through" : "none",
    margin: 0,
  };

  const metaStyle: React.CSSProperties = {
    fontSize: "0.85rem",
    color: "#666",
  };

  const buttonStyle: React.CSSProperties = {
    marginLeft: "4px",
    padding: "4px 8px",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
  };

  const editButtonStyle: React.CSSProperties = {
    ...buttonStyle,
    backgroundColor: "#1976d2",
    color: "white",
  };

  const deleteButtonStyle: React.CSSProperties = {
    ...buttonStyle,
    backgroundColor: "#d32f2f",
    color: "white",
  };

  return (
    <div style={containerStyle} data-testid="task-item">
      <input
        type="checkbox"
        checked={task.completed}
        onChange={handleCheckboxChange}
        aria-label="Mark task as completed"
      />
      <div style={infoStyle}>
        <p style={titleStyle}>{task.title}</p>
        <div style={metaStyle}>
          {task.category && <span>Category: {task.category} </span>}
          {task.dueDate && (
            <span>
              Due: {new Date(task.dueDate).toLocaleDateString(undefined, {
                year: "numeric",
                month: "short",
                day: "numeric",
              })}
            </span>
          )}
        </div>
      </div>
      <div>
        <button style={editButtonStyle} onClick={handleEdit} aria-label="Edit task">
          Edit
        </button>
        <button
          style={deleteButtonStyle}
          onClick={handleDelete}
          aria-label="Delete task"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default TaskItem;
