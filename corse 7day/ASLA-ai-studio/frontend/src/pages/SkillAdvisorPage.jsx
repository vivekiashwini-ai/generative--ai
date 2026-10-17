import React, { useState } from 'react';
import { Card, Separator, Input, Button, Select, Option, Progress, Alert } from './components';

const SkillAdvisorPage = () => {
  const [desiredJob, setDesiredJob] = useState('');
  const [userSkills, setUserSkills] = useState([]);
  const [skillGaps, setSkillGaps] = useState([]);
  const [learningRoadmap, setLearningRoadmap] = useState([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const addUserSkill = () => {
    setUserSkills(prev => [...prev, { id: Date.now(), name: '', level: 'intermediate' }]);
  };

  const removeUserSkill = (index) => {
    setUserSkills(prev => prev.filter((_, i) => i !== index));
  };

  const skillChangeHandler = (e) => {
    const { name, value } = e.target;
    setUserSkills(prev => 
      prev.map(skill => skill.name === name ? { ...skill, level: value } : skill)
    );
  };

  analyzeSkills = async () => {
    if (!desiredJob || !userSkills.length) return;
    
    setIsAnalyzing(true);
    
    // In a real implementation, this would call the backend with job descriptions
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Mock skill gap analysis
    const allSkills = {
      'Data Analyst': ['Python', 'SQL', 'Excel', 'Data Visualization', 'Statistics'],
      'Software Developer': ['JavaScript', 'Python', 'Git', 'SQL', 'Data Structures'],
      'Product Manager': ['Product Strategy', 'Data Analysis', 'Communication', 'Analytics'],
      'Marketing Specialist': ['SEO', 'Content Creation', 'Analytics', 'Social Media'],
      'Graphic Designer': ['Adobe Creative Suite', 'Typography', 'Color Theory', 'Figma']
    };
    
    const targetSkills = allSkills[desiredJob] || [];
    const userSkillNames = userSkills.map(s => s.name).filter(Boolean);
    
    const gaps = targetSkills.filter(skill => !userSkillNames.includes(skill));
    
    const roadmap = gaps.map(skill => ({
      skill,
      resources: [
        { title: `Learn ${skill}`, type: 'course', url: '#' },
        { title: `Practice ${skill}`, type: 'project', url: '#' }
      ]
    }));
    
    setSkillGaps(gaps);
    setLearningRoadmap(roadmap);
    setIsAnalyzing(false);
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Skill Advisor</h1>
      
      {/* Desired Job Selection */}
      <Card className="mb-6">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Desired Job Role</h2>
        <Separator />
        
        <Input 
          placeholder="Enter job title (e.g., Data Analyst)" 
          value={desiredJob} 
          onChange={(e) => setDesiredJob(e.target.value)}
          className="w-full mb-4"
        />
        
        <Button onClick={analyzeSkills} disabled={isAnalyzing} className="w-full">
          {isAnalyzing ? 'Analyzing...' : 'Identify Skill Gaps'}
        </Button>
        
        {isAnalyzing && <Progress className="my-4" />}
      </Card>

      {/* User Skills Section */}
      <Card className="mb-6">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Your Current Skills</h2>
        <Separator />
        
        <div className="mb-4">
          <Button onClick={addUserSkill} className="mb-2">
            Add Skill
          </Button>
          
          {userSkills.map((skill, index) => (
            <div key={index} className="mb-2">
              <select 
                name={`skill[${index}].name`}
                value={skill.name || ''}
                onChange={(e) => skillChangeHandler(e)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-700 dark:text-white mb-1"
              >
                <option value="">Select a skill</option>
                <option value="Python">Python</option>
                <option value="SQL">SQL</option>
                <option value="JavaScript">JavaScript</option>
                <option value="Excel">Excel</option>
                <option value="Machine Learning">Machine Learning</option>
                <option value="Data Visualization">Data Visualization</option>
                <option value="SEO">SEO</option>
                <option value="Content Creation">Content Creation</option>
                <option value="Adobe Creative Suite">Adobe Creative Suite</option>
                <option value="Figma">Figma</option>
              </select>
              <select 
                name={`skill[${index}].level`}
                value={skill.level || 'intermediate'}
                onChange={(e) => skillChangeHandler(e)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-700 dark:text-white"
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
              <Button 
                onClick={() => removeUserSkill(index)}
                className="mt-1 text-sm text-red-600"
              >
                Remove
              </Button>
            </div>
          ))}
        </div>
      </Card>

      {/* Skill Gaps Section */}
      {skillGaps.length > 0 && (
        <Card>
          <h2 className="text-xl font-semibold text-gray-700 mb-4">Skill Gaps for {desiredJob}</h2>
          <Separator />
          
          <p className="text-gray-600 mb-4">
            The following skills are commonly required for {desiredJob} roles but 
            not currently in your skill set:
          </p>
          
          <ul className="space-y-2">
            {skillGaps.map((gap, index) => (
              <li key={index} className="p-3 rounded-lg border-l border-primary-500 bg-primary-50 dark:bg-primary-900/50">
                <span className="font-medium text-gray-900 dark:text-gray-100">{gap}</span>
                <span className="text-xs text-gray-500 ml-auto">Add this skill to your profile</span>
              </li>
            ))}
          </ul>
        </Card>
      )}

      {/* Learning Roadmap */}
      {learningRoadmap.length > 0 && (
        <Card>
          <h2 className="text-xl font-semibold text-gray-700 mb-4">Personalized Learning Roadmap</h2>
          <Separator />
          
          <p className="text-gray-600 mb-4">
            Based on your skill gaps, here's a structured learning path:
          </p>
          
          <ul className="space-y-4">
            {learningRoadmap.map((stage, index) => (
              <li key={index} className="p-4 rounded-lg border bg-gray-50 dark:bg-gray-800">
                <h3 className="font-medium text-gray-900 dark:text-gray-100 mb-2">
                  {stage.skill} - Beginner to Intermediate
                </h3>
                <ul className="list-disc pl-5 space-y-1 text-sm text-gray-600 dark:text-gray-300">
                  {stage.resources.map((resource, i) => (
                    <li key={i}>
                      <a href={resource.url} target="_blank" rel="noopener noreferrer">
                        {resource.title} ({resource.type})
                      </a>
                    </li>
                  ))}
                </ul>
              </li>
            ))}
          </ul>
        </Card>
      )}
    </div>
  );
};

export default SkillAdvisorPage;