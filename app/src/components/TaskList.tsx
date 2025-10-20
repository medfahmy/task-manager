'use client';

import { useState, useEffect } from 'react';
import { TaskResponseDto as Task, TaskCreateDto as CreateTaskData, TaskUpdateDto as UpdateTaskData, ProjectResponseDto as Project } from '@/lib/types.gen';
import { getAllTasksTasksGet, createTaskTasksPost, deleteTaskTasksTaskIdDelete, completeTaskTasksTaskIdCompletePatch, getProjectTasksProjectsProjectIdTasksGet, updateTaskTasksTaskIdPut, linkTaskToProjectProjectsProjectIdTasksTaskIdLinkPost, unlinkTaskFromProjectProjectsProjectIdTasksTaskIdUnlinkDelete, getAllProjectsProjectsGet } from '@/lib/sdk.gen';
import { apiClient } from '@/config/api-client';

interface TaskListProps {
  projectId?: string;
  onTaskUpdate?: () => void;
}

export default function TaskList({ projectId, onTaskUpdate }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [filter, setFilter] = useState<'all' | 'completed' | 'open' | 'overdue'>('all');
  const [newTask, setNewTask] = useState<CreateTaskData>({
    title: '',
    description: '',
    deadline: '',
  });

  useEffect(() => {
    loadTasks();
    if (!projectId) {
      loadProjects();
    }
  }, [projectId]);

  const loadTasks = async () => {
    try {
      setLoading(true);
      const response = projectId 
        ? await getProjectTasksProjectsProjectIdTasksGet({ path: { project_id: projectId }, client: apiClient })
        : await getAllTasksTasksGet({ client: apiClient });
      setTasks(response.data || []);
    } catch (error) {
      console.error('Failed to load tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadProjects = async () => {
    try {
      const response = await getAllProjectsProjectsGet({ client: apiClient });
      setProjects(response.data || []);
    } catch (error) {
      console.error('Failed to load projects:', error);
    }
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const taskData = {
        ...newTask,
        project_id: projectId,
        deadline: newTask.deadline || undefined,
      };
      await createTaskTasksPost({ body: taskData, client: apiClient });
      setNewTask({ title: '', description: '', deadline: '' });
      setShowCreateForm(false);
      loadTasks();
      onTaskUpdate?.();
    } catch (error) {
      console.error('Failed to create task:', error);
    }
  };

  const handleCompleteTask = async (taskId: string) => {
    try {
      await completeTaskTasksTaskIdCompletePatch({ path: { task_id: taskId }, client: apiClient });
      loadTasks();
      onTaskUpdate?.();
    } catch (error) {
      console.error('Failed to complete task:', error);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    try {
      await deleteTaskTasksTaskIdDelete({ path: { task_id: taskId }, client: apiClient });
      loadTasks();
      onTaskUpdate?.();
    } catch (error) {
      console.error('Failed to delete task:', error);
    }
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setNewTask({
      title: task.title,
      description: task.description || '',
      deadline: task.deadline ? new Date(task.deadline).toISOString().slice(0, 16) : '',
    });
    setShowCreateForm(true);
  };

  const handleUpdateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingTask) return;
    
    try {
      const updateData: UpdateTaskData = {
        title: newTask.title,
        description: newTask.description,
        deadline: newTask.deadline || undefined,
      };
      await updateTaskTasksTaskIdPut({ 
        path: { task_id: editingTask.id }, 
        body: updateData, 
        client: apiClient 
      });
      setEditingTask(null);
      setNewTask({ title: '', description: '', deadline: '' });
      setShowCreateForm(false);
      loadTasks();
      onTaskUpdate?.();
    } catch (error) {
      console.error('Failed to update task:', error);
    }
  };

  const handleLinkToProject = async (taskId: string, projectId: string) => {
    try {
      await linkTaskToProjectProjectsProjectIdTasksTaskIdLinkPost({ 
        path: { project_id: projectId, task_id: taskId }, 
        client: apiClient 
      });
      loadTasks();
      onTaskUpdate?.();
    } catch (error) {
      console.error('Failed to link task to project:', error);
    }
  };

  const handleUnlinkFromProject = async (taskId: string) => {
    try {
      await unlinkTaskFromProjectProjectsProjectIdTasksTaskIdUnlinkDelete({ 
        path: { project_id: 'dummy', task_id: taskId }, 
        client: apiClient 
      });
      loadTasks();
      onTaskUpdate?.();
    } catch (error) {
      console.error('Failed to unlink task from project:', error);
    }
  };

  const getFilteredTasks = () => {
    let filtered = tasks;
    
    if (filter === 'completed') {
      filtered = tasks.filter(task => task.completed);
    } else if (filter === 'open') {
      filtered = tasks.filter(task => !task.completed);
    } else if (filter === 'overdue') {
      const now = new Date();
      filtered = tasks.filter(task => 
        !task.completed && 
        task.deadline && 
        new Date(task.deadline) < now
      );
    }
    
    return filtered;
  };

  if (loading) {
    return <div className="flex justify-center p-4">Loading tasks...</div>;
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold">
          {projectId ? 'Project Tasks' : 'All Tasks'}
        </h2>
        <div className="flex space-x-2">
          {!projectId && (
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value as any)}
              className="border border-gray-300 rounded px-3 py-2"
            >
              <option value="all">All Tasks</option>
              <option value="open">Open Tasks</option>
              <option value="completed">Completed Tasks</option>
              <option value="overdue">Overdue Tasks</option>
            </select>
          )}
          <button
            onClick={() => {
              setEditingTask(null);
              setNewTask({ title: '', description: '', deadline: '' });
              setShowCreateForm(!showCreateForm);
            }}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            {showCreateForm ? 'Cancel' : 'Add Task'}
          </button>
        </div>
      </div>

      {showCreateForm && (
        <form onSubmit={editingTask ? handleUpdateTask : handleCreateTask} className="bg-gray-50 p-4 rounded-lg space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Title</label>
            <input
              type="text"
              value={newTask.title}
              onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
              className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Description</label>
            <textarea
              value={newTask.description || ''}
              onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
              className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
              rows={3}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Deadline</label>
            <input
              type="datetime-local"
              value={newTask.deadline || ''}
              onChange={(e) => setNewTask({ ...newTask, deadline: e.target.value })}
              className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
            />
          </div>
          <div className="flex space-x-2">
            <button
              type="submit"
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
              {editingTask ? 'Update Task' : 'Create Task'}
            </button>
            <button
              type="button"
              onClick={() => {
                setShowCreateForm(false);
                setEditingTask(null);
                setNewTask({ title: '', description: '', deadline: '' });
              }}
              className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
            >
              Cancel
            </button>
          </div>
        </form>
      )}

      <div className="space-y-2">
        {getFilteredTasks().length === 0 ? (
          <p className="text-gray-500 text-center py-4">No tasks found</p>
        ) : (
          getFilteredTasks().map((task) => (
            <div
              key={task.id}
              className={`border rounded-lg p-4 ${
                task.completed ? 'bg-green-50 border-green-200' : 'bg-white border-gray-200'
              }`}
            >
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className={`font-medium ${task.completed ? 'line-through text-gray-500' : ''}`}>
                    {task.title}
                  </h3>
                  {task.description && (
                    <p className="text-gray-600 text-sm mt-1">{task.description}</p>
                  )}
                  {task.deadline && (
                    <p className="text-sm text-gray-500 mt-1">
                      Deadline: {new Date(task.deadline).toLocaleString()}
                    </p>
                  )}
                  {task.project_id && (
                    <p className="text-sm text-blue-600 mt-1">
                      Project: {projects.find(p => p.id === task.project_id)?.title || 'Unknown Project'}
                    </p>
                  )}
                  <p className="text-xs text-gray-400 mt-1">
                    Created: {new Date(task.created_at).toLocaleString()}
                  </p>
                </div>
                <div className="flex space-x-2 ml-4">
                  {!task.completed && (
                    <button
                      onClick={() => handleCompleteTask(task.id)}
                      className="bg-blue-500 text-white px-3 py-1 rounded text-sm hover:bg-blue-600"
                    >
                      Complete
                    </button>
                  )}
                  <button
                    onClick={() => handleEditTask(task)}
                    className="bg-blue-500 text-white px-3 py-1 rounded text-sm hover:bg-blue-600"
                  >
                    Edit
                  </button>
                  {!projectId && !task.project_id && (
                    <select
                      onChange={(e) => e.target.value && handleLinkToProject(task.id, e.target.value)}
                      className="border border-gray-300 rounded px-2 py-1 text-sm"
                      defaultValue=""
                    >
                      <option value="">Link to Project</option>
                      {projects.map(project => (
                        <option key={project.id} value={project.id}>{project.title}</option>
                      ))}
                    </select>
                  )}
                  {!projectId && task.project_id && (
                    <button
                      onClick={() => handleUnlinkFromProject(task.id)}
                      className="bg-blue-500 text-white px-3 py-1 rounded text-sm hover:bg-blue-600"
                    >
                      Unlink
                    </button>
                  )}
                  <button
                    onClick={() => handleDeleteTask(task.id)}
                    className="bg-red-500 text-white px-3 py-1 rounded text-sm hover:bg-red-600"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
