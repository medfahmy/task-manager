'use client';

import { useState, useEffect } from 'react';
import { ProjectResponseDto as Project, ProjectCreateDto as CreateProjectData, ProjectUpdateDto as UpdateProjectData } from '@/lib/types.gen';
import { getAllProjectsProjectsGet, createProjectProjectsPost, deleteProjectProjectsProjectIdDelete, updateProjectProjectsProjectIdPut, completeProjectProjectsProjectIdCompletePatch } from '@/lib/sdk.gen';
import { apiClient } from '@/config/api-client';

interface ProjectListProps {
  onProjectUpdate?: () => void;
  onProjectSelect?: (project: Project) => void;
}

export default function ProjectList({ onProjectUpdate, onProjectSelect }: ProjectListProps) {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingProject, setEditingProject] = useState<Project | null>(null);
  const [newProject, setNewProject] = useState<CreateProjectData>({
    title: '',
    deadline: '',
  });

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      setLoading(true);
      const response = await getAllProjectsProjectsGet({ client: apiClient });
      setProjects(response.data || []);
    } catch (error) {
      console.error('Failed to load projects:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateProject = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const projectData = {
        ...newProject,
        deadline: newProject.deadline || undefined,
      };
      await createProjectProjectsPost({ body: projectData, client: apiClient });
      setNewProject({ title: '', deadline: '' });
      setShowCreateForm(false);
      loadProjects();
      onProjectUpdate?.();
    } catch (error) {
      console.error('Failed to create project:', error);
    }
  };

  const handleDeleteProject = async (projectId: string) => {
    try {
      await deleteProjectProjectsProjectIdDelete({ path: { project_id: projectId }, client: apiClient });
      loadProjects();
      onProjectUpdate?.();
    } catch (error) {
      console.error('Failed to delete project:', error);
    }
  };

  const handleEditProject = (project: Project) => {
    setEditingProject(project);
    setNewProject({
      title: project.title,
      deadline: project.deadline ? new Date(project.deadline).toISOString().slice(0, 16) : '',
    });
    setShowCreateForm(true);
  };

  const handleUpdateProject = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingProject) return;
    
    try {
      const updateData: UpdateProjectData = {
        title: newProject.title,
        deadline: newProject.deadline || undefined,
      };
      await updateProjectProjectsProjectIdPut({ 
        path: { project_id: editingProject.id }, 
        body: updateData, 
        client: apiClient 
      });
      setEditingProject(null);
      setNewProject({ title: '', deadline: '' });
      setShowCreateForm(false);
      loadProjects();
      onProjectUpdate?.();
    } catch (error) {
      console.error('Failed to update project:', error);
    }
  };

  const handleCompleteProject = async (projectId: string) => {
    try {
      await completeProjectProjectsProjectIdCompletePatch({ 
        path: { project_id: projectId as any }, 
        client: apiClient 
      });
      loadProjects();
      onProjectUpdate?.();
    } catch (error) {
      console.error('Failed to complete project:', error);
    }
  };

  if (loading) {
    return <div className="flex justify-center p-4">Loading projects...</div>;
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold">Projects</h2>
        <button
          onClick={() => {
            setEditingProject(null);
            setNewProject({ title: '', deadline: '' });
            setShowCreateForm(!showCreateForm);
          }}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          {showCreateForm ? 'Cancel' : 'Add Project'}
        </button>
      </div>

      {showCreateForm && (
        <form onSubmit={editingProject ? handleUpdateProject : handleCreateProject} className="bg-gray-50 p-4 rounded-lg space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Title</label>
            <input
              type="text"
              value={newProject.title}
              onChange={(e) => setNewProject({ ...newProject, title: e.target.value })}
              className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Deadline</label>
            <input
              type="datetime-local"
              value={newProject.deadline || ''}
              onChange={(e) => setNewProject({ ...newProject, deadline: e.target.value })}
              className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
            />
          </div>
          <div className="flex space-x-2">
            <button
              type="submit"
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
              {editingProject ? 'Update Project' : 'Create Project'}
            </button>
            <button
              type="button"
              onClick={() => {
                setShowCreateForm(false);
                setEditingProject(null);
                setNewProject({ title: '', deadline: '' });
              }}
              className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
            >
              Cancel
            </button>
          </div>
        </form>
      )}

      <div className="space-y-2">
        {projects.length === 0 ? (
          <p className="text-gray-500 text-center py-4">No projects found</p>
        ) : (
          projects.map((project) => (
            <div
              key={project.id}
              className={`border rounded-lg p-4 ${
                project.completed ? 'bg-green-50 border-green-200' : 'bg-white border-gray-200'
              }`}
            >
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className={`font-medium ${project.completed ? 'line-through text-gray-500' : ''}`}>
                    {project.title}
                  </h3>
                  {project.deadline && (
                    <p className="text-sm text-gray-500 mt-1">
                      Deadline: {new Date(project.deadline).toLocaleString()}
                    </p>
                  )}
                  <p className="text-xs text-gray-400 mt-1">
                    Created: {new Date(project.created_at).toLocaleString()}
                  </p>
                </div>
                <div className="flex space-x-2 ml-4">
                  {onProjectSelect && (
                    <button
                      onClick={() => onProjectSelect(project)}
                      className="bg-blue-500 text-white px-3 py-1 rounded text-sm hover:bg-blue-600"
                    >
                      View Tasks
                    </button>
                  )}
                  {!project.completed && (
                    <button
                      onClick={() => handleCompleteProject(project.id)}
                      className="bg-blue-500 text-white px-3 py-1 rounded text-sm hover:bg-blue-600"
                    >
                      Complete
                    </button>
                  )}
                  <button
                    onClick={() => handleEditProject(project)}
                    className="bg-blue-500 text-white px-3 py-1 rounded text-sm hover:bg-blue-600"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDeleteProject(project.id)}
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
