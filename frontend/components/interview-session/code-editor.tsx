'use client';

import { useState } from 'react';
import Editor from '@monaco-editor/react';
import { Button } from '@/components/ui/button';
import { RotateCcw } from 'lucide-react';

const LANGUAGES = [
  { id: 'javascript', name: 'JavaScript' },
  { id: 'typescript', name: 'TypeScript' },
  { id: 'python', name: 'Python' },
  { id: 'java', name: 'Java' },
  { id: 'cpp', name: 'C++' },
  { id: 'c', name: 'C' },
  { id: 'go', name: 'Go' },
  { id: 'rust', name: 'Rust' },
];

const DEFAULT_CODE: Record<string, string> = {
  javascript: '// Write your solution here\nfunction solution() {\n  \n}\n',
  typescript: '// Write your solution here\nfunction solution(): void {\n  \n}\n',
  python: '# Write your solution here\ndef solution():\n    pass\n',
  java: '// Write your solution here\npublic class Solution {\n    public static void main(String[] args) {\n        \n    }\n}\n',
  cpp: '// Write your solution here\n#include <iostream>\nusing namespace std;\n\nint main() {\n    \n    return 0;\n}\n',
  c: '// Write your solution here\n#include <stdio.h>\n\nint main() {\n    \n    return 0;\n}\n',
  go: '// Write your solution here\npackage main\n\nimport "fmt"\n\nfunc main() {\n    \n}\n',
  rust: '// Write your solution here\nfn main() {\n    \n}\n',
};

export default function CodeEditor({
  onCodeChange,
  initialCode = '',
}: {
  onCodeChange: (code: string, language: string) => void;
  initialCode?: string;
}) {
  const [language, setLanguage] = useState('javascript');
  const [code, setCode] = useState(initialCode || DEFAULT_CODE[language]);

  const handleLanguageChange = (newLanguage: string) => {
    setLanguage(newLanguage);
    const newCode = DEFAULT_CODE[newLanguage] || '';
    setCode(newCode);
    onCodeChange(newCode, newLanguage);
  };

  const handleCodeChange = (value: string | undefined) => {
    const newCode = value || '';
    setCode(newCode);
    onCodeChange(newCode, language);
  };

  const handleReset = () => {
    const defaultCode = DEFAULT_CODE[language] || '';
    setCode(defaultCode);
    onCodeChange(defaultCode, language);
  };

  return (
    <div className="flex flex-col h-full bg-[#1e1e1e] rounded-lg overflow-hidden">
      {/* Toolbar */}
      <div className="flex items-center justify-between p-3 border-b border-gray-700 bg-[#252526]">
        <div className="flex items-center gap-3">
          <select
            value={language}
            onChange={(e) => handleLanguageChange(e.target.value)}
            title="Select programming language"
            aria-label="Select programming language"
            className="w-[140px] h-8 bg-[#3c3c3c] border border-gray-600 text-white text-sm rounded px-2 focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            {LANGUAGES.map((lang) => (
              <option key={lang.id} value={lang.id}>
                {lang.name}
              </option>
            ))}
          </select>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={handleReset}
            className="text-gray-400 hover:text-white hover:bg-gray-700"
          >
            <RotateCcw className="w-4 h-4 mr-1" />
            Reset
          </Button>
        </div>
      </div>

      {/* Editor */}
      <div className="flex-1">
        <Editor
          height="100%"
          language={language}
          value={code}
          onChange={handleCodeChange}
          theme="vs-dark"
          options={{
            minimap: { enabled: false },
            fontSize: 14,
            lineNumbers: 'on',
            scrollBeyondLastLine: false,
            automaticLayout: true,
            tabSize: 2,
            wordWrap: 'on',
            padding: { top: 16 },
          }}
        />
      </div>
    </div>
  );
}
