import { createRoutesFromElements, Router } from 'react-router-dom';
import DashboardPage from './pages/DashboardPage';
import ImageToolsPage from './pages/ImageToolsPage';
import ResumeBuilderPage from './pages/ResumeBuilderPage';
import JobMatcherPage from './pages/JobMatcherPage';
import SkillAdvisorPage from './pages/SkillAdvisorPage';
import SkillAssessmentPage from './pages/SkillAssessmentPage';
import WritingAssistantPage from './pages/WritingAssistantPage';
import MyProgressPage from './pages/MyProgressPage';
import SettingsPage from './pages/SettingsPage';

export default createRoutesFromElements(
  <Router>
    <Route element={<DashboardPage />} path="/" />
    <Route element={<ImageToolsPage />} path="/image-tools" />
    <Route element={<ResumeBuilderPage />} path="/resume-builder" />
    <Route element={<JobMatcherPage />} path="/job-matcher" />
    <Route element={<SkillAdvisorPage />} path="/skill-advisor" />
    <Route element={<SkillAssessmentPage />} path="/skill-assessment" />
    <Route element={<WritingAssistantPage />} path="/writing-assistant" />
    <Route element={<MyProgressPage />} path="/my-progress" />
    <Route element={<SettingsPage />} path="/settings" />
  </Router>
);