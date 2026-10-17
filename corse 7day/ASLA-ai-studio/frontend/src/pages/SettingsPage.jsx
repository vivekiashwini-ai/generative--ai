import React from 'react';
import { Card, Separator } from './components';

const SettingsPage = () => {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Settings</h1>
      
      <Card>
        <h2 className="text-xl font-semibold text-gray-700 mb-4">API Configuration</h2>
        <Separator />
        <p className="text-gray-500 text-sm">
          Configure your AI API keys here. The application supports multiple LLM providers.
        </p>
      </Card>
      
      <Card className="mt-4">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Feature Settings</h2>
        <Separator />
        <p className="text-gray-500 text-sm">
          Enable or disable optional features like the Image Generator based on your preferences.
        </p>
      </Card>
      
      <Card className="mt-4">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Privacy & Data</h2>
        <Separator />
        <p className="text-gray-500 text-sm">
          Control your data privacy settings and manage stored information.
        </p>
      </Card>
    </div>
  );
};

export default SettingsPage;