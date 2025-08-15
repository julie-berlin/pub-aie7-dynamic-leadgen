import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  PlusIcon, 
  FunnelIcon, 
  MagnifyingGlassIcon, 
  DocumentTextIcon,
  UsersIcon,
  ArrowTrendingUpIcon,
  ClockIcon
} from '@heroicons/react/24/outline';
import { useFormsStore } from '../stores/formsStore';

export default function FormsPage() {
  const navigate = useNavigate();
  const {
    forms,
    filters,
    isLoading,
    fetchForms,
    setFilters,
    clearFilters,
  } = useFormsStore();

  const [searchTerm, setSearchTerm] = useState(filters.search);

  useEffect(() => {
    fetchForms();
  }, [fetchForms]);

  const handleSearch = (value: string) => {
    setSearchTerm(value);
    setFilters({ search: value });
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

      {/* Forms list */}
      <div className="space-y-4">
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
                  <div className="relative">
                    <button className="admin-btn-secondary admin-btn-sm">
                      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                      </svg>
                    </button>
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