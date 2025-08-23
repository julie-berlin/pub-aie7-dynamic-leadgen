import { useEffect, useState, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  PlusIcon, 
  FunnelIcon, 
  MagnifyingGlassIcon, 
  DocumentTextIcon,
  UsersIcon,
  ArrowTrendingUpIcon,
  ClockIcon,
  EllipsisVerticalIcon,
  PlayIcon,
  PauseIcon,
  ArchiveBoxIcon,
  DocumentDuplicateIcon,
  TrashIcon
} from '@heroicons/react/24/outline';
import { useFormsStore } from '../stores/formsStore';

export default function FormsPage() {
  const navigate = useNavigate();
  const {
    forms,
    filters,
    isLoading,
    fetchForms,
    updateForm,
    setFilters,
    clearFilters,
  } = useFormsStore();

  const [searchTerm, setSearchTerm] = useState(filters.search);
  const [openDropdown, setOpenDropdown] = useState<string | null>(null);
  const [selectedForms, setSelectedForms] = useState<string[]>([]);
  const [bulkActionLoading, setBulkActionLoading] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchForms();
  }, [fetchForms]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setOpenDropdown(null);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleSearch = (value: string) => {
    setSearchTerm(value);
    setFilters({ search: value });
  };

  const handleStatusChange = async (formId: string, newStatus: string, currentStatus: string) => {
    if (currentStatus === newStatus) return;

    // Confirmation for certain status changes
    if (newStatus === 'archived') {
      const confirmed = confirm(
        'Are you sure you want to archive this form? Archived forms stop accepting new responses.'
      );
      if (!confirmed) return;
    }

    if (newStatus === 'active' && currentStatus === 'draft') {
      const confirmed = confirm(
        'Are you sure you want to activate this form? Once active, it will be publicly accessible.'
      );
      if (!confirmed) return;
    }

    try {
      await updateForm(formId, { status: newStatus });
      setOpenDropdown(null);
    } catch (error) {
      console.error('Failed to update form status:', error);
      alert('Failed to update form status. Please try again.');
    }
  };

  const handleDuplicateForm = async (formId: string, formTitle: string) => {
    const confirmed = confirm(
      `Create a duplicate of "${formTitle}"? The copy will be created as a draft with all questions and settings.`
    );
    if (!confirmed) return;

    try {
      // Since there's no specific duplicate endpoint, we'll fetch the form and create a new one
      const token = localStorage.getItem('admin_token');
      if (!token) {
        alert('Authentication required. Please log in again.');
        return;
      }

      const response = await fetch(`http://localhost:8000/api/forms/${formId}`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch form details');
      }

      const { data: originalForm } = await response.json();

      // Create duplicate with modified title
      const duplicateData = {
        title: `${originalForm.title} (Copy)`,
        description: originalForm.description,
        status: 'draft', // Always create copies as drafts
        theme_config: originalForm.theme_config,
        settings: {
          ...originalForm.settings,
          require_auth: originalForm.settings.requireAuth || false,
          allow_multiple_submissions: originalForm.settings.allowMultipleSubmissions || false,
          max_responses: originalForm.settings.maxResponses || null,
          expires_at: null // Clear expiration for copy
        }
      };

      const createResponse = await fetch('http://localhost:8000/api/forms', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(duplicateData)
      });

      if (createResponse.ok) {
        const { data: newForm } = await createResponse.json();
        
        // Copy questions if they exist
        if (originalForm.questions && originalForm.questions.length > 0) {
          // Note: This would require a separate API endpoint for copying questions
          // For now, we'll just show success message
          console.log('Questions would be copied:', originalForm.questions);
        }

        setOpenDropdown(null);
        await fetchForms(); // Refresh the forms list
        alert(`Form duplicated successfully! The copy "${newForm.title}" has been created as a draft.`);
      } else {
        throw new Error('Failed to create duplicate form');
      }
    } catch (error) {
      console.error('Failed to duplicate form:', error);
      alert('Failed to duplicate form. Please try again.');
    }
  };

  const handleSelectForm = (formId: string) => {
    setSelectedForms(prev => 
      prev.includes(formId) 
        ? prev.filter(id => id !== formId)
        : [...prev, formId]
    );
  };

  const handleSelectAll = () => {
    if (selectedForms.length === forms.length) {
      setSelectedForms([]);
    } else {
      setSelectedForms(forms.map(form => form.id));
    }
  };

  const handleBulkStatusChange = async (newStatus: string) => {
    if (selectedForms.length === 0) return;

    const selectedFormTitles = forms
      .filter(form => selectedForms.includes(form.id))
      .map(form => form.title);

    const confirmed = confirm(
      `Change status to "${newStatus}" for ${selectedForms.length} selected forms?\n\nForms:\n${selectedFormTitles.join('\n')}`
    );
    if (!confirmed) return;

    setBulkActionLoading(true);
    try {
      // Update each form individually (since we don't have a bulk endpoint)
      const updatePromises = selectedForms.map(formId =>
        updateForm(formId, { status: newStatus })
      );

      await Promise.all(updatePromises);
      setSelectedForms([]);
      alert(`Successfully updated ${selectedForms.length} forms to ${newStatus}.`);
    } catch (error) {
      console.error('Failed to update forms:', error);
      alert('Failed to update some forms. Please try again.');
    } finally {
      setBulkActionLoading(false);
    }
  };

  const handleBulkDelete = async () => {
    if (selectedForms.length === 0) return;

    const selectedFormTitles = forms
      .filter(form => selectedForms.includes(form.id))
      .map(form => form.title);

    const confirmed = confirm(
      `⚠️ DELETE ${selectedForms.length} selected forms?\n\nThis action cannot be undone!\n\nForms to delete:\n${selectedFormTitles.join('\n')}`
    );
    if (!confirmed) return;

    setBulkActionLoading(true);
    try {
      // Delete each form individually
      const deletePromises = selectedForms.map(async (formId) => {
        const response = await fetch(`http://localhost:8000/api/forms/${formId}`, {
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json' }
        });
        if (!response.ok) {
          throw new Error(`Failed to delete form ${formId}`);
        }
        return formId;
      });

      await Promise.all(deletePromises);
      setSelectedForms([]);
      await fetchForms(); // Refresh the list
      alert(`Successfully deleted ${selectedForms.length} forms.`);
    } catch (error) {
      console.error('Failed to delete forms:', error);
      alert('Failed to delete some forms. Please try again.');
    } finally {
      setBulkActionLoading(false);
    }
  };

  const statusColors = {
    draft: 'bg-slate-100 text-slate-800',
    active: 'bg-success-100 text-success-800',
    paused: 'bg-warning-100 text-warning-800',
    archived: 'bg-slate-100 text-slate-800',
  };

  if (isLoading && forms.length === 0) {
    return (
      <div className="space-y-6">
        {/* Loading skeleton */}
        <div className="flex justify-between items-center">
          <div className="h-8 bg-slate-200 rounded w-32 animate-pulse"></div>
          <div className="h-10 bg-slate-200 rounded w-24 animate-pulse"></div>
        </div>
        <div className="space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="admin-card animate-pulse">
              <div className="h-6 bg-slate-200 rounded w-1/3 mb-2"></div>
              <div className="h-4 bg-slate-200 rounded w-2/3 mb-4"></div>
              <div className="flex space-x-4">
                <div className="h-4 bg-slate-200 rounded w-16"></div>
                <div className="h-4 bg-slate-200 rounded w-20"></div>
                <div className="h-4 bg-slate-200 rounded w-24"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Forms</h1>
          <p className="mt-1 text-sm text-slate-600">
            Manage your lead generation forms and campaigns
          </p>
        </div>
        <button 
          className="admin-btn-primary disabled:opacity-50"
          disabled
          title="Form creation coming in future update"
        >
          <PlusIcon className="w-4 h-4 mr-2" />
          Create Form
        </button>
      </div>

      {/* Filters and search */}
      <div className="admin-card">
        <div className="flex flex-col sm:flex-row gap-4">
          {/* Search */}
          <div className="flex-1 relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <MagnifyingGlassIcon className="h-4 w-4 text-slate-400" />
            </div>
            <input
              type="text"
              className="admin-input pl-10"
              placeholder="Search forms..."
              value={searchTerm}
              onChange={(e) => handleSearch(e.target.value)}
            />
          </div>

          {/* Status filter */}
          <select
            className="admin-select"
            value={filters.status[0] || ''}
            onChange={(e) => setFilters({ status: e.target.value ? [e.target.value] : [] })}
          >
            <option value="">All Status</option>
            <option value="draft">Draft</option>
            <option value="active">Active</option>
            <option value="paused">Paused</option>
            <option value="archived">Archived</option>
          </select>

          {/* Filter button */}
          <button className="admin-btn-secondary">
            <FunnelIcon className="w-4 h-4 mr-2" />
            Filters
          </button>

          {/* Clear filters */}
          {(filters.search || filters.status.length > 0) && (
            <button
              onClick={clearFilters}
              className="admin-btn-secondary text-xs"
            >
              Clear
            </button>
          )}
        </div>
      </div>

      {/* Bulk actions toolbar */}
      {selectedForms.length > 0 && (
        <div className="admin-card bg-blue-50 border-blue-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <span className="text-sm font-medium text-blue-900">
                {selectedForms.length} form{selectedForms.length !== 1 ? 's' : ''} selected
              </span>
              <button
                onClick={() => setSelectedForms([])}
                className="text-sm text-blue-700 hover:text-blue-900 underline"
              >
                Clear selection
              </button>
            </div>
            
            <div className="flex items-center space-x-2">
              {/* Bulk status changes */}
              <button
                onClick={() => handleBulkStatusChange('active')}
                disabled={bulkActionLoading}
                className="admin-btn-sm bg-success-600 text-white hover:bg-success-700 disabled:opacity-50"
              >
                <PlayIcon className="w-4 h-4 mr-1" />
                Activate
              </button>
              
              <button
                onClick={() => handleBulkStatusChange('paused')}
                disabled={bulkActionLoading}
                className="admin-btn-sm bg-warning-600 text-white hover:bg-warning-700 disabled:opacity-50"
              >
                <PauseIcon className="w-4 h-4 mr-1" />
                Pause
              </button>
              
              <button
                onClick={() => handleBulkStatusChange('archived')}
                disabled={bulkActionLoading}
                className="admin-btn-sm bg-slate-600 text-white hover:bg-slate-700 disabled:opacity-50"
              >
                <ArchiveBoxIcon className="w-4 h-4 mr-1" />
                Archive
              </button>
              
              <div className="w-px h-6 bg-slate-300"></div>
              
              <button
                onClick={handleBulkDelete}
                disabled={bulkActionLoading}
                className="admin-btn-sm bg-red-600 text-white hover:bg-red-700 disabled:opacity-50"
              >
                <TrashIcon className="w-4 h-4 mr-1" />
                Delete
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Forms list */}
      <div className="space-y-4">
        {/* Select all header */}
        {forms.length > 0 && (
          <div className="flex items-center space-x-3 px-4 py-2 bg-slate-50 rounded-lg border">
            <input
              type="checkbox"
              checked={forms.length > 0 && selectedForms.length === forms.length}
              onChange={handleSelectAll}
              className="h-4 w-4 text-admin-600 focus:ring-admin-500 border-slate-300 rounded"
            />
            <span className="text-sm text-slate-600">
              {selectedForms.length === forms.length ? 'Deselect all' : 'Select all forms'}
            </span>
            <span className="text-xs text-slate-500">
              ({forms.length} total)
            </span>
          </div>
        )}
        {forms.length === 0 ? (
          <div className="admin-card text-center py-12">
            <DocumentTextIcon className="w-12 h-12 text-slate-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-slate-900 mb-2">No forms found</h3>
            <p className="text-slate-600 mb-4">
              {searchTerm || filters.status.length > 0
                ? 'No forms match your current filters.'
                : 'Get started by creating your first form.'}
            </p>
            <button 
              className="admin-btn-primary disabled:opacity-50"
              disabled
              title="Form creation coming in future update"
            >
              <PlusIcon className="w-4 h-4 mr-2" />
              Create Your First Form
            </button>
          </div>
        ) : (
          forms.map((form) => (
            <div key={form.id} className="admin-card hover:shadow-admin-md transition-shadow">
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3 flex-1">
                  {/* Checkbox for selection */}
                  <input
                    type="checkbox"
                    checked={selectedForms.includes(form.id)}
                    onChange={() => handleSelectForm(form.id)}
                    className="mt-2 h-4 w-4 text-admin-600 focus:ring-admin-500 border-slate-300 rounded"
                  />
                  
                  <div className="flex-1">
                    <div className="flex items-center space-x-3">
                    <Link 
                      to={`/forms/${form.id}`}
                      className="text-lg font-semibold text-slate-900 hover:text-admin-600 transition-colors"
                    >
                      {form.title}
                    </Link>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${statusColors[form.status]}`}>
                      {form.status}
                    </span>
                  </div>
                  {form.description && (
                    <p className="mt-1 text-sm text-slate-600 line-clamp-2">
                      {form.description}
                    </p>
                  )}
                  <div className="mt-3 flex items-center space-x-6 text-sm text-slate-500">
                    <div className="flex items-center">
                      <UsersIcon className="w-4 h-4 mr-1" />
                      {form.totalResponses.toLocaleString()} responses
                    </div>
                    <div className="flex items-center">
                      <ArrowTrendingUpIcon className="w-4 h-4 mr-1" />
                      {(form.conversionRate * 100).toFixed(1)}% conversion
                    </div>
                    <div className="flex items-center">
                      <ClockIcon className="w-4 h-4 mr-1" />
                      {Math.round(form.averageCompletionTime / 60)}m avg time
                    </div>
                  </div>
                  {form.tags.length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-1">
                      {form.tags.map((tag) => (
                        <span
                          key={tag}
                          className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-slate-100 text-slate-700"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                  </div>
                </div>
                <div className="ml-4 flex-shrink-0 flex items-center space-x-2">
                  <Link 
                    to={`/forms/${form.id}`}
                    className="admin-btn-secondary admin-btn-sm"
                  >
                    View Details
                  </Link>
                  <button 
                    className="admin-btn-secondary admin-btn-sm disabled:opacity-50"
                    disabled
                    title="Analytics view coming soon"
                  >
                    Analytics
                  </button>
                  <div className="relative" ref={dropdownRef}>
                    <button 
                      className="admin-btn-secondary admin-btn-sm"
                      onClick={() => setOpenDropdown(openDropdown === form.id ? null : form.id)}
                    >
                      <EllipsisVerticalIcon className="w-4 h-4" />
                    </button>
                    
                    {/* Dropdown menu */}
                    {openDropdown === form.id && (
                      <div className="absolute right-0 mt-2 w-48 bg-white border border-slate-200 rounded-lg shadow-lg z-10">
                        <div className="py-1">
                          {/* Status management */}
                          <div className="px-3 py-2 text-xs font-medium text-slate-500 uppercase tracking-wider border-b border-slate-100">
                            Change Status
                          </div>
                          
                          {form.status !== 'active' && (
                            <button
                              onClick={() => handleStatusChange(form.id, 'active', form.status)}
                              className="flex items-center w-full px-4 py-2 text-sm text-slate-700 hover:bg-slate-50"
                            >
                              <PlayIcon className="w-4 h-4 mr-3 text-success-500" />
                              Activate
                            </button>
                          )}
                          
                          {form.status !== 'paused' && form.status !== 'draft' && (
                            <button
                              onClick={() => handleStatusChange(form.id, 'paused', form.status)}
                              className="flex items-center w-full px-4 py-2 text-sm text-slate-700 hover:bg-slate-50"
                            >
                              <PauseIcon className="w-4 h-4 mr-3 text-warning-500" />
                              Pause
                            </button>
                          )}
                          
                          {form.status !== 'archived' && (
                            <button
                              onClick={() => handleStatusChange(form.id, 'archived', form.status)}
                              className="flex items-center w-full px-4 py-2 text-sm text-slate-700 hover:bg-slate-50"
                            >
                              <ArchiveBoxIcon className="w-4 h-4 mr-3 text-slate-500" />
                              Archive
                            </button>
                          )}
                          
                          <div className="border-t border-slate-100"></div>
                          
                          {/* Other actions */}
                          <button
                            onClick={() => handleDuplicateForm(form.id, form.title)}
                            className="flex items-center w-full px-4 py-2 text-sm text-slate-700 hover:bg-slate-50"
                          >
                            <DocumentDuplicateIcon className="w-4 h-4 mr-3 text-slate-500" />
                            Duplicate
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
              <div className="mt-4 pt-4 border-t border-slate-200 flex items-center justify-between text-xs text-slate-500">
                <span>Created {new Date(form.createdAt).toLocaleDateString()}</span>
                <span>Last updated {new Date(form.updatedAt).toLocaleDateString()}</span>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Pagination placeholder */}
      {forms.length > 0 && (
        <div className="flex items-center justify-between">
          <p className="text-sm text-slate-700">
            Showing <span className="font-medium">1</span> to <span className="font-medium">{forms.length}</span> of{' '}
            <span className="font-medium">{forms.length}</span> results
          </p>
          <div className="flex space-x-2">
            <button className="admin-btn-secondary admin-btn-sm" disabled>
              Previous
            </button>
            <button className="admin-btn-secondary admin-btn-sm" disabled>
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
}