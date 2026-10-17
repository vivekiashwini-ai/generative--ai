import React, { useState } from 'react';
import { Card, Separator, Textarea, Select, Option, Button, Progress } from './components';

const WritingAssistantPage = () => {
  const [task, setTask] = useState('improve');
  const [tone, setTone] = useState('professional');
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const tasks = [
    { value: 'improve', label: 'Improve Grammar and Clarity' },
    { value: 'rewrite', label: 'Rewrite in Different Tone' },
    { value: 'summarize', label: 'Summarize Long Text' },
    { value: 'email', label: 'Generate Professional Email' },
    { value: 'bio', label: 'Create Biography' },
    { value: 'resume', label: 'Improve Resume Summary' }
  ];

  const tones = [
    { value: 'professional', label: 'Professional' },
    { value: 'friendly', label: 'Friendly' },
    { value: 'formal', label: 'Formal' },
    { value: 'concise', label: 'Concise' },
    { value: 'persuasive', label: 'Persuasive' }
  ];

  const generateContent = async () => {
    if (!inputText.trim()) return;
    
    setIsGenerating(true);
    
    // In a real implementation, this would call the LLM API
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Mock generated content based on task and tone
    let generated = '';
    
    switch (task) {
      case 'improve':
        generated = inputText.split('.').filter(s => s.trim()).map(s => s.trim().charAt(0).toUpperCase() + s.trim().slice(1) + '.').join(' ');
        break;
      case 'rewrite':
        generated = inputText + ' (rewritten in ' + tone + ' tone)';
        break;
      case 'summarize':
        generated = inputText.split('.').slice(0, 2).map(s => s.trim()).join('. ') + '.';
        break;
      case 'email':
        generated = `Subject: Follow-up\n\nDear recipient,\n\n${inputText}\n\nBest regards,\nASLA AI Studio`;
        break;
      case 'bio':
        generated = `Professional biography for ${inputText || 'the user'}. Expert with extensive experience in their field.`;
        break;
      case 'resume':
        generated = `Professional Summary: ${inputText || 'Results-driven professional with expertise in various domains.'}`;
        break;
    }
    
    setOutputText(generated);
    setIsGenerating(false);
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">AI Writing Assistant</h1>
      
      {/* Task and Tone Selection */}
      <Card className="mb-6">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Writing Task</h2>
        <Separator />
        
        <select 
          value={task}
          onChange={(e) => setTask(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-700 dark:text-white mb-4"
        >
          {tasks.map(t => (
            <option key={t.value} value={t.value}>
              {t.label}
            </option>
          ))}
        </select>
        
        <select 
          value={tone}
          onChange={(e) => setTone(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-700 dark:text-white mb-4"
        >
          {tones.map(t => (
            <option key={t.value} value={t.value}>
              {t.label}
            </option>
          ))}
        </select>
      </Card>

      {/* Text Input */}
      <Card className="mb-6">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Your Text</h2>
        <Separator />
        
        <textarea 
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          rows={4}
          placeholder="Enter text to process..."
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-700 dark:text-white resize-none"
        />
      </Card>

      {/* Generate Button */}
      <Card>
        <Button 
          onClick={generateContent}
          disabled={isGenerating}
          className="w-full mb-4"
        >
          {isGenerating ? 'Generating...' : 'Generate Content'}
        </Button>
        
        {isGenerating && <Progress className="my-4" />}
      </Card>

      {/* Output Section */}
      {outputText && (
        <Card>
          <h2 className="text-xl font-semibold text-gray-700 mb-4">Generated Content</h2>
          <Separator />
          
          <textarea 
            value={outputText}
            rows={4}
            readOnly
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-700 dark:text-white resize-none mt-2"
          />
          
          <div className="mt-4 flex justify-between">
            <Button 
              onClick={() => navigator.clipboard.writeText(outputText)}
              className="text-sm text-primary-600 dark:text-primary-400"
            >
              Copy to Clipboard
            </Button>
          </div>
        </Card>
      )}
    </div>
  );
};

export default WritingAssistantPage;