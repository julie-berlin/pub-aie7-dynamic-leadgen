import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeftIcon } from '@heroicons/react/24/outline';
import { themeService, type SimpleTheme, type ThemeResponse } from '../services/themeService';
import { LoadingSpinner } from '../components/ui';

const FONT_OPTIONS = [
  { value: 'Inter', label: 'Inter (Modern Sans-Serif)' },
  { value: 'Arial', label: 'Arial (Classic Sans-Serif)' },
  { value: 'Helvetica', label: 'Helvetica (Clean Sans-Serif)' },
  { value: 'Georgia', label: 'Georgia (Elegant Serif)' },
  { value: 'Times New Roman', label: 'Times New Roman (Traditional Serif)' },
  { value: 'Roboto', label: 'Roboto (Google Sans-Serif)' },
  { value: 'Open Sans', label: 'Open Sans (Friendly Sans-Serif)' },
];

export default function ThemeEditorPage() {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const isEditing = !!id;

  const [loading, setLoading] = useState(isEditing);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Form state
  const [theme, setTheme] = useState<SimpleTheme>({
    name: '',
    description: '',
    primary_color: '#3b82f6',
    font_family: 'Inter',
    logo_url: '',
    custom_css: '',
    is_default: false
  });

  const [showAdvanced, setShowAdvanced] = useState(false);

  // Load existing theme if editing
  useEffect(() => {
    if (isEditing && id) {
      // Auth is guaranteed to be ready when this component renders
      loadTheme(id);
    }
  }, [isEditing, id]);

  const loadTheme = async (themeId: string) => {
    try {
      setLoading(true);
      const themeResponse = await themeService.getTheme(themeId);
      const simpleTheme = themeService.extractSimpleTheme(themeResponse);
      setTheme(simpleTheme);
      setShowAdvanced(!!simpleTheme.custom_css);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load theme');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!theme.name.trim()) {
      setError('Theme name is required');
      return;
    }

    try {
      setSaving(true);
      setError(null);

      if (isEditing && id) {
        await themeService.updateTheme(id, theme);
      } else {
        await themeService.createTheme(theme);
      }

      navigate('/themes');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save theme');
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    navigate('/themes');
  };

  const updateTheme = (updates: Partial<SimpleTheme>) => {
    setTheme(prev => ({ ...prev, ...updates }));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <LoadingSpinner />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-4">
        <button
          onClick={handleCancel}
          className="p-2 text-gray-400 hover:text-gray-600"
        >
          <ArrowLeftIcon className="w-5 h-5" />
        </button>
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">
            {isEditing ? 'Edit Theme' : 'Create Theme'}
          </h1>
          <p className="text-sm text-gray-500 mt-1">
            Customize colors, fonts, and branding for your forms
          </p>
        </div>
      </div>

      {/* Error message */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Form */}
        <div className="bg-white shadow rounded-lg p-6">
          <div className="space-y-6">
            {/* Basic Information */}
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Basic Information
              </h3>
              
              <div className="space-y-4">
                {/* Name */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Theme Name *
                  </label>
                  <input
                    type="text"
                    value={theme.name}
                    onChange={(e) => updateTheme({ name: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    placeholder="My Brand Theme"
                  />
                </div>

                {/* Description */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Description
                  </label>
                  <textarea
                    value={theme.description || ''}
                    onChange={(e) => updateTheme({ description: e.target.value })}
                    rows={2}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Optional description..."
                  />
                </div>

                {/* Default theme checkbox */}
                <div className="flex items-center">
                  <input
                    id="is-default"
                    type="checkbox"
                    checked={theme.is_default || false}
                    onChange={(e) => updateTheme({ is_default: e.target.checked })}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <label htmlFor="is-default" className="ml-2 block text-sm text-gray-900">
                    Set as default theme for new forms
                  </label>
                </div>
              </div>
            </div>

            {/* Styling */}
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Styling
              </h3>
              
              <div className="space-y-4">
                {/* Primary Color */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Primary Color *
                  </label>
                  <div className="flex items-center space-x-3">
                    <input
                      type="color"
                      value={theme.primary_color}
                      onChange={(e) => updateTheme({ primary_color: e.target.value })}
                      className="h-10 w-20 border border-gray-300 rounded cursor-pointer"
                    />
                    <input
                      type="text"
                      value={theme.primary_color}
                      onChange={(e) => updateTheme({ primary_color: e.target.value })}
                      className="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      placeholder="#3b82f6"
                    />
                  </div>
                </div>

                {/* Font Family */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Font Family *
                  </label>
                  <select
                    value={theme.font_family}
                    onChange={(e) => updateTheme({ font_family: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  >
                    {FONT_OPTIONS.map(font => (
                      <option key={font.value} value={font.value}>
                        {font.label}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Logo URL */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Logo URL
                  </label>
                  <input
                    type="url"
                    value={theme.logo_url || ''}
                    onChange={(e) => updateTheme({ logo_url: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    placeholder="https://example.com/logo.png"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Optional. URL to your logo image that will appear on forms.
                  </p>
                </div>
              </div>
            </div>

            {/* Advanced CSS */}
            <div>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-medium text-gray-900">
                  Advanced Customization
                </h3>
                <button
                  type="button"
                  onClick={() => setShowAdvanced(!showAdvanced)}
                  className="text-sm text-blue-600 hover:text-blue-700"
                >
                  {showAdvanced ? 'Hide' : 'Show'} Advanced Options
                </button>
              </div>

              {showAdvanced && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Custom CSS
                  </label>
                  <textarea
                    value={theme.custom_css || ''}
                    onChange={(e) => updateTheme({ custom_css: e.target.value })}
                    rows={8}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 font-mono text-sm"
                    placeholder="/* Add your custom CSS here */
.form-container {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.question-title {
  font-weight: 600;
  color: #2d3748;
}"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Advanced users can add custom CSS to override default styling.
                  </p>
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex items-center justify-end space-x-4 pt-6 border-t border-gray-200">
              <button
                type="button"
                onClick={handleCancel}
                className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleSave}
                disabled={saving || !theme.name.trim()}
                className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {saving ? 'Saving...' : (isEditing ? 'Update Theme' : 'Create Theme')}
              </button>
            </div>
          </div>
        </div>

        {/* Live Preview */}
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            Preview
          </h3>
          
          <div 
            className="border border-gray-200 rounded-lg p-6"
            style={{
              fontFamily: `${theme.font_family}, sans-serif`,
              '--primary-color': theme.primary_color
            } as React.CSSProperties}
          >
            {/* Logo preview */}
            {theme.logo_url && (
              <div className="mb-4">
                <img 
                  src={theme.logo_url} 
                  alt="Logo preview"
                  className="h-8 w-auto"
                  onError={(e) => {
                    (e.target as HTMLImageElement).style.display = 'none';
                  }}
                />
              </div>
            )}
            
            {/* Sample form elements */}
            <div className="space-y-4">
              <h2 className="text-xl font-semibold" style={{ color: theme.primary_color }}>
                Sample Form Title
              </h2>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Your Name
                </label>
                <input
                  type="text"
                  placeholder="John Smith"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  style={{ fontFamily: `${theme.font_family}, sans-serif` }}
                />
              </div>
              
              <button
                type="button"
                className="px-4 py-2 rounded-md text-white font-medium"
                style={{ 
                  backgroundColor: theme.primary_color,
                  fontFamily: `${theme.font_family}, sans-serif`
                }}
              >
                Continue
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}