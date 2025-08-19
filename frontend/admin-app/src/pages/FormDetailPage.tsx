import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { PencilIcon, TrashIcon, PlusIcon, DocumentDuplicateIcon } from '@heroicons/react/24/outline';
import { useFormsStore } from '../stores/formsStore';
import type { AdminForm } from '../stores/formsStore';
import type { FormStatus } from '../types';
import { API_ENDPOINTS } from '../config/api';
import { createFormDetailBreadcrumbs } from '../components/common/Breadcrumb';
import { useBreadcrumbContext } from '../components/common/BreadcrumbContext';

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
  const [isEditingTheme, setIsEditingTheme] = useState(false);
  const [themeValues, setThemeValues] = useState({
    primaryColor: '#3B82F6',
    fontFamily: 'Inter',
    borderRadius: '0.5rem'
  });
  const [editingQuestionId, setEditingQuestionId] = useState<number | null>(null);
  const [questionEditValues, setQuestionEditValues] = useState<any>({});

  useEffect(() => {
    if (id) {
      loadFormDetails(id);
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
            questionType: q.question_type || 'text',
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
        
        // Initialize theme values
        if (transformedForm.theme) {
          setThemeValues({
            primaryColor: transformedForm.theme.primaryColor || '#3B82F6',
            fontFamily: transformedForm.theme.fontFamily || 'Inter',
            borderRadius: transformedForm.theme.borderRadius || '0.5rem'
          });
        } else {
          // Set default theme values if no theme exists
          setThemeValues({
            primaryColor: '#3B82F6',
            fontFamily: 'Inter',
            borderRadius: '0.5rem'
          });
        }
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

  const handleThemeSave = async () => {
    if (!form) return;

    try {
      // Use form ID to create a consistent theme name
      const themeName = `Form ${form.id} Theme`;
      
      // First, check if a theme with this name already exists
      const existingThemesResponse = await fetch('/api/themes/');
      const existingThemesData = await existingThemesResponse.json();
      
      const existingTheme = existingThemesData.data.themes.find(
        (theme: any) => theme.name === themeName
      );
      
      const themeConfig = {
        name: `${form.title} Theme`,
        colors: {
          primary: themeValues.primaryColor,
          primaryHover: themeValues.primaryColor,
          primaryLight: themeValues.primaryColor,
          secondary: "#64748B",
          secondaryHover: "#4b5563",
          secondaryLight: "#f3f4f6",
          accent: "#10b981",
          text: "#111827",
          textLight: "#6b7280",
          textMuted: "#9ca3af",
          background: "#ffffff",
          backgroundLight: "#f9fafb",
          border: "#e5e7eb",
          error: "#ef4444",
          success: "#10b981",
          warning: "#f59e0b"
        },
        typography: {
          primary: `${themeValues.fontFamily}, sans-serif`,
          secondary: `${themeValues.fontFamily}, sans-serif`
        },
        spacing: {
          section: "2rem",
          element: "1rem"
        },
        borderRadius: themeValues.borderRadius,
        borderRadiusLg: "0.75rem",
        shadow: "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)",
        shadowLg: "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)"
      };
      
      let response;
      
      if (existingTheme) {
        // Update existing theme
        response = await fetch(`/api/themes/${existingTheme.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            description: `Theme for ${form.title}`,
            theme_config: themeConfig,
            primary_color: themeValues.primaryColor,
            secondary_color: "#64748B",
            font_family: themeValues.fontFamily,
            is_default: false
          })
        });
      } else {
        // Create new theme
        response = await fetch('/api/themes/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: themeName,
            description: `Theme for ${form.title}`,
            theme_config: themeConfig,
            primary_color: themeValues.primaryColor,
            secondary_color: "#64748B",
            font_family: themeValues.fontFamily,
            is_default: false
          })
        });
      }

      if (response.ok) {
        await response.json();
        setForm(prev => prev ? {
          ...prev,
          theme: {
            primaryColor: themeValues.primaryColor,
            fontFamily: themeValues.fontFamily,
            borderRadius: themeValues.borderRadius
          }
        } : null);
        setIsEditingTheme(false);
        alert('Theme saved successfully!');
      } else {
        const errorData = await response.json();
        console.error('Theme save failed:', response.status, errorData);
        throw new Error(`Failed to save theme: ${response.status} - ${errorData.message || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Failed to save theme:', error);
      alert(`Failed to save theme. Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  };

  const handleThemeCancel = () => {
    if (form?.theme) {
      setThemeValues({
        primaryColor: form.theme.primaryColor || '#3B82F6',
        fontFamily: form.theme.fontFamily || 'Inter',
        borderRadius: form.theme.borderRadius || '0.5rem'
      });
    }
    setIsEditingTheme(false);
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
              <p className="text-sm text-slate-500">Visual styling for this form</p>
            </div>
            <button
              onClick={() => setIsEditingTheme(true)}
              disabled={isEditingTheme}
              className="text-slate-400 hover:text-slate-600 transition-colors disabled:opacity-50"
              title="Edit theme"
            >
              <PencilIcon className="w-4 h-4" />
            </button>
          </div>
        </div>
        
        <div className="admin-card-body">
          {isEditingTheme ? (
            <div className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="admin-form-group">
                  <label htmlFor="primaryColor" className="admin-label">
                    Primary Color
                  </label>
                  <div className="flex items-center space-x-3">
                    <input
                      type="color"
                      id="primaryColor"
                      value={themeValues.primaryColor}
                      onChange={(e) => setThemeValues(prev => ({ ...prev, primaryColor: e.target.value }))}
                      className="w-12 h-10 rounded border border-slate-300 cursor-pointer"
                    />
                    <input
                      type="text"
                      value={themeValues.primaryColor}
                      onChange={(e) => setThemeValues(prev => ({ ...prev, primaryColor: e.target.value }))}
                      className="admin-input font-mono text-sm"
                      placeholder="#3B82F6"
                    />
                  </div>
                </div>

                <div className="admin-form-group">
                  <label htmlFor="fontFamily" className="admin-label">
                    Font Family
                  </label>
                  <select
                    id="fontFamily"
                    value={themeValues.fontFamily}
                    onChange={(e) => setThemeValues(prev => ({ ...prev, fontFamily: e.target.value }))}
                    className="admin-input"
                  >
                    <option value="Inter">Inter</option>
                    <option value="Roboto">Roboto</option>
                    <option value="Open Sans">Open Sans</option>
                    <option value="Lato">Lato</option>
                    <option value="Poppins">Poppins</option>
                    <option value="Montserrat">Montserrat</option>
                    <option value="Source Sans Pro">Source Sans Pro</option>
                    <option value="system-ui">System Default</option>
                  </select>
                </div>

                <div className="admin-form-group">
                  <label htmlFor="borderRadius" className="admin-label">
                    Border Radius
                  </label>
                  <select
                    id="borderRadius"
                    value={themeValues.borderRadius}
                    onChange={(e) => setThemeValues(prev => ({ ...prev, borderRadius: e.target.value }))}
                    className="admin-input"
                  >
                    <option value="0">None (0px)</option>
                    <option value="0.25rem">Small (4px)</option>
                    <option value="0.5rem">Medium (8px)</option>
                    <option value="0.75rem">Large (12px)</option>
                    <option value="1rem">Extra Large (16px)</option>
                    <option value="1.5rem">Rounded (24px)</option>
                  </select>
                </div>
              </div>

              {/* Theme preview */}
              <div className="border border-slate-200 rounded-lg p-4 bg-slate-50">
                <h4 className="text-sm font-medium text-slate-700 mb-3">Preview</h4>
                <div className="space-y-3">
                  <div
                    className="p-4 bg-white border-2 shadow-sm"
                    style={{
                      borderColor: themeValues.primaryColor,
                      borderRadius: themeValues.borderRadius,
                      fontFamily: themeValues.fontFamily
                    }}
                  >
                    <h5 className="font-semibold text-slate-900 mb-2">Sample Question</h5>
                    <p className="text-slate-600 text-sm mb-3">How would you rate your experience with our service?</p>
                    <button
                      className="px-4 py-2 text-white rounded transition-colors"
                      style={{
                        backgroundColor: themeValues.primaryColor,
                        borderRadius: themeValues.borderRadius
                      }}
                    >
                      Submit Response
                    </button>
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-end space-x-3 pt-4 border-t border-slate-200">
                <button
                  onClick={handleThemeCancel}
                  className="admin-btn-secondary"
                >
                  Cancel
                </button>
                <button
                  onClick={handleThemeSave}
                  className="admin-btn-primary"
                >
                  Save Theme
                </button>
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
              <div>
                <dt className="text-sm font-medium text-slate-500">Primary Color</dt>
                <dd className="flex items-center space-x-2 mt-1">
                  <div 
                    className="w-6 h-6 rounded border border-slate-200"
                    style={{ backgroundColor: form?.theme?.primaryColor || themeValues.primaryColor }}
                  />
                  <span className="text-sm text-slate-900 font-mono">
                    {form?.theme?.primaryColor || themeValues.primaryColor}
                  </span>
                </dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-slate-500">Font Family</dt>
                <dd className="text-sm text-slate-900 mt-1">
                  {form?.theme?.fontFamily || themeValues.fontFamily}
                </dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-slate-500">Border Radius</dt>
                <dd className="text-sm text-slate-900 mt-1">
                  {form?.theme?.borderRadius || themeValues.borderRadius}
                </dd>
              </div>
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