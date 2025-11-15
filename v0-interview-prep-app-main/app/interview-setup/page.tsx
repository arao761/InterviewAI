'use client';

import { useState } from 'react';
import Link from 'next/link';
import InterviewTypeSelector from '@/components/interview-setup/interview-type-selector';
import JobDetailsForm from '@/components/interview-setup/job-details-form';
import DifficultySelector from '@/components/interview-setup/difficulty-selector';
import InterviewSettingsForm from '@/components/interview-setup/interview-settings-form';
import SetupProgressBar from '@/components/interview-setup/setup-progress-bar';
import { Button } from '@/components/ui/button';
import { ArrowLeft, ArrowRight } from 'lucide-react';

type SetupStep = 'interview-type' | 'job-details' | 'difficulty' | 'settings';

export default function InterviewSetup() {
  const [currentStep, setCurrentStep] = useState<SetupStep>('interview-type');
  const [formData, setFormData] = useState({
    interviewType: '',
    jobTitle: '',
    company: '',
    industry: '',
    yearsOfExperience: '',
    difficulty: '',
    duration: '30',
    numberOfQuestions: '5',
    focusAreas: [] as string[],
  });

  const steps: SetupStep[] = ['interview-type', 'job-details', 'difficulty', 'settings'];
  const currentStepIndex = steps.indexOf(currentStep);
  const progress = ((currentStepIndex + 1) / steps.length) * 100;

  const handleNext = () => {
    if (currentStepIndex < steps.length - 1) {
      setCurrentStep(steps[currentStepIndex + 1]);
    } else {
      // Start interview
      console.log('Starting interview with:', formData);
    }
  };

  const handleBack = () => {
    if (currentStepIndex > 0) {
      setCurrentStep(steps[currentStepIndex - 1]);
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="border-b border-border py-4 px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
            <span className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
              InterviewAI
            </span>
          </Link>
        </div>
      </div>

      <div className="py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto">
          {/* Header */}
          <div className="mb-12">
            <h1 className="text-4xl font-bold mb-2">Setup Your Interview</h1>
            <p className="text-muted-foreground">
              Customize your interview experience with personalized settings
            </p>
          </div>

          {/* Progress Bar */}
          <SetupProgressBar currentStep={currentStepIndex + 1} totalSteps={steps.length} progress={progress} />

          {/* Step Content */}
          <div className="bg-card border border-border rounded-lg p-8 my-12">
            {currentStep === 'interview-type' && (
              <InterviewTypeSelector
                value={formData.interviewType}
                onChange={(type) => setFormData({ ...formData, interviewType: type })}
              />
            )}

            {currentStep === 'job-details' && (
              <JobDetailsForm
                data={{
                  jobTitle: formData.jobTitle,
                  company: formData.company,
                  industry: formData.industry,
                  yearsOfExperience: formData.yearsOfExperience,
                }}
                onChange={(updates) => setFormData({ ...formData, ...updates })}
              />
            )}

            {currentStep === 'difficulty' && (
              <DifficultySelector
                value={formData.difficulty}
                onChange={(difficulty) => setFormData({ ...formData, difficulty })}
              />
            )}

            {currentStep === 'settings' && (
              <InterviewSettingsForm
                data={{
                  duration: formData.duration,
                  numberOfQuestions: formData.numberOfQuestions,
                  focusAreas: formData.focusAreas,
                }}
                onChange={(updates) => setFormData({ ...formData, ...updates })}
              />
            )}
          </div>

          {/* Navigation Buttons */}
          <div className="flex justify-between items-center">
            <Button
              variant="outline"
              onClick={handleBack}
              disabled={currentStepIndex === 0}
              className="border-border hover:bg-card disabled:opacity-50"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back
            </Button>

            <div className="text-sm text-muted-foreground">
              Step {currentStepIndex + 1} of {steps.length}
            </div>

            <Button
              onClick={handleNext}
              className="bg-primary text-primary-foreground hover:bg-primary/90"
            >
              {currentStepIndex === steps.length - 1 ? 'Start Interview' : 'Next'}
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
