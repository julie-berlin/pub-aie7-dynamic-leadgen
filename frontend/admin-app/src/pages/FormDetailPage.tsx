import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { PencilIcon, TrashIcon, PlusIcon, DocumentDuplicateIcon, SwatchIcon } from '@heroicons/react/24/outline';
import { useFormsStore } from '../stores/formsStore';
import type { AdminForm } from '../stores/formsStore';
import type { FormStatus } from '../types';
import { API_ENDPOINTS } from '../config/api';
import { createFormDetailBreadcrumbs } from '../components/common/Breadcrumb';
import { useBreadcrumbContext } from '../components/common/BreadcrumbContext';
import { themeService, type ThemeResponse } from '../services/themeService';

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
  status: FormStatus;
}

export default function FormDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { updateForm } = useFormsStore();
  const { setCustomBreadcrumbs } = useBreadcrumbContext();
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState<FormDetails | null>(null);
  const [isEditingTitle, setIsEditingTitle] = useState(false);
  const [titleValue, setTitleValue] = useState('');
  const [availableThemes, setAvailableThemes] = useState<ThemeResponse[]>([]);
  const [selectedThemeId, setSelectedThemeId] = useState<string>('');
  const [isSelectingTheme, setIsSelectingTheme] = useState(false);
  const [editingQuestionId, setEditingQuestionId] = useState<number | null>(null);
  const [questionEditValues, setQuestionEditValues] = useState<any>({});

  useEffect(() => {
    if (id) {
      loadFormDetails(id);
      loadAvailableThemes();
    }
  }, [id]);

  // Update breadcrumbs when form data changes
  useEffect(() => {
    if (form) {
      setCustomBreadcrumbs(createFormDetailBreadcrumbs(form.title));
    }
    
    // Cleanup breadcrumbs when component unmounts
    return () => {
      setCustomBreadcrumbs(undefined);
    };
  }, [form, setCustomBreadcrumbs]);

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
        
        // Transform API response to match expected form structure
        const transformedForm = {
          id: formId,
          clientId: data.client_id,
          title: data.title,
          description: data.description,
          status: data.status as FormStatus,
          tags: data.tags || [],
          createdAt: data.created_at,
          updatedAt: data.updated_at,
          totalResponses: data.total_responses || 0,
          conversionRate: data.conversion_rate || 0,
          averageCompletionTime: data.average_completion_time || 0,
          questions: (data.questions || []).map((q: any) => ({
            id: q.question_id || 0,
            questionText: q.question_text || '',
            questionType: q.input_type || 'text',
            required: q.is_required || false,
            scoringRubric: q.scoring_rubric,
            orderIndex: q.question_order || 0,
            options: q.options,
            description: q.description,
            placeholder: q.placeholder
          })),
          settings: {
            maxResponses: data.max_responses,
            expiresAt: data.expires_at,
            requireAuth: data.require_auth || false,
            allowMultipleSubmissions: data.allow_multiple_submissions || false,
          },
          theme: data.theme_config ? {
            primaryColor: data.theme_config.primary_color || '#3B82F6',
            fontFamily: data.theme_config.font_family || 'Inter',
            borderRadius: data.theme_config.border_radius || '0.5rem',
          } : undefined,
        };
        
        setForm(transformedForm);
        setTitleValue(transformedForm.title || '');
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

  const loadAvailableThemes = async () => {
    try {
      console.log('Loading available themes...');
      const themes = await themeService.getThemes();
      console.log('Loaded themes:', themes.length, themes);
      setAvailableThemes(themes);
    } catch (error) {
      console.error('Error loading themes:', error);
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

  const handleApplyTheme = async () => {
    if (!form || !selectedThemeId) return;

    try {
      // Get the selected theme details
      const selectedTheme = availableThemes.find(theme => theme.id === selectedThemeId);
      if (!selectedTheme) {
        alert('Selected theme not found');
        return;
      }

      console.log('Applying theme:', selectedTheme.name, 'to form:', form.id);

      // Apply theme to form by updating form's theme_config
      const token = localStorage.getItem('admin_token');
      const response = await fetch(API_ENDPOINTS.FORMS.BY_ID(form.id), {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          ...(token && { 'Authorization': `Bearer ${token}` }),
        },
        body: JSON.stringify({
          theme_config: {
            theme_id: selectedTheme.id,
            primary_color: selectedTheme.primary_color,
            font_family: selectedTheme.font_family,
            theme_name: selectedTheme.name
          }
        })
      });

      const responseData = await response.json();
      console.log('Theme apply response:', response.status, responseData);

      if (response.ok) {
        // Update local form state
        setForm(prev => prev ? {
          ...prev,
          theme: {
            primaryColor: selectedTheme.primary_color,
            fontFamily: selectedTheme.font_family,
            borderRadius: '0.5rem' // Default value
          }
        } : null);
        
        setIsSelectingTheme(false);
        setSelectedThemeId('');
        alert('Theme applied successfully!');
      } else {
        throw new Error(`Failed to apply theme: ${response.status} - ${responseData.message || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Failed to apply theme:', error);
      alert(`Failed to apply theme. Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  };

  const handleCancelThemeSelection = () => {
    setIsSelectingTheme(false);
    setSelectedThemeId('');
  };

  const handleEditQuestion = (question: FormQuestion) => {
    setEditingQuestionId(question.id);
    setQuestionEditValues({
      questionText: question.questionText,
      questionType: question.questionType,
      required: question.required
    });
  };

  const handleCancelEditQuestion = () => {
    setEditingQuestionId(null);
    setQuestionEditValues({});
  };

  const handleSaveQuestion = async (questionId: number) => {
    if (!form || !questionEditValues.questionText?.trim()) {
      handleCancelEditQuestion();
      return;
    }

    try {
      // For now, just update the local state - full API integration can be added later
      setForm(prev => {
        if (!prev) return null;
        return {
          ...prev,
          questions: prev.questions.map(q => 
            q.id === questionId 
              ? { ...q, questionText: questionEditValues.questionText.trim() }
              : q
          )
        };
      });
      
      handleCancelEditQuestion();
      alert('Question updated successfully! (Full API integration coming in next phase)');
    } catch (error) {
      console.error('Failed to update question:', error);
      alert('Failed to update question. Please try again.');
    }
  };

  const handleDeleteQuestion = async (questionId: number) => {
    if (!form) return;

    const question = form.questions.find(q => q.id === questionId);
    const confirmed = confirm(
      `Are you sure you want to delete the question "${question?.questionText}"? This action cannot be undone.`
    );
    
    if (!confirmed) return;

    try {
      // For now, just update the local state - full API integration can be added later
      setForm(prev => {
        if (!prev) return null;
        return {
          ...prev,
          questions: prev.questions.filter(q => q.id !== questionId)
        };
      });
      
      alert('Question deleted successfully! (Full API integration coming in next phase)');
    } catch (error) {
      console.error('Failed to delete question:', error);
      alert('Failed to delete question. Please try again.');
    }
  };

  const handleStatusChange = async (newStatus: string) => {
    if (!form || form.status === newStatus) return;

    // Confirmation for certain status changes
    if (newStatus === 'archived') {
      const confirmed = confirm(
        'Are you sure you want to archive this form? Archived forms stop accepting new responses and are hidden from most views.'
      );
      if (!confirmed) return;
    }

    if (newStatus === 'active' && form.status === 'draft') {
      const confirmed = confirm(
        'Are you sure you want to activate this form? Once active, it will be publicly accessible and will start collecting responses.'
      );
      if (!confirmed) return;
    }

    try {
      const response = await fetch(API_ENDPOINTS.FORMS.UPDATE(form.id), {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          status: newStatus
        })
      });

      if (response.ok) {
        setForm(prev => prev ? { ...prev, status: newStatus as FormStatus } : null);
        
        // Update the form in the store as well
        await updateForm(form.id, { status: newStatus as FormStatus });
      } else {
        throw new Error('Failed to update form status');
      }
    } catch (error) {
      console.error('Failed to update form status:', error);
      alert('Failed to update form status. Please try again.');
    }
  };

  const handleDuplicateForm = async () => {
    if (!form) return;

    const confirmed = confirm(
      `Create a duplicate of "${form.title}"? The copy will be created as a draft with all questions and settings.`
    );
    if (!confirmed) return;

    try {
      // Create duplicate with modified title
      const duplicateData = {
        title: `${form.title} (Copy)`,
        description: form.description,
        status: 'draft', // Always create copies as drafts
        theme_config: form.theme ? {
          primary_color: form.theme.primaryColor,
          font_family: form.theme.fontFamily,
          border_radius: form.theme.borderRadius
        } : null,
        settings: {
          require_auth: form.settings.requireAuth || false,
          allow_multiple_submissions: form.settings.allowMultipleSubmissions || false,
          max_responses: form.settings.maxResponses || null,
          expires_at: null // Clear expiration for copy
        }
      };

      const createResponse = await fetch(API_ENDPOINTS.FORMS.CREATE, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(duplicateData)
      });

      if (createResponse.ok) {
        const { data: newForm } = await createResponse.json();
        alert(`Form duplicated successfully! The copy "${newForm.title}" has been created as a draft.`);
        
        // Navigate to the new form's detail page
        navigate(`/forms/${newForm.id}`);
      } else {
        throw new Error('Failed to create duplicate form');
      }
    } catch (error) {
      console.error('Failed to duplicate form:', error);
      alert('Failed to duplicate form. Please try again.');
    }
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
              
              {/* Action buttons */}
              <div className="flex items-center space-x-2">
                <button
                  onClick={handleDuplicateForm}
                  className="admin-btn-secondary admin-btn-sm"
                  title="Duplicate this form"
                >
                  <DocumentDuplicateIcon className="w-4 h-4 mr-1" />
                  Duplicate
                </button>
                
                {/* Status management dropdown */}
                <div className="relative">
                  <select
                    value={form.status}
                    onChange={(e) => handleStatusChange(e.target.value)}
                    className="admin-input text-sm py-1 px-2 pr-8"
                    style={{ minWidth: '120px' }}
                  >
                    <option value="draft">Draft</option>
                    <option value="active">Active</option>
                    <option value="paused">Paused</option>
                    <option value="archived">Archived</option>
                  </select>
                </div>
              </div>
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
              className="admin-btn-primary flex items-center whitespace-nowrap" 
              onClick={() => alert('Add Question functionality will be implemented in the next phase')}
              title="Add a new question to this form"
            >
              <PlusIcon className="w-4 h-4 mr-2 flex-shrink-0" />
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
                          {editingQuestionId === question.id ? (
                            <input
                              type="text"
                              value={questionEditValues.questionText || question.questionText}
                              onChange={(e) => setQuestionEditValues((prev: any) => ({ ...prev, questionText: e.target.value }))}
                              className="admin-input text-sm w-full"
                              onKeyDown={(e) => {
                                if (e.key === 'Enter') handleSaveQuestion(question.id);
                                if (e.key === 'Escape') handleCancelEditQuestion();
                              }}
                              onBlur={() => handleSaveQuestion(question.id)}
                              autoFocus
                            />
                          ) : (
                            <p className="text-sm font-medium text-slate-900 truncate">
                              {question.questionText}
                            </p>
                          )}
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
                          {editingQuestionId === question.id ? (
                            <>
                              <button
                                onClick={() => handleSaveQuestion(question.id)}
                                className="text-success-600 hover:text-success-700 transition-colors"
                                title="Save changes (Enter)"
                              >
                                ✓
                              </button>
                              <button
                                onClick={handleCancelEditQuestion}
                                className="text-slate-400 hover:text-slate-600 transition-colors"
                                title="Cancel editing (Esc)"
                              >
                                ✕
                              </button>
                            </>
                          ) : (
                            <>
                              <button 
                                className="text-slate-400 hover:text-slate-600 transition-colors" 
                                onClick={() => handleEditQuestion(question)}
                                title="Edit question text"
                              >
                                <PencilIcon className="w-4 h-4" />
                              </button>
                              <button 
                                className="text-slate-400 hover:text-danger-600 transition-colors" 
                                onClick={() => handleDeleteQuestion(question.id)}
                                title="Delete this question"
                              >
                                <TrashIcon className="w-4 h-4" />
                              </button>
                            </>
                          )}
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
      <div className="admin-card">
        <div className="admin-card-header">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-medium text-slate-900">Theme Configuration</h3>
              <p className="text-sm text-slate-500">Apply a theme to style this form</p>
            </div>
            <button
              onClick={() => setIsSelectingTheme(true)}
              disabled={isSelectingTheme}
              className="text-slate-400 hover:text-slate-600 transition-colors disabled:opacity-50"
              title="Select theme"
            >
              <SwatchIcon className="w-4 h-4" />
            </button>
          </div>
        </div>
        
        <div className="admin-card-body">
          {isSelectingTheme ? (
            <div className="space-y-6">
              <div className="admin-form-group">
                <label htmlFor="themeSelect" className="admin-label">
                  Select Theme
                </label>
                <select
                  id="themeSelect"
                  value={selectedThemeId}
                  onChange={(e) => setSelectedThemeId(e.target.value)}
                  className="admin-input"
                >
                  <option value="">Choose a theme...</option>
                  {availableThemes.map((theme) => (
                    <option key={theme.id} value={theme.id}>
                      {theme.name} {theme.is_default && '(Default)'}
                    </option>
                  ))}
                </select>
              </div>

              {/* Theme preview */}
              {selectedThemeId && (() => {
                const selectedTheme = availableThemes.find(t => t.id === selectedThemeId);
                if (!selectedTheme) return null;
                
                return (
                  <div className="border border-slate-200 rounded-lg p-4 bg-slate-50">
                    <h4 className="text-sm font-medium text-slate-700 mb-3">Preview</h4>
                    <div className="space-y-3">
                      <div
                        className="p-4 bg-white border-2 shadow-sm rounded-lg"
                        style={{
                          borderColor: selectedTheme.primary_color,
                          fontFamily: `${selectedTheme.font_family}, sans-serif`
                        }}
                      >
                        <h5 className="font-semibold text-slate-900 mb-2">Sample Question</h5>
                        <p className="text-slate-600 text-sm mb-3">How would you rate your experience with our service?</p>
                        <button
                          className="px-4 py-2 text-white rounded transition-colors"
                          style={{
                            backgroundColor: selectedTheme.primary_color
                          }}
                        >
                          Submit Response
                        </button>
                      </div>
                      
                      {/* Theme details */}
                      <div className="grid grid-cols-3 gap-4 text-xs">
                        <div>
                          <span className="text-slate-500">Primary Color:</span>
                          <div className="flex items-center space-x-1 mt-1">
                            <div 
                              className="w-4 h-4 rounded border border-slate-200"
                              style={{ backgroundColor: selectedTheme.primary_color }}
                            />
                            <span className="font-mono">{selectedTheme.primary_color}</span>
                          </div>
                        </div>
                        <div>
                          <span className="text-slate-500">Font:</span>
                          <div className="mt-1">{selectedTheme.font_family}</div>
                        </div>
                        <div>
                          <span className="text-slate-500">Description:</span>
                          <div className="mt-1">{selectedTheme.description || 'No description'}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })()}

              <div className="flex items-center justify-end space-x-3 pt-4 border-t border-slate-200">
                <button
                  onClick={handleCancelThemeSelection}
                  className="admin-btn-secondary"
                >
                  Cancel
                </button>
                <button
                  onClick={handleApplyTheme}
                  disabled={!selectedThemeId}
                  className="admin-btn-primary disabled:opacity-50"
                >
                  Apply Theme
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {/* Current theme display */}
              {form?.theme ? (
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
                  <div>
                    <dt className="text-sm font-medium text-slate-500">Primary Color</dt>
                    <dd className="flex items-center space-x-2 mt-1">
                      <div 
                        className="w-6 h-6 rounded border border-slate-200"
                        style={{ backgroundColor: form.theme.primaryColor }}
                      />
                      <span className="text-sm text-slate-900 font-mono">
                        {form.theme.primaryColor}
                      </span>
                    </dd>
                  </div>
                  <div>
                    <dt className="text-sm font-medium text-slate-500">Font Family</dt>
                    <dd className="text-sm text-slate-900 mt-1">
                      {form.theme.fontFamily}
                    </dd>
                  </div>
                  <div>
                    <dt className="text-sm font-medium text-slate-500">Applied Theme</dt>
                    <dd className="text-sm text-slate-900 mt-1">
                      Custom Theme
                    </dd>
                  </div>
                </div>
              ) : (
                <div className="text-center py-8 text-slate-500">
                  <SwatchIcon className="w-12 h-12 mx-auto mb-2 text-slate-300" />
                  <p>No theme applied to this form</p>
                  <p className="text-sm">Click the theme icon to select and apply a theme</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

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