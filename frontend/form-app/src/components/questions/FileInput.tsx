import { useRef, useState } from 'react';
import type { UseFormRegister, Control } from 'react-hook-form';
import { useController } from 'react-hook-form';
import type { Question } from '../../types';

interface FileInputProps {
  question: Question;
  register: UseFormRegister<any>;
  control: Control<any>;
  error?: string;
  disabled?: boolean;
  defaultValue?: File[];
}

export default function FileInput({ question, control, error, disabled }: FileInputProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [dragOver, setDragOver] = useState(false);
  
  const { field } = useController({
    name: question.id,
    control,
    defaultValue: []
  });

  const allowedTypes = question.options?.allowedTypes || [];
  const maxFileSize = question.options?.maxFileSize ? parseInt(question.options.maxFileSize) : 5 * 1024 * 1024; // 5MB default
  const maxFiles = question.options?.maxFiles ? parseInt(question.options.maxFiles) : 1;
  const multiple = maxFiles > 1;

  const validateFile = (file: File): string | null => {
    if (allowedTypes.length > 0 && !allowedTypes.includes(file.type)) {
      return `File type ${file.type} is not allowed`;
    }
    if (file.size > maxFileSize) {
      return `File size must be less than ${Math.round(maxFileSize / (1024 * 1024))}MB`;
    }
    return null;
  };

  const handleFiles = (files: FileList | null) => {
    if (!files) return;

    const fileArray = Array.from(files);
    const currentFiles = field.value || [];
    const errors: string[] = [];

    // Validate each file
    for (const file of fileArray) {
      const error = validateFile(file);
      if (error) {
        errors.push(`${file.name}: ${error}`);
      }
    }

    if (errors.length > 0) {
      alert(errors.join('\n'));
      return;
    }

    // Check file count limit
    const newFiles = multiple ? [...currentFiles, ...fileArray] : fileArray;
    if (newFiles.length > maxFiles) {
      alert(`Maximum ${maxFiles} file(s) allowed`);
      return;
    }

    field.onChange(newFiles);
  };

  const removeFile = (index: number) => {
    const currentFiles = field.value || [];
    const newFiles = currentFiles.filter((_: File, i: number) => i !== index);
    field.onChange(newFiles);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    if (!disabled) {
      handleFiles(e.dataTransfer.files);
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const currentFiles = field.value || [];

  return (
    <div className="question-container">
      <label className="question-label">
        {question.text}
        {question.required && <span className="text-error ml-1">*</span>}
      </label>
      
      {question.description && (
        <p className="question-description">{question.description}</p>
      )}

      {/* File Drop Zone */}
      <div
        className={`border-2 border-dashed rounded-theme p-6 text-center transition-colors ${
          dragOver
            ? 'border-primary bg-primary bg-opacity-5'
            : 'border-border hover:border-primary-hover'
        } ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !disabled && fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple={multiple}
          accept={allowedTypes.join(',')}
          disabled={disabled}
          onChange={(e) => handleFiles(e.target.files)}
          className="hidden"
        />
        
        <div className="space-y-2">
          <svg className="w-10 h-10 mx-auto text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
          
          <div>
            <p className="text-text">
              <span className="font-medium text-primary">Click to upload</span> or drag and drop
            </p>
            <p className="text-sm text-text-muted">
              {allowedTypes.length > 0 && (
                <>Supported: {allowedTypes.join(', ')}<br /></>
              )}
              Max {formatFileSize(maxFileSize)} per file
              {multiple && `, up to ${maxFiles} files`}
            </p>
          </div>
        </div>
      </div>

      {/* File List */}
      {currentFiles.length > 0 && (
        <div className="mt-4 space-y-2">
          {currentFiles.map((file: File, index: number) => (
            <div
              key={`${file.name}-${index}`}
              className="flex items-center justify-between p-3 bg-background-light rounded-theme"
            >
              <div className="flex items-center space-x-3 flex-1 min-w-0">
                <svg className="w-5 h-5 text-primary flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
                </svg>
                
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-text truncate">{file.name}</p>
                  <p className="text-xs text-text-muted">{formatFileSize(file.size)}</p>
                </div>
              </div>
              
              {!disabled && (
                <button
                  type="button"
                  onClick={() => removeFile(index)}
                  className="p-1 text-text-muted hover:text-error transition-colors"
                >
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </button>
              )}
            </div>
          ))}
        </div>
      )}
      
      {error && (
        <p className="error-message">{error}</p>
      )}
    </div>
  );
}