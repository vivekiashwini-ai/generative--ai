import React, { useState } from 'react';
import { Card, Separator, Input, Button, Select, Option, Progress, Alert } from './components';

const ResumeBuilderPage = () => {
  const sections = [
    'personal-details',
    'education', 
    'experience',
    'skills',
    'projects',
    'certifications'
  ];

  const [currentSection, setCurrentSection] = useState(sections[0]);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    summary: '',
    education: [],
    experience: [],
    skills: [],
    projects: [],
    certifications: []
  });

  const [isGenerating, setIsGenerating] = useState(false);
  const [previewVisible, setPreviewVisible] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const addSection = (sectionType) => {
    setFormData(prev => ({
      ...prev,
      [sectionType]: [...prev[sectionType], { id: Date.now(), value: '' }]
    }));
  };

  const removeSection = (sectionType, index) => {
    setFormData(prev => ({
      ...prev,
      [sectionType]: prev[sectionType].filter((_, i) => i !== index)
    }));
  };

  const generateResumeContent = async () => {
    setIsGenerating(true);
    
    // In a real implementation, this would call the LLM API
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    setIsGenerating(false);
    setPreviewVisible(true);
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">AI Resume Builder</h1>
      
      <Card className="mb-6">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Personal Details</h2>
        <Separator />
        
        <div className="grid grid-cols-2 gap-4">
          <Input 
            name="name" 
            placeholder="Full Name" 
            value={formData.name} 
            onChange={handleChange}
            className="w-full"
          />
          <Input 
            name="email" 
            type="email" 
            placeholder="Email" 
            value={formData.email} 
            onChange={handleChange}
            className="w-full"
          />
          <Input 
            name="phone" 
            type="tel" 
            placeholder="Phone" 
            value={formData.phone} 
            onChange={handleChange}
            className="w-full"
          />
        </div>
        
        <textarea 
          placeholder="Professional summary or career objective" 
          value={formData.summary} 
          onChange={handleChange}
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-700 dark:text-white mt-2"
        />
      </Card>

      {sections.map(section => (
        <Card key={section} className="mb-6">
          <h2 className="text-xl font-semibold text-gray-700 mb-4">{section.replace('-', ' ')}</h2>
          <Separator />
          
          {section === 'education' && (
            <div>
              <Button 
                onClick={() => addSection('education')}
                className="mb-3 w-full justify-end"
              >
                Add Education Entry
              </Button>
              {formData.education.map((edu, index) => (
                <div key={index} className="mb-3">
                  <Input 
                    name={`education[${index}].degree`}
                    placeholder="Degree" 
                    value={edu.degree || ''} 
                    onChange={handleChange}
                    className="w-full mb-2"
                  />
                  <Input 
                    name={`education[${index}].institution`}
                    placeholder="Institution" 
                    value={edu.institution || ''} 
                    onChange={handleChange}
                    className="w-full mb-2"
                  />
                  <Input 
                    name={`education[${index}].graduationYear`}
                    placeholder="Graduation Year" 
                    value={edu.graduationYear || ''} 
                    onChange={handleChange}
                    className="w-full"
                  />
                  <Button 
                    onClick={() => removeSection('education', index)}
                    className="mt-1 text-sm text-red-600"
                  >
                    Remove
                  </Button>
                </div>
              ))}
            </div>
          )}

          {section === 'experience' && (
            <div>
              <Button 
                onClick={() => addSection('experience')}
                className="mb-3 w-full justify-end"
              >
                Add Experience Entry
              </Button>
              {formData.experience.map((exp, index) => (
                <div key={index} className="mb-3">
                  <Input 
                    name={`experience[${index}].position`}
                    placeholder="Position" 
                    value={exp.position || ''} 
                    onChange={handleChange}
                    className="w-full mb-2"
                  />
                  <Input 
                    name={`experience[${index}].company`}
                    placeholder="Company" 
                    value={exp.company || ''} 
                    onChange={handleChange}
                    className="w-full mb-2"
                  />
                  <Input 
                    name={`experience[${index}].duration`}
                    placeholder="Duration" 
                    value={exp.duration || ''} 
                    onChange={handleChange}
                    className="w-full mb-2"
                  />
                  <textarea 
                    name={`experience[${index}].description`}
                    placeholder="Description of responsibilities and achievements" 
                    value={exp.description || ''} 
                    rows={2}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-700 dark:text-white mt-2"
                  />
                  <Button 
                    onClick={() => removeSection('experience', index)}
                    className="mt-1 text-sm text-red-600"
                  >
                    Remove
                  </Button>
                </div>
              ))}
            </div>
          )}

          {section === 'skills' && (
            <div>
              <Button 
                onClick={() => addSection('skills')}
                className="mb-3 w-full justify-end"
              >
                Add Skill
              </Button>
              {formData.skills.map((skill, index) => (
                <div key={index} className="mb-2">
                  <Input 
                    name={`skills[${index}].name`}
                    placeholder="Skill name" 
                    value={skill.name || ''} 
                    onChange={handleChange}
                    className="w-full mb-2"
                  />
                  <select 
                    name={`skills[${index}].level`}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-700 dark:text-white"
                  >
                    <option value="beginner">Beginner</option>
                    <option value="intermediate">Intermediate</option>
                    <option value="advanced">Advanced</option>
                  </select>
                </div>
              ))}
              <Button 
                onClick={() => removeSection('skills', formData.skills.length - 1)}
                className="mt-1 text-sm text-red-600"
              >
                Remove Last
              </Button>
            </div>
          )}

          {section === 'projects' && (
            <div>
              <Button 
                onClick={() => addSection('projects')}
                className="mb-3 w-full justify-end"
              >
                Add Project
              </Button>
              {formData.projects.map((project, index) => (
                <div key={index} className="mb-3">
                  <Input 
                    name={`projects[${index}].title`}
                    placeholder="Project Title" 
                    value={project.title || ''} 
                    onChange={handleChange}
                    className="w-full mb-2"
                  />
                  <Input 
                    name={`projects[${index}].description`}
                    placeholder="Project Description" 
                    value={project.description || ''} 
                    onChange={handleChange}
                    rows={2}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-700 dark:text-white mt-2"
                  />
                  <Input 
                    name={`projects[${index}].technologies`}
                    placeholder="Technologies used" 
                    value={project.technologies || ''} 
                    onChange={handleChange}
                    className="w-full mb-2"
                  />
                  <Button 
                    onClick={() => removeSection('projects', index)}
                    className="mt-1 text-sm text-red-600"
                  >
                    Remove
                  </Button>
                </div>
              ))}
              <Button 
                onClick={() => removeSection('projects', formData.projects.length - 1)}
                className="mt-1 text-sm text-red-600"
              >
                Remove Last
              </Button>
            </div>
          )}

          {section === 'certifications' && (
            <div>
              <Button 
                onClick={() => addSection('certifications')}
                className="mb-3 w-full justify-end"
              >
                Add Certification
              </Button>
              {formData.certifications.map((cert, index) => (
                <div key={index} className="mb-3">
                  <Input 
                    name={`certifications[${index}].name`}
                    placeholder="Certification Name" 
                    value={cert.name || ''} 
                    onChange={handleChange}
                    className="w-full mb-2"
                  />
                  <Input 
                    name={`certifications[${index}].issuer`}
                    placeholder="Issuing Organization" 
                    value={cert.issuer || ''} 
                    onChange={handleChange}
                    className="w-full mb-2"
                  />
                  <Input 
                    name={`certifications[${index}].date`}
                    placeholder="Date obtained" 
                    value={cert.date || ''} 
                    onChange={handleChange}
                    className="w-full"
                  />
                  <Button 
                    onClick={() => removeSection('certifications', index)}
                    className="mt-1 text-sm text-red-600"
                  >
                    Remove
                  </Button>
                </div>
              ))}
              <Button 
                onClick={() => removeSection('certifications', formData.certifications.length - 1)}
                className="mt-1 text-sm text-red-600"
              >
                Remove Last
              </Button>
            </div>
          )}
        </Card>
      ))}

      {/* Generate Content Section */}
      <Card>
        <h2 className="text-xl font-semibold text-gray-700 mb-4">AI Content Generation</h2>
        <Separator />
        
        <Button 
          onClick={generateResumeContent}
          disabled={isGenerating}
          className="w-full mb-4"
        >
          {isGenerating ? 'Generating...' : 'Generate Professional Content'}
        </Button>
        
        {isGenerating && <Progress className="my-4" />}
        
        {previewVisible && (
          <div className="mt-6 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
            <h3 className="text-bold text-gray-900 dark:text-gray-100 mb-4">Resume Preview</h3>
            <p className="text-gray-600 dark:text-gray-300">
              Your resume has been generated with the provided information. 
              Review and edit the content below before exporting.
            </p>
            {/* Preview content would go here */}
          </div>
        )}
      </Card>
    </div>
  );
};

export default ResumeBuilderPage;