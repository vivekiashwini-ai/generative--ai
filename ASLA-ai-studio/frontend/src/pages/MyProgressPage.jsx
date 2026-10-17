import React from 'react';
import { Card, Separator } from './components';

const MyProgressPage = () => {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">My Progress</h1>
      
      <Card>
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Assessment History</h2>
        <Separator />
        <p className="text-gray-500 text-sm">No assessments taken yet. Start with the Skill Assessment page to begin tracking your progress.</p>
      </Card>
      
      <Card className="mt-4">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Skills Developed</h2>
        <Separator />
        <p className="text-gray-500 text-sm">Track your learning journey here.</p>
      </Card>
      
      <Card className="mt-4">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Learning Roadmap Progress</h2>
        <Separator />
        <p className="text-gray-500 text-sm">Monitor your progress through recommended learning paths.</p>
      </Card>
      
      <Card className="mt-4">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Saved Items</h2>
        <Separator />
        <p className="text-gray-500 text-sm">Saved resumes and jobs will appear here.</p>
      </Card>
    </div>
  );
};

export default MyProgressPage;