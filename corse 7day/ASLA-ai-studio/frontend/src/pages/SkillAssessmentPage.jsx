import React, { useState } from 'react';
import { Card, Separator, Input, Button, Progress, Alert } from './components';

const SkillAssessmentPage = () => {
  const [selectedSkill, setSelectedSkill] = useState('');
  const [difficulty, setDifficulty] = useState('beginner');
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);
  const [score, setScore] = useState(null);

  const skills = [
    'Python', 'SQL', 'JavaScript', 'Excel', 'Machine Learning', 
    'Data Visualization', 'SEO', 'Content Creation', 'Figma'
  ];

  const questionBanks = {
    Python: {
      beginner: [
        {
          id: 1,
          question: "What is the correct way to define a function in Python?",
          options: ["def my_function():", "function my_function():", "def my_function(x):", "function my_function(x)"],
          answer: 0
        },
        {
          id: 2,
          question: "Which of the following is used to iterate over a range of numbers?",
          options: ["for i in range(5):", "for i from 0 to 5:", "for i in 5:", "for i = 0; i < 5; i++"],
          answer: 0
        }
      ],
      intermediate: [
        {
          id: 1,
          question: "What does the *args syntax do in a function?",
          options: ["Returns the argument count", "Passes a variable number of non-keyword arguments", "Passes a variable number of keyword arguments", "Unpacks a dictionary"],
          answer: 1
        }
      ],
      advanced: [
        {
          id: 1,
          question: "What is a decorator in Python?",
          options: ["A function that modifies another function's behavior", "A syntax error", "A type of loop", "A built-in module"],
          answer: 0
        }
      ]
    },
    SQL: {
      beginner: [
        {
          id: 1,
          question: "Which SQL clause is used to filter results?",
          options: ["SELECT", "FROM", "WHERE", "GROUP BY"],
          answer: 2
        }
      ],
      intermediate: [],
      advanced: []
    }
  };

  const startAssessment = () => {
    if (!selectedSkill) return;
    
    const bank = questionBanks[selectedSkill]?.[difficulty] || [];
    if (bank.length > 0) {
      setQuestions(bank);
      setCurrentQuestionIndex(0);
      setAnswers({});
      setShowResults(false);
      setScore(null);
    }
  };

  const submitAnswer = (questionId, selectedIndex) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: selectedIndex
    }));
  };

  const finishAssessment = () => {
    if (questions.length === 0) return;
    
    let correct = 0;
    questions.forEach((q, i) => {
      if (answers[i] === q.answer) correct++;
    });
    
    const percentage = Math.round((correct / questions.length) * 100);
    setScore(percentage);
    setShowResults(true);
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Skill Assessment</h1>
      
      {/* Skill and Difficulty Selection */}
      <Card className="mb-6">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Assessment Setup</h2>
        <Separator />
        
        <select 
          value={selectedSkill}
          onChange={(e) => setSelectedSkill(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-700 dark:text-white mb-4"
        >
          <option value="">Select a skill</option>
          {skills.map(skill => (
            <option key={skill} value={skill}>
              {skill}
            </option>
          ))}
        </select>
        
        <select 
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-700 dark:text-white mb-4"
        >
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>
        
        <Button onClick={startAssessment} disabled={!selectedSkill} className="w-full">
          Start Assessment
        </Button>
      </Card>

      {/* Questions Section */}
      {showResults && score !== null && (
        <Card>
          <h2 className="text-xl font-semibold text-gray-700 mb-4">Assessment Results</h2>
          <Separator />
          
          <p className="text-2xl font-bold {score >= 80 ? 'text-green-600' : score >= 60 ? 'text-yellow-600' : 'text-red-600'}">
            {score}%
          </p>
          
          <p className="text-gray-600 mt-2">
            {questions.length > 0 ? `You got {score}% correct` : 'No questions answered'}
          </p>
          
          <Button 
            onClick={() => setShowResults(false)}
            className="w-full mt-4"
          >
            Retake Assessment
          </Button>
        </Card>
      )}

      {questions.length > 0 && !showResults && (
        <Card>
          <h2 className="text-xl font-semibold text-gray-700 mb-4">
            {selectedSkill} {difficulty.charAt(0).toUpperCase() + difficulty.slice(1)} Assessment
          </h2>
          <Separator />
          
          <p className="text-gray-600 mb-4">
            Question {currentQuestionIndex + 1} of {questions.length}
          </p>
          
          {questions[currentQuestionIndex] && (
            <div>
              <p className="font-medium text-gray-900 mb-3">{questions[currentQuestionIndex].question}</p>
              
              {questions[currentQuestionIndex].options.map((option, i) => (
                <div key={i} className="mb-2">
                  <label className="flex items-center px-3 py-2 rounded border bg-gray-100 dark:bg-gray-800">
                    <input
                      type="radio"
                      name="question"
                      value={i}
                      checked={answers[currentQuestionIndex] === i}
                      onChange={() => submitAnswer(currentQuestionIndex, i)}
                      className="w-4 h-4 mr-2 focus:ring-primary-500"
                    />
                    {option}
                  </label>
                </div>
              ))}
              
              <div className="mt-4">
                {currentQuestionIndex < questions.length - 1 ? (
                  <Button 
                    onClick={() => setCurrentQuestionIndex(prev => prev + 1)}
                    className="w-full"
                  >
                    Next Question
                  </Button>
                ) : (
                  <Button 
                    onClick={finishAssessment}
                    className="w-full"
                  >
                    Submit Assessment
                  </Button>
                )}
              </div>
            </div>
          )}
        </Card>
      )}
    </div>
  );
};

export default SkillAssessmentPage;