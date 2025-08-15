import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { ChevronLeftIcon, PencilIcon, TrashIcon, PlusIcon } from '@heroicons/react/24/outline';
import { useFormsStore } from '../stores/formsStore';
import type { AdminForm } from '../stores/formsStore';
import { API_ENDPOINTS } from '../config/api';

interface FormQuestion {
  id: number;
  questionText: string;
  questionType: string;
  required: boolean;
  scoringRubric: any;
  orderIndex: number;
}

interface FormDetails extends AdminForm {
  questions: FormQuestion[];
}

export default function FormDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { selectedForm, fetchForm, updateForm } = useFormsStore();
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState<FormDetails | null>(null);
  const [isEditingTitle, setIsEditingTitle] = useState(false);
  const [titleValue, setTitleValue] = useState('');

  useEffect(() => {
    if (id) {
      loadFormDetails(id);
    }
  }, [id]);

  const loadFormDetails = async (formId: string) => {
    setLoading(true);
    try {
      const response = await fetch(API_ENDPOINTS.FORMS.BY_ID(formId), {
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (response.ok) {
        const { data } = await response.json();
        setForm(data);
        setTitleValue(data.title || '');
      } else if (response.status === 404) {
        navigate('/forms', { replace: true });
      } else {
        throw new Error('Failed to load form details');
      }
    } catch (error) {
      console.error('Error loading form details:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTitleSave = async () => {
    if (!form || !titleValue.trim() || titleValue === form.title) {
      setIsEditingTitle(false);
      setTitleValue(form?.title || '');
      return;
    }

    try {
      await updateForm(form.id, { title: titleValue.trim() });
      setForm(prev => prev ? { ...prev, title: titleValue.trim() } : null);
      setIsEditingTitle(false);
    } catch (error) {
      console.error('Failed to update form title:', error);
      alert('Failed to update form title. Please try again.');
    }
  };

  const handleTitleCancel = () => {
    setTitleValue(form?.title || '');
    setIsEditingTitle(false);
  };

  const getStatusBadge = (status: string) => {
    const statusClasses = {
      active: 'admin-badge admin-badge-success',
      draft: 'admin-badge admin-badge-warning',
      paused: 'admin-badge admin-badge-info',
      archived: 'admin-badge admin-badge-danger'
    };
    return statusClasses[status as keyof typeof statusClasses] || 'admin-badge';
  };

  const getQuestionTypeBadge = (type: string) => {
    const typeMap: Record<string, string> = {
      text: 'Text',
      email: 'Email',
      phone: 'Phone',
      radio: 'Multiple Choice',
      checkbox: 'Checkboxes',
      textarea: 'Long Text',
      number: 'Number',
      date: 'Date',
      rating: 'Rating',
      select: 'Dropdown'
    };
    return typeMap[type] || type;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-slate-500">Loading form details...</div>
      </div>
    );
  }

  if (!form) {
    return (
      <div className="text-center py-12">
        <h3 className="text-lg font-medium text-slate-900 mb-2">Form not found</h3>
        <p className="text-slate-500 mb-4">The form you're looking for doesn't exist.</p>
        <Link to="/forms" className="admin-btn-primary">
          Back to Forms
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header with breadcrumb */}
      <div className="flex items-center space-x-4">
        <Link 
          to="/forms" 
          className="flex items-center text-slate-500 hover:text-slate-700 transition-colors"
        >
          <ChevronLeftIcon className="w-5 h-5 mr-1" />
          Back to Forms
        </Link>
      </div>

      {/* Form header */}
      <div className="admin-card">
        <div className="admin-card-header">
          <div className="flex items-center justify-between">
            <div className="flex-1">
              {isEditingTitle ? (
                <div className="flex items-center space-x-3">
                  <input
                    type="text"
                    value={titleValue}
                    onChange={(e) => setTitleValue(e.target.value)}
                    className="admin-input text-xl font-semibold"
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') handleTitleSave();
                      if (e.key === 'Escape') handleTitleCancel();
                    }}
                    onBlur={handleTitleSave}
                    autoFocus
                  />
                  <div className="flex space-x-2">
                    <button
                      onClick={handleTitleSave}
                      className="text-success-600 hover:text-success-700 transition-colors"
                      title="Save (Enter)"
                    >
                      ✓
                    </button>
                    <button
                      onClick={handleTitleCancel}
                      className="text-slate-400 hover:text-slate-600 transition-colors"
                      title="Cancel (Esc)"
                    >
                      ✕
                    </button>
                  </div>
                </div>
              ) : (
                <div className="flex items-center space-x-3">
                  <h1 className="text-xl font-semibold text-slate-900">{form.title}</h1>
                  <button
                    onClick={() => setIsEditingTitle(true)}
                    className="text-slate-400 hover:text-slate-600 transition-colors"
                    title="Edit title"
                  >
                    <PencilIcon className="w-4 h-4" />
                  </button>
                </div>
              )}
              <p className="text-slate-500 text-sm mt-1">{form.description || 'No description provided'}</p>
            </div>
            <div className="flex items-center space-x-3">
              <span className={getStatusBadge(form.status)}>
                {form.status.charAt(0).toUpperCase() + form.status.slice(1)}
              </span>
            </div>
          </div>
        </div>
        
        <div className="admin-card-body">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <dt className="text-sm font-medium text-slate-500">Total Responses</dt>
              <dd className="text-2xl font-semibold text-slate-900">{form.totalResponses}</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-slate-500">Conversion Rate</dt>
              <dd className="text-2xl font-semibold text-slate-900">{(form.conversionRate * 100).toFixed(1)}%</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-slate-500">Avg. Completion Time</dt>
              <dd className="text-2xl font-semibold text-slate-900">{Math.round(form.averageCompletionTime / 60)}m</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-slate-500">Questions</dt>
              <dd className="text-2xl font-semibold text-slate-900">{form.questions?.length || 0}</dd>
            </div>
          </div>
        </div>
      </div>

      {/* Questions section */}
      <div className="admin-card">
        <div className="admin-card-header">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-medium text-slate-900">Form Questions</h3>
              <p className="text-sm text-slate-500">Questions in this form and their configuration</p>
            </div>
            <button 
              className="admin-btn-primary disabled:opacity-50" 
              disabled
              title="Question editing coming in future update"
            >
              <PlusIcon className="w-4 h-4 mr-2" />
              Add Question
            </button>
          </div>
        </div>
        
        <div className="admin-card-body p-0">
          {form.questions && form.questions.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="admin-table">
                <thead className="admin-table-header">
                  <tr>
                    <th className="admin-table-header-cell">#</th>
                    <th className="admin-table-header-cell">Question</th>
                    <th className="admin-table-header-cell">Type</th>
                    <th className="admin-table-header-cell">Required</th>
                    <th className="admin-table-header-cell">Scoring</th>
                    <th className="admin-table-header-cell">Actions</th>
                  </tr>
                </thead>
                <tbody className="admin-table-body">
                  {form.questions
                    .sort((a, b) => a.orderIndex - b.orderIndex)
                    .map((question, index) => (
                    <tr key={question.id} className="admin-table-row">
                      <td className="admin-table-cell font-medium text-slate-500">
                        {index + 1}
                      </td>
                      <td className="admin-table-cell">
                        <div className="max-w-md">
                          <p className="text-sm font-medium text-slate-900 truncate">
                            {question.questionText}
                          </p>
                        </div>
                      </td>
                      <td className="admin-table-cell">
                        <span className="admin-badge admin-badge-info">
                          {getQuestionTypeBadge(question.questionType)}
                        </span>
                      </td>
                      <td className="admin-table-cell">
                        {question.required ? (
                          <span className="admin-badge admin-badge-danger">Required</span>
                        ) : (
                          <span className="admin-badge">Optional</span>
                        )}
                      </td>
                      <td className="admin-table-cell">
                        {question.scoringRubric ? (
                          <span className="admin-badge admin-badge-success">Scored</span>
                        ) : (
                          <span className="admin-badge">No Score</span>
                        )}
                      </td>
                      <td className="admin-table-cell">
                        <div className="flex items-center space-x-2">
                          <button 
                            className="text-slate-400 hover:text-slate-600 disabled:opacity-50" 
                            disabled
                            title="Question editing coming in future update"
                          >
                            <PencilIcon className="w-4 h-4" />
                          </button>
                          <button 
                            className="text-slate-400 hover:text-danger-600 disabled:opacity-50" 
                            disabled
                            title="Question deletion coming in future update"
                          >
                            <TrashIcon className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-slate-500">No questions found for this form.</p>
            </div>
          )}
        </div>
      </div>

      {/* Theme section */}
      {form.theme && (
        <div className="admin-card">
          <div className="admin-card-header">
            <h3 className="text-lg font-medium text-slate-900">Theme Configuration</h3>
            <p className="text-sm text-slate-500">Visual styling for this form</p>
          </div>
          
          <div className="admin-card-body">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
              <div>
                <dt className="text-sm font-medium text-slate-500">Primary Color</dt>
                <dd className="flex items-center space-x-2 mt-1">
                  <div 
                    className="w-6 h-6 rounded border border-slate-200"
                    style={{ backgroundColor: form.theme.primaryColor }}
                  />
                  <span className="text-sm text-slate-900 font-mono">{form.theme.primaryColor}</span>
                </dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-slate-500">Font Family</dt>
                <dd className="text-sm text-slate-900 mt-1">{form.theme.fontFamily}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-slate-500">Border Radius</dt>
                <dd className="text-sm text-slate-900 mt-1">{form.theme.borderRadius}</dd>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Form settings */}
      <div className="admin-card">
        <div className="admin-card-header">
          <h3 className="text-lg font-medium text-slate-900">Form Settings</h3>
          <p className="text-sm text-slate-500">Configuration options for this form</p>
        </div>
        
        <div className="admin-card-body">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <dt className="text-sm font-medium text-slate-500">Authentication Required</dt>
              <dd className="text-sm text-slate-900 mt-1">
                {form.settings.requireAuth ? 'Yes' : 'No'}
              </dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-slate-500">Multiple Submissions</dt>
              <dd className="text-sm text-slate-900 mt-1">
                {form.settings.allowMultipleSubmissions ? 'Allowed' : 'Not allowed'}
              </dd>
            </div>
            {form.settings.maxResponses && (
              <div>
                <dt className="text-sm font-medium text-slate-500">Response Limit</dt>
                <dd className="text-sm text-slate-900 mt-1">{form.settings.maxResponses.toLocaleString()}</dd>
              </div>
            )}
            {form.settings.expiresAt && (
              <div>
                <dt className="text-sm font-medium text-slate-500">Expires</dt>
                <dd className="text-sm text-slate-900 mt-1">
                  {new Date(form.settings.expiresAt).toLocaleDateString()}
                </dd>
              </div>
            )}
            <div>
              <dt className="text-sm font-medium text-slate-500">Created</dt>
              <dd className="text-sm text-slate-900 mt-1">
                {new Date(form.createdAt).toLocaleDateString()} at {new Date(form.createdAt).toLocaleTimeString()}
              </dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-slate-500">Last Modified</dt>
              <dd className="text-sm text-slate-900 mt-1">
                {new Date(form.updatedAt).toLocaleDateString()} at {new Date(form.updatedAt).toLocaleTimeString()}
              </dd>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}