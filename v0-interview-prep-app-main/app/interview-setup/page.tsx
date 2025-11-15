'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import InterviewTypeSelector from '@/components/interview-setup/interview-type-selector';
import JobDetailsForm from '@/components/interview-setup/job-details-form';
import DifficultySelector from '@/components/interview-setup/difficulty-selector';
import InterviewSettingsForm from '@/components/interview-setup/interview-settings-form';
import SetupProgressBar from '@/components/interview-setup/setup-progress-bar';
import ResumeUploader from '@/components/resume-upload/resume-uploader';
import { Button } from '@/components/ui/button';
import { ArrowLeft, ArrowRight, Loader2 } from 'lucide-react';
import { apiClient } from '@/lib/api/client';
import type { ParsedResume, InterviewQuestion, InterviewType } from '@/lib/api/types';

type SetupStep = 'resume' | 'interview-type' | 'job-details' | 'difficulty' | 'settings';

export default function InterviewSetup() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState<SetupStep>('resume');
  const [isGenerating, setIsGenerating] = useState(false);
  const [resumeData, setResumeData] = useState<ParsedResume | null>(null);
  const [formData, setFormData] = useState({
    interviewType: '' as InterviewType | '',
    jobTitle: '',
    company: '',
    industry: '',
    yearsOfExperience: '',
    difficulty: '',
    duration: '30',
    numberOfQuestions: '5',
    focusAreas: [] as string[],
  });

  const steps: SetupStep[] = ['resume', 'interview-type', 'job-details', 'difficulty', 'settings'];
  const currentStepIndex = steps.indexOf(currentStep);
  const progress = ((currentStepIndex + 1) / steps.length) * 100;

  const handleResumeUploaded = (data: ParsedResume) => {
    setResumeData(data);
    // Auto-fill job details from resume if available
    if (data.experience && data.experience.length > 0) {
      setFormData(prev => ({
        ...prev,
        jobTitle: data.experience[0].title || prev.jobTitle,
        company: data.experience[0].company || prev.company,
      }));
    }
  };

  const handleStartInterview = async () => {
    setIsGenerating(true);
    try {
      // Prepare resume data - convert to plain object if needed
      let resumeForAPI: any = {
        name: formData.jobTitle || 'Candidate',
        skills: [],
        experience: [],
        education: [],
      };

      // If we have resume data, use it
      if (resumeData) {
        // Make sure nested objects are serializable
        resumeForAPI = JSON.parse(JSON.stringify(resumeData));
      }

      console.log('Resume data being sent:', resumeForAPI);

      // Generate questions from backend
      const response = await apiClient.generateQuestions({
        resume_data: resumeForAPI,
        interview_type: (formData.interviewType || 'both') as InterviewType,
        num_questions: parseInt(formData.numberOfQuestions) || 5,
      });

      if (response.success && 'questions' in response) {
        // Store interview data in sessionStorage
        const interviewSession = {
          questions: response.questions,
          formData,
          resumeData,
          startTime: new Date().toISOString(),
        };
        sessionStorage.setItem('interviewSession', JSON.stringify(interviewSession));

        // Navigate to interview page
        router.push('/interview');
      } else {
        console.error('Failed to generate questions:', response);
        alert('Failed to generate questions. Please try again.');
      }
    } catch (error) {
      console.error('Error starting interview:', error);
      alert('An error occurred. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleNext = () => {
    if (currentStepIndex < steps.length - 1) {
      setCurrentStep(steps[currentStepIndex + 1]);
    } else {
      handleStartInterview();
    }
  };

  const handleBack = () => {
    if (currentStepIndex > 0) {
      setCurrentStep(steps[currentStepIndex - 1]);
    }
  };

  const canProceed = () => {
    switch (currentStep) {
      case 'resume':
        return true; // Resume is optional
      case 'interview-type':
        return formData.interviewType !== '';
      case 'job-details':
        return formData.jobTitle !== '';
      case 'difficulty':
        return formData.difficulty !== '';
      case 'settings':
        return true;
      default:
        return false;
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="border-b border-border py-4 px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
            <span className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
              PrepWise AI
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
              Customize your interview experience with AI-powered personalization
            </p>
          </div>

          {/* Progress Bar */}
          <SetupProgressBar currentStep={currentStepIndex + 1} totalSteps={steps.length} progress={progress} />

          {/* Step Content */}
          <div className="bg-card border border-border rounded-lg p-8 my-12">
            {currentStep === 'resume' && (
              <div>
                <ResumeUploader onResumeUploaded={handleResumeUploaded} />
                <p className="text-sm text-muted-foreground mt-4 text-center">
                  Skip this step if you don't have a resume ready
                </p>
              </div>
            )}

            {currentStep === 'interview-type' && (
              <InterviewTypeSelector
                value={formData.interviewType}
                onChange={(type) => setFormData({ ...formData, interviewType: type as InterviewType })}
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
              disabled={currentStepIndex === 0 || isGenerating}
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
              disabled={!canProceed() || isGenerating}
              className="bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-50"
            >
              {isGenerating ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Generating Questions...
                </>
              ) : (
                <>
                  {currentStepIndex === steps.length - 1 ? 'Start Interview' : 'Next'}
                  <ArrowRight className="w-4 h-4 ml-2" />
                </>
              )}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
