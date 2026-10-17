import React, { useState } from 'react';
import { Card, Separator, Input, Button, Select, Option, Progress, Alert } from './components';

const JobMatcherPage = () => {
  const [userSkills, setUserSkills] = useState([]);
  const [userPreferences, setUserPreferences] = useState({
    desiredRole: '',
    location: '',
    experienceLevel: '',
  });
  const [jobRecommendations, setJobRecommendations] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const addSkill = () => {
    setUserSkills(prev => [...prev, { id: Date.now(), name: '', level: 'intermediate' }]);
  };

  const removeSkill = (index) => {
    setUserSkills(prev => prev.filter((_, i) => i !== index));
  };

  const handleSkillChange = (e) => {
    const { name, value } = e.target;
    setUserSkills(prev => 
      prev.map(skill => skill.name === name ? { ...skill, level: value } : skill)
    );
  };

  const recommendJobs = async () => {
    if (!userSkills.length || !userPreferences.desiredRole) return;
    
    setIsLoading(true);
    
    // In a real implementation, this would call the backend API
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const mockJobs = [
      {
        id: 1,
        title: 'Data Analyst',
        company: 'TechCorp Industries',
        location: 'Remote',
        experience: '2-4 years',
        matchPercentage: 85,
        matchReasons: ['Strong analytical skills', 'SQL experience matches requirements', 'Data visualization background'],
        applyLink: '#'
      },
      {
        id: 2,
        title: 'Business Intelligence Analyst',
        company: 'DataInsights Ltd.',
        location: 'New York, NY',
        experience: '3-5 years',
        matchPercentage: 78,
        matchReasons: ['BI tool experience', 'SQL proficiency', 'Analytics background'],
        applyLink: '#'
      },
      {
        id: 3,
        title: 'Junior Data Scientist',
        company: 'AI Studios',
        location: 'San Francisco, CA',
        experience: '1-3 years',
        matchPercentage: 65,
        matchReasons: ['Python knowledge', 'Basic ML understanding', 'Project experience'],
        applyLink: '#'
      }
    ];
    
    setJobRecommendations(mockJobs);
    setIsLoading(false);
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Job Matcher</h1>
      
      {/* User Skills Section */}
      <Card className="mb-6">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Your Skills</h2>
        <Separator />
        
        <div className="mb-4">
          <Button onClick={addSkill} className="mb-2">
            Add Skill
          </Button>
          
          {userSkills.map((skill, index) => (
            <div key={index} className="mb-2">
              <select 
                name={`skill[${index}].name`}
                value={skill.name || ''}
                onChange={(e) => handleSkillChange(e)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-700 dark:text-white mb-1"
              >
                <option value="">Select a skill</option>
                <option value="Python">Python</option>
                <option value="SQL">SQL</option>
                <option value="JavaScript">JavaScript</option>
                <option value="Excel">Excel</option>
                <option value="Machine Learning">Machine Learning</option>
                <option value="Data Visualization">Data Visualization</option>
              </select>
              <select 
                name={`skill[${index}].level`}
                value={skill.level || 'intermediate'}
                onChange={(e) => handleSkillChange(e)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-700 dark:text-white"
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>
          ))}
        </div>
      </Card>

      {/* Preferences Section */}
      <Card className="mb-6">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Preferences</h2>
        <Separator />
        
        <div className="grid grid-cols-2 gap-4">
          <Input 
            placeholder="Desired role (e.g., Data Analyst)" 
            value={userPreferences.desiredRole} 
            onChange={(e) => setUserPreferences(prev => ({ ...prev, desiredRole: e.target.value }))}
            className="w-full"
          />
          <Input 
            placeholder="Location" 
            value={userPreferences.location} 
            onChange={(e) => setUserPreferences(prev => ({ ...prev, location: e.target.value }))}
            className="w-full"
          />
          <select 
            value={userPreferences.experienceLevel}
            onChange={(e) => setUserPreferences(prev => ({ ...prev, experienceLevel: e.target.value }))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-700 dark:text-white"
          >
            <option value="">Any</option>
            <option value="entry">Entry Level</option>
            <option value="mid">Mid Level</option>
            <option value="senior">Senior Level</option>
          </select>
        </div>
      </Card>

      {/* Job Recommendations */}
      <Card>
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Job Recommendations</h2>
        <Separator />
        
        {isLoading && <Progress className="my-4" />}
        
        {jobRecommendations.length === 0 && (
          <p className="text-gray-500">Enter your skills and desired role above to get recommendations</p>
        )}
        
        {jobRecommendations.map((job) => (
          <div key={job.id} className="p-4 rounded-lg border border-gray-200 dark:border-gray-700 mb-3">
            <h3 className="text-bold text-gray-900 dark:text-gray-100 mb-2">{job.title}</h3>
            <p className="text-sm text-gray-600 dark:text-gray-300 mb-1">{job.company}</p>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">{job.location} • {job.experience}</p>
            <p className="text-sm font-medium text-primary-600 dark:text-primary-400 mb-2">
              Match: {job.matchPercentage}%
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              {job.matchReasons.map((reason, i) => (
                <React.Fragment key={i}>
                  • {reason}
                </React.Fragment>
              ))}
            </p>
            <a 
              href={job.applyLink}
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary-600 dark:text-primary-400 underline cursor-pointer"
            >
              Apply Now
            </a>
          </div>
        ))}
      </Card>
    </div>
  );
};

export default JobMatcherPage;