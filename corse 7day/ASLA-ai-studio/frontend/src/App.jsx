import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import SidebarLayout from './layouts/SidebarLayout';
import DashboardPage from './pages/DashboardPage';
import ImageToolsPage from './pages/ImageToolsPage';
import ResumeBuilderPage from './pages/ResumeBuilderPage';
import JobMatcherPage from './pages/JobMatcherPage';
import SkillAdvisorPage from './pages/SkillAdvisorPage';
import SkillAssessmentPage from './pages/SkillAssessmentPage';
import WritingAssistantPage from './pages/WritingAssistantPage';
import MyProgressPage from './pages/MyProgressPage';
import SettingsPage from './pages/SettingsPage';

function App() {
  return (
    <BrowserRouter>
      <SidebarLayout>
        <DashboardPage />
        <ImageToolsPage />
        <ResumeBuilderPage />
        <JobMatcherPage />
        <SkillAdvisorPage />
        <SkillAssessmentPage />
        <WritingAssistantPage />
        <MyProgressPage />
        <SettingsPage />
      </SidebarLayout>
    </BrowserRouter>
  );
}

export default App;