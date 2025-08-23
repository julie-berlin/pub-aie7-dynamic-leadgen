import { useState, useRef } from 'react';
import { CloudArrowUpIcon, PhotoIcon, TrashIcon } from '@heroicons/react/24/outline';

interface LogoUploadProps {
  currentLogoUrl?: string;
  onLogoChange: (logoUrl: string | null) => void;
  disabled?: boolean;
}

/**
 * LogoUpload Component
 * 
 * Handles logo file upload with preview, validation, and removal.
 * Supports drag & drop and click to upload.
 */
export default function LogoUpload({ currentLogoUrl, onLogoChange, disabled = false }: LogoUploadProps) {
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = async (file: File) => {
    // Validate file type
    if (!file.type.startsWith('image/')) {
      alert('Please select an image file');
      return;
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      alert('File size must be less than 5MB');
      return;
    }

    setUploading(true);
    
    try {
      const formData = new FormData();
      formData.append('logo', file);

      const response = await fetch('/api/admin/upload/logo', {
        method: 'POST',
        headers: {
          Authorization: 'Bearer mock-token'
        },
        body: formData,
      });

      if (response.ok) {
        const { data } = await response.json();
        onLogoChange(data.logo_url);
      } else {
        let errorMessage = 'Upload failed';
        try {
          const errorData = await response.json();
          errorMessage = errorData.message || `Upload failed (${response.status})`;
        } catch (parseError) {
          // If response isn't JSON, use status text
          errorMessage = `Upload failed: ${response.status} ${response.statusText}`;
        }
        throw new Error(errorMessage);
      }
    } catch (error) {
      console.error('Logo upload failed:', error);
      alert(`Upload failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setUploading(false);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(false);
    
    if (disabled || uploading) return;

    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (!disabled && !uploading) {
      setDragOver(true);
    }
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleClick = () => {
    if (!disabled && !uploading && fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
    // Reset input so same file can be selected again
    e.target.value = '';
  };

  const handleRemoveLogo = async () => {
    if (!currentLogoUrl) return;

    const confirmed = confirm('Are you sure you want to remove your logo?');
    if (!confirmed) return;

    try {
      // Update client settings to remove logo
      const response = await fetch('/api/clients/me', {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          company_logo_url: null
        })
      });

      if (response.ok) {
        onLogoChange(null);
      } else {
        throw new Error('Failed to remove logo');
      }
    } catch (error) {
      console.error('Failed to remove logo:', error);
      alert('Failed to remove logo. Please try again.');
    }
  };

  return (
    <div className="space-y-4">
      {/* Current Logo Preview */}
      {currentLogoUrl && (
        <div className="flex items-start space-x-4">
          <div className="flex-shrink-0">
            <img
              src={currentLogoUrl}
              alt="Current logo"
              className="w-16 h-16 object-cover rounded-lg border border-slate-200"
            />
          </div>
          <div className="flex-1">
            <div className="text-sm font-medium text-slate-900">Current Logo</div>
            <div className="text-sm text-slate-500 mt-1">
              This logo will appear on your forms and surveys
            </div>
          </div>
          <button
            type="button"
            onClick={handleRemoveLogo}
            disabled={disabled || uploading}
            className="text-slate-400 hover:text-red-600 transition-colors disabled:opacity-50"
            title="Remove logo"
          >
            <TrashIcon className="w-5 h-5" />
          </button>
        </div>
      )}

      {/* Upload Area */}
      <div
        className={`
          relative border-2 border-dashed rounded-lg p-6 transition-colors cursor-pointer
          ${dragOver ? 'border-blue-400 bg-blue-50' : 'border-slate-300'}
          ${disabled || uploading ? 'opacity-50 cursor-not-allowed' : 'hover:border-slate-400'}
        `}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={handleClick}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleFileInput}
          disabled={disabled || uploading}
          className="hidden"
        />

        <div className="text-center">
          <div className="mx-auto w-12 h-12 text-slate-400 mb-4">
            {uploading ? (
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
            ) : (
              <CloudArrowUpIcon className="w-12 h-12" />
            )}
          </div>
          
          <div className="text-lg font-medium text-slate-900 mb-2">
            {uploading ? 'Uploading...' : currentLogoUrl ? 'Replace Logo' : 'Upload Logo'}
          </div>
          
          <div className="text-sm text-slate-500 mb-4">
            {uploading ? 'Please wait while your logo is being uploaded' : 'Drag and drop your logo here, or click to browse'}
          </div>
          
          <div className="text-xs text-slate-400">
            Supports: JPG, PNG, GIF • Max size: 5MB • Max dimensions: 1000x1000px
          </div>
        </div>

        {!uploading && (
          <PhotoIcon className="absolute top-2 right-2 w-5 h-5 text-slate-300" />
        )}
      </div>

      {/* Upload Tips */}
      <div className="text-xs text-slate-500 bg-slate-50 rounded-lg p-3">
        <div className="font-medium mb-1">Tips for best results:</div>
        <ul className="space-y-1">
          <li>• Use a square format (1:1 ratio) for consistent display</li>
          <li>• Ensure high contrast for visibility on various backgrounds</li>
          <li>• Test how your logo looks at small sizes</li>
        </ul>
      </div>
    </div>
  );
}