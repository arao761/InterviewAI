'use client';

import { useState, useCallback } from 'react';
import { Upload, FileText, CheckCircle, XCircle, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { apiClient } from '@/lib/api/client';
import type { ParsedResume } from '@/lib/api/types';

interface ResumeUploaderProps {
  onResumeUploaded?: (resumeData: ParsedResume) => void;
}

export default function ResumeUploader({ onResumeUploaded }: ResumeUploaderProps) {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [error, setError] = useState<string>('');
  const [resumeData, setResumeData] = useState<ParsedResume | null>(null);

  const handleFileChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      // Validate file type
      const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
      if (!validTypes.includes(selectedFile.type) && !selectedFile.name.match(/\.(pdf|docx)$/i)) {
        setError('Please upload a PDF or DOCX file');
        setUploadStatus('error');
        return;
      }

      // Validate file size (10MB max)
      if (selectedFile.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB');
        setUploadStatus('error');
        return;
      }

      setFile(selectedFile);
      setUploadStatus('idle');
      setError('');
    }
  }, []);

  const handleUpload = useCallback(async () => {
    if (!file) return;

    setUploading(true);
    setError('');

    try {
      console.log('📤 Uploading resume:', file.name);
      const response = await apiClient.parseResume(file);
      console.log('📥 Parse response:', response);

      if (response.success && 'data' in response) {
        console.log('✅ Resume parsed successfully');
        setUploadStatus('success');
        setResumeData(response.data);
        // Pass the parsed data to parent
        onResumeUploaded?.(response.data);
      } else {
        console.error('❌ Parse failed:', response);
        setUploadStatus('error');
        setError('error' in response ? response.error : 'Failed to parse resume');
      }
    } catch (err) {
      console.error('❌ Upload error:', err);
      setUploadStatus('error');
      setError(err instanceof Error ? err.message : 'Failed to upload resume');
    } finally {
      setUploading(false);
    }
  }, [file, onResumeUploaded]);

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      const event = {
        target: { files: [droppedFile] },
      } as any;
      handleFileChange(event);
    }
  }, [handleFileChange]);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  }, []);

  return (
    <div className="space-y-4">
      <div className="space-y-2">
        <h3 className="text-lg font-semibold">Upload Your Resume</h3>
        <p className="text-sm text-muted-foreground">
          Upload your resume to get personalized interview questions
        </p>
      </div>

      {/* Drop Zone */}
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center transition-colors
          ${file ? 'border-primary bg-primary/5' : 'border-border hover:border-primary/50'}
          ${uploadStatus === 'error' ? 'border-red-500 bg-red-50 dark:bg-red-950' : ''}
          ${uploadStatus === 'success' ? 'border-green-500 bg-green-50 dark:bg-green-950' : ''}
        `}
      >
        <input
          type="file"
          id="resume-upload"
          accept=".pdf,.docx"
          onChange={handleFileChange}
          className="hidden"
          disabled={uploading}
        />

        <label
          htmlFor="resume-upload"
          className="flex flex-col items-center gap-4 cursor-pointer"
        >
          {uploadStatus === 'idle' && !file && (
            <>
              <Upload className="w-12 h-12 text-muted-foreground" />
              <div>
                <p className="font-medium">Click to upload or drag and drop</p>
                <p className="text-sm text-muted-foreground">PDF or DOCX (max 10MB)</p>
              </div>
            </>
          )}

          {file && uploadStatus === 'idle' && (
            <>
              <FileText className="w-12 h-12 text-primary" />
              <div>
                <p className="font-medium">{file.name}</p>
                <p className="text-sm text-muted-foreground">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </>
          )}

          {uploadStatus === 'success' && (
            <>
              <CheckCircle className="w-12 h-12 text-green-500" />
              <div>
                <p className="font-medium text-green-700 dark:text-green-400">
                  Resume uploaded successfully!
                </p>
                <p className="text-sm text-muted-foreground">{file?.name}</p>
              </div>
            </>
          )}

          {uploadStatus === 'error' && (
            <>
              <XCircle className="w-12 h-12 text-red-500" />
              <div>
                <p className="font-medium text-red-700 dark:text-red-400">Upload failed</p>
                <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
              </div>
            </>
          )}
        </label>
      </div>

      {/* Upload Button */}
      {file && uploadStatus !== 'success' && (
        <Button
          onClick={handleUpload}
          disabled={uploading}
          className="w-full"
        >
          {uploading ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              Parsing Resume...
            </>
          ) : (
            <>
              <Upload className="w-4 h-4 mr-2" />
              Upload and Parse Resume
            </>
          )}
        </Button>
      )}

      {/* Resume Preview */}
      {resumeData && uploadStatus === 'success' && (
        <div className="border rounded-lg p-4 bg-card space-y-3">
          <h4 className="font-semibold">Parsed Information:</h4>
          <div className="space-y-2 text-sm">
            {resumeData.name && (
              <p><strong>Name:</strong> {resumeData.name}</p>
            )}
            {resumeData.email && (
              <p><strong>Email:</strong> {resumeData.email}</p>
            )}
            {resumeData.skills && (() => {
              const skillsArray = Array.isArray(resumeData.skills)
                ? resumeData.skills
                : [
                    ...(resumeData.skills.technical || []),
                    ...(resumeData.skills.soft || []),
                    ...(resumeData.skills.tools || []),
                    ...(resumeData.skills.languages || [])
                  ];

              return skillsArray.length > 0 && (
                <div>
                  <strong>Skills:</strong>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {skillsArray.slice(0, 10).map((skill, i) => (
                      <span
                        key={i}
                        className="px-2 py-1 bg-primary/10 text-primary rounded text-xs"
                      >
                        {skill}
                      </span>
                    ))}
                    {skillsArray.length > 10 && (
                      <span className="px-2 py-1 bg-muted rounded text-xs">
                        +{skillsArray.length - 10} more
                      </span>
                    )}
                  </div>
                </div>
              );
            })()}
          </div>
        </div>
      )}
    </div>
  );
}
