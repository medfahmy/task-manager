'use client';

import { useState } from 'react';
import TaskList from '@/components/TaskList';
import ProjectList from '@/components/ProjectList';
import { ProjectResponseDto as Project } from '@/lib/types.gen';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'tasks' | 'projects'>('tasks');
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Task Manager</h1>
        </header>

        <div className="bg-white rounded-lg shadow-sm">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-6">
              <button
                onClick={() => setActiveTab('tasks')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'tasks'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Tasks
              </button>
              <button
                onClick={() => setActiveTab('projects')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'projects'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Projects
              </button>
            </nav>
          </div>

          <div className="p-6">
            {selectedProject ? (
              <div className="space-y-4">
                <div className="flex items-center space-x-4">
                  <button
                    onClick={() => setSelectedProject(null)}
                    className="text-blue-600 hover:text-blue-800"
                  >
                    ← Back to Projects
                  </button>
                  <h2 className="text-xl font-semibold">
                    Tasks for: {selectedProject.title}
                  </h2>
                </div>
                <TaskList projectId={selectedProject.id} />
              </div>
            ) : (
              <>
                {activeTab === 'tasks' && (
                  <TaskList />
                )}
                {activeTab === 'projects' && (
                  <ProjectList onProjectSelect={setSelectedProject} />
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}