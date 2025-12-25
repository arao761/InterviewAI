'use client';

import { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Upload, FileText, Check, ArrowLeft } from 'lucide-react';

export default function ResumeUploadSection({ onBack }: { onBack: () => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  return (
    <section className="min-h-screen flex flex-col px-4 sm:px-6 lg:px-8 py-20">
      <div className="mb-8">
        <Button
          onClick={onBack}
          variant="outline"
          className="flex items-center gap-2 border-border hover:bg-card"
        >
          <ArrowLeft className="w-4 h-4" />
          Back
        </Button>
      </div>

      {/* Main content container */}
      <div className="flex-1 flex items-center justify-center">
        <div className="w-full max-w-2xl">
          <div className="mb-12 text-center">
            <h1 className="text-4xl sm:text-5xl font-bold mb-4">Upload Your Resume</h1>
            <p className="text-lg text-muted-foreground">
              Start your interview preparation by uploading your resume. We'll analyze it to provide personalized questions.
            </p>
          </div>

          <Card className="bg-card border-border p-12">
            <form
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              className="space-y-6"
            > 
              <div
                className={`relative border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
                  dragActive ? 'border-primary bg-primary/5' : 'border-border'
                } ${file ? 'bg-primary/5' : 'hover:bg-card/50'}`}
              >
                <input
                  type="file"
                  onChange={handleChange}
                  accept=".pdf,.doc,.docx"
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  id="file-upload"
                />

                <div className="flex flex-col items-center gap-4">
                  {file ? (
                    <>
                      <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center">
                        <Check className="w-8 h-8 text-primary" />
                      </div>
                      <div>
                        <p className="font-semibold text-foreground">{file.name}</p>
                        <p className="text-sm text-muted-foreground">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                      </div>
                    </>
                  ) : (
                    <>
                      <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center">
                        <Upload className="w-8 h-8 text-primary" />
                      </div>
                      <div>
                        <p className="font-semibold text-foreground">Drag and drop your resume here</p>
                        <p className="text-sm text-muted-foreground">or click to browse</p>
                      </div>
                      <p className="text-xs text-muted-foreground">Supported formats: PDF, DOC, DOCX</p>
                    </>
                  )}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <Button
                  type="button"
                  variant="outline"
                  className="border-border hover:bg-card"
                  onClick={() => setFile(null)}
                  disabled={!file}
                >
                  Clear
                </Button>
                <Button
                  type="submit"
                  disabled={!file}
                  className="bg-primary text-primary-foreground hover:bg-primary/90"
                >
                  Continue
                </Button>
              </div>
            </form>
          </Card>

          {/* Info cards */}
          <div className="grid sm:grid-cols-3 gap-4 mt-12">
            {[
              { title: 'Fast Analysis', description: 'AI analyzes your resume instantly' },
              { title: 'Personalized Questions', description: 'Get interview questions tailored to your experience' },
              { title: 'Privacy First', description: 'Your data is secure and encrypted' },
            ].map((info, i) => (
              <Card key={i} className="bg-card border-border p-4 text-center">
                <h3 className="font-semibold text-foreground mb-2">{info.title}</h3>
                <p className="text-sm text-muted-foreground">{info.description}</p>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
