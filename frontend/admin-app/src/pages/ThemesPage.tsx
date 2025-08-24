import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { PlusIcon, PencilIcon, TrashIcon, StarIcon } from '@heroicons/react/24/outline';
import { StarIcon as StarIconSolid } from '@heroicons/react/24/solid';
import { themeService, type ThemeResponse } from '../services/themeService';
import { LoadingSpinner } from '../components/ui';

export default function ThemesPage() {
  const navigate = useNavigate();
  const [themes, setThemes] = useState<ThemeResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load themes on mount
  useEffect(() => {
    loadThemes();
  }, []);

  const loadThemes = async () => {
    try {
      setLoading(true);
      const themesData = await themeService.getThemes();
      setThemes(themesData);
      setError(null);
    } catch (err) {
      console.error('ThemesPage: Error loading themes:', err);
      setError(err instanceof Error ? err.message : 'Failed to load themes');
    } finally {
      setLoading(false);
    }
  };

  const handleSetDefault = async (themeId: string) => {
    try {
      await themeService.setDefaultTheme(themeId);
      await loadThemes(); // Refresh list
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to set default theme');
    }
  };

  const handleDelete = async (themeId: string) => {
    if (!confirm('Are you sure you want to delete this theme?')) return;
    
    try {
      await themeService.deleteTheme(themeId);
      await loadThemes(); // Refresh list
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete theme');
    }
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
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Themes</h1>
          <p className="text-sm text-gray-500 mt-1">
            Customize the look and feel of your forms
          </p>
        </div>
        <button
          onClick={() => navigate('/themes/new')}
          className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          <PlusIcon className="w-4 h-4 mr-2" />
          Create Theme
        </button>
      </div>

      {/* Error message */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
          {error}
        </div>
      )}

      {/* Themes list */}
      <div className="bg-white shadow rounded-lg overflow-hidden">
        {themes.length === 0 ? (
          <div className="text-center py-12">
            <PlusIcon className="mx-auto h-12 w-12 text-gray-300" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No themes</h3>
            <p className="mt-1 text-sm text-gray-500">
              Get started by creating your first theme.
            </p>
            <div className="mt-6">
              <button
                onClick={() => navigate('/themes/new')}
                className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <PlusIcon className="w-4 h-4 mr-2" />
                Create Theme
              </button>
            </div>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Primary Color
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Font
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Created
                  </th>
                  <th className="relative px-6 py-3">
                    <span className="sr-only">Actions</span>
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {themes.map((theme) => (
                  <tr key={theme.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div>
                          <div className="text-sm font-medium text-gray-900">
                            {theme.name}
                          </div>
                          {theme.description && (
                            <div className="text-sm text-gray-500">
                              {theme.description}
                            </div>
                          )}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center space-x-2">
                        <div
                          className="w-6 h-6 rounded-full border border-gray-300"
                          style={{ backgroundColor: theme.primary_color }}
                          title={theme.primary_color}
                        />
                        <span className="text-sm text-gray-900">
                          {theme.primary_color}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {theme.font_family}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center space-x-2">
                        {theme.is_default ? (
                          <div className="flex items-center space-x-1">
                            <StarIconSolid className="w-4 h-4 text-yellow-400" />
                            <span className="text-sm font-medium text-yellow-700">
                              Default
                            </span>
                          </div>
                        ) : theme.is_system_theme ? (
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                            System
                          </span>
                        ) : (
                          <span className="text-sm text-gray-500">Custom</span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(theme.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div className="flex items-center space-x-2">
                        {!theme.is_default && (
                          <button
                            onClick={() => handleSetDefault(theme.id)}
                            className="text-yellow-600 hover:text-yellow-900"
                            title="Set as default"
                          >
                            <StarIcon className="w-4 h-4" />
                          </button>
                        )}
                        <button
                          onClick={() => navigate(`/themes/${theme.id}/edit`)}
                          className="text-blue-600 hover:text-blue-900"
                          title="Edit theme"
                        >
                          <PencilIcon className="w-4 h-4" />
                        </button>
                        {!theme.is_system_theme && (
                          <button
                            onClick={() => handleDelete(theme.id)}
                            className="text-red-600 hover:text-red-900"
                            title="Delete theme"
                          >
                            <TrashIcon className="w-4 h-4" />
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}