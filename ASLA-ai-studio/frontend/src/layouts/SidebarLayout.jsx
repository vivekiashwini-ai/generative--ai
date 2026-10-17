import React from 'react';
import { Link } from 'react-router-dom';
import { Menu, X, Settings, User, LayoutDashboard, List, Search, FileText, Image, LayoutList, Users, Mail, Palette, GraduationCap, ChartBar, FolderDownload, Heart, Shield, LogOut } from 'lucide-react';

const SidebarLayout = ({ children }) => {
  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
      {/* Sidebar */}
      <aside className="w-64 border-r border-gray-200 dark:border-gray-700 flex-shrink-0 p-4">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-xl font-bold text-gray-900 dark:text-gray-100">ASLA AI Studio</h2>
          <button 
            className="p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            aria-label="Toggle sidebar"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <nav className="space-y-2">
          <Link to="/" className="flex items-center px-3 py-2 rounded hover:bg-primary-100 dark:hover:bg-primary-900 text-gray-700 dark:text-gray-300 font-medium transition-colors">
            <LayoutDashboard className="w-5 h-5 mr-3" />
            Dashboard
          </Link>

          <Link to="/image-tools" className="flex items-center px-3 py-2 rounded hover:bg-primary-100 dark:hover:bg-primary-900 text-gray-700 dark:text-gray-300 font-medium transition-colors">
            <Image className="w-5 h-5 mr-3" />
            Image Tools
          </Link>

          <Link to="/resume-builder" className="flex items-center px-3 py-2 rounded hover:bg-primary-100 dark:hover:bg-primary-900 text-gray-700 dark:text-gray-300 font-medium transition-colors">
            <FileText className="w-5 h-5 mr-3" />
            Resume Builder
          </Link>

          <Link to="/job-matcher" className="flex items-center px-3 py-2 rounded hover:bg-primary-100 dark:hover:bg-primary-900 text-gray-700 dark:text-gray-300 font-medium transition-colors">
            <Users className="w-5 h-5 mr-3" />
            Job Matcher
          </Link>

          <Link to="/skill-advisor" className="flex items-center px-3 py-2 rounded hover:bg-primary-100 dark:hover:bg-primary-900 text-gray-700 dark:text-gray-300 font-medium transition-colors">
            <Palette className="w-5 h-5 mr-3" />
            Skill Advisor
          </Link>

          <Link to="/skill-assessment" className="flex items-center px-3 py-2 rounded hover:bg-primary-100 dark:hover:bg-primary-900 text-gray-700 dark:text-gray-300 font-medium transition-colors">
            <ChartBar className="w-5 h-5 mr-3" />
            Skill Assessment
          </Link>

          <Link to="/writing-assistant" className="flex items-center px-3 py-2 rounded hover:bg-primary-100 dark:hover:bg-primary-900 text-gray-700 dark:text-gray-300 font-medium transition-colors">
            <Mail className="w-5 h-5 mr-3" />
            Writing Assistant
          </Link>

          <Link to="/my-progress" className="flex items-center px-3 py-2 rounded hover:bg-primary-100 dark:hover:bg-primary-900 text-gray-700 dark:text-gray-300 font-medium transition-colors">
            <FolderDownload className="w-5 h-5 mr-3" />
            My Progress
          </Link>

          <Link to="/settings" className="flex items-center px-3 py-2 rounded hover:bg-primary-100 dark:hover:bg-primary-900 text-gray-700 dark:text-gray-300 font-medium transition-colors">
            <Settings className="w-5 h-5 mr-3" />
            Settings
          </Link>
        </nav>
      </aside>

      {/* Main content */}
      <main className="flex-1 p-6 overflow-y-auto">
        {children}
      </main>
    </div>
  );
};

export default SidebarLayout;