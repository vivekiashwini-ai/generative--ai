import React from 'react';
import { Card, Separator } from './components';

const DashboardPage = () => {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">ASLA AI Studio</h1>
      
      {/* Welcome section */}
      <Card className="mb-6">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Welcome</h2>
        <p className="text-gray-600">
          Your all-in-one AI productivity and career development platform. 
          Explore tools to enhance your skills, build your resume, and find 
          career opportunities.
        </p>
      </Card>

      {/* Feature cards section */}
      <Card className="mb-6">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Quick Access</h2>
        <Separator />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {/* Image Tools Card */}
          <div className="group p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow cursor-pointer">
            <div className="w-12 h-12 rounded-lg bg-primary-100 flex items-center justify-center group-hover:bg-primary-200 transition-colors mb-3">
              <svg className="w-6 h-6 text-primary-600" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
              </svg>
            </div>
            <h3 className="text-sm font-medium text-gray-900 dark:text-gray-100 group-hover:text-primary-600 transition-colors">
              Image Tools
            </h3>
            <p className="text-xs text-gray-500 mt-1">Background remover, resizer, compressor</p>
          </div>

          {/* Resume Builder Card */}
          <div className="group p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow cursor-pointer">
            <div className="w-12 h-12 rounded-lg bg-primary-100 flex items-center justify-center group-hover:bg-primary-200 transition-colors mb-3">
              <svg className="w-6 h-6 text-primary-600" viewBox="0 0 24 24" fill="currentColor">
                <path d="M17 2H7c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-5 5h2v2h-2V7zm0 4h2v2h-2V11zm4 5c1.1 0 2 .9 2 2v2c0 1.1-.9 2-2 2h-2c-1.1 0-2-.9-2-2v-2c0-1.1.9-2 2-2zm-2-6v2h6V9h-6z" />
              </svg>
            </div>
            <h3 className="text-sm font-medium text-gray-900 dark:text-gray-100 group-hover:text-primary-600 transition-colors">
              Resume Builder
            </h3>
            <p className="text-xs text-gray-500 mt-1">Create professional resumes</p>
          </div>

          {/* Job Matcher Card */}
          <div className="group p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow cursor-pointer">
            <div className="w-12 h-12 rounded-lg bg-primary-100 flex items-center justify-center group-hover:bg-primary-200 transition-colors mb-3">
              <svg className="w-6 h-6 text-primary-600" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 4h-3.3l-.9-2.6H17v2h3.8l.9 2.6H21v2h-5.3l-.9 2.6H7V10h5.5l.9-2.6H4v-2h3.8l.9 2.6H2v2H1c-1.1 0-2 .9-2 2v2h2l.9 2.6H19c1.1 0 2-.9 2-2v-2c0-1.1-.9-2-2-2zm-7 8c-1.1 0-2 .9-2 2v2h6v-2c0-1.1-.9-2-2-2zm-5 4h2c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2h-2c-1.1 0-2 .9-2 2v2zm5-15V2h2v2h-2V2zm0 3h2v2h-2V2zm-3 8c-1.1 0-2 .9-2 2v2h2V7c0-1.1-.9-2-2-2h-2c-1.1 0-2 .9-2 2vzm3 8c-1.1 0-2 .9-2 2v2h4v-2c0-1.1-.9-2-2-2h-2c-1.1 0-2 .9-2 2zm-7-8V2h2v2H7c-1.1 0-2 .9-2 2z" />
              </svg>
            </div>
            <h3 className="text-sm font-medium text-gray-900 dark:text-gray-100 group-hover:text-primary-600 transition-colors">
              Job Matcher
            </h3>
            <p className="text-xs text-gray-500 mt-1">Find suitable job roles</p>
          </div>

          {/* Skill Assessment Card */}
          <div className="group p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow cursor-pointer">
            <div className="w-12 h-12 rounded-lg bg-primary-100 flex items-center justify-center group-hover:bg-primary-200 transition-colors mb-3">
              <svg className="w-6 h-6 text-primary-600" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 12l10 5 10-5" />
              </svg>
            </div>
            <h3 className="text-sm font-medium text-gray-900 dark:text-gray-100 group-hover:text-primary-600 transition-colors">
              Skill Assessment
            </h3>
            <p className="text-xs text-gray-500 mt-1">Test your knowledge</p>
          </div>

          {/* Writing Assistant Card */}
          <div className="group p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow cursor-pointer">
            <div className="w-12 h-12 rounded-lg bg-primary-100 flex items-center justify-center group-hover:bg-primary-200 transition-colors mb-3">
              <svg className="w-6 h-6 text-primary-600" viewBox="0 0 24 24" fill="currentColor">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zm6 6.1c-.83 0-1.5.67-1.5 1.5v7c0 .83.67 1.5 1.5 1.5s1.5-.67 1.5-1.5v-7c0-.83-.67-1.5-1.5-1.5zM8 12c0-.66-.54-1.2-1.2-1.2S5 11.34 5 12s.54 1.2 1.2 1.2S8 12.66 8 12zm7.5 4.25l-.05.15-.85-.6-.8.55.05-.15 1.4.8 1.4-.8-.8.55.8.6-.05.15z" />
              </svg>
            </div>
            <h3 className="text-sm font-medium text-gray-900 dark:text-gray-100 group-hover:text-primary-600 transition-colors">
              Writing Assistant
            </h3>
            <p className="text-xs text-gray-500 mt-1">Generate professional content</p>
          </div>
        </div>
      </Card>

      {/* Recently used tools */}
      <Card>
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Recently Used</h2>
        <Separator />
        <p className="text-gray-500 text-sm">No recent activity yet. Start exploring the tools above!</p>
      </Card>
    </div>
  );
};

export default DashboardPage;