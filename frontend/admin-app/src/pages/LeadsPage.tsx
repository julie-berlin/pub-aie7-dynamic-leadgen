import { useEffect, useState, useRef } from 'react';
import { 
  FunnelIcon,
  MagnifyingGlassIcon,
  UsersIcon,
  EnvelopeIcon,
  PhoneIcon,
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon,
  ArrowTrendingUpIcon,
  CurrencyDollarIcon,
  EllipsisVerticalIcon,
  PencilIcon,
  EyeIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';
import { CheckCircleIcon as CheckCircleIconSolid, XCircleIcon as XCircleIconSolid } from '@heroicons/react/24/solid';
import { buildApiUrl, API_ENDPOINTS } from '../config/api';

interface Lead {
  lead_id: string;  // Safe unique identifier for React keys
  form_title: string;
  lead_status: 'yes' | 'maybe' | 'no' | 'unknown';
  final_score: number;
  started_at: string;
  completed_at: string | null;
  contact_name: string | null;
  contact_email: string | null;
  contact_phone: string | null;
  actual_conversion: boolean | null;
  conversion_date: string | null;
  conversion_value: number | null;
  conversion_type: string | null;
  utm_source: string | null;
  utm_campaign: string | null;
  utm_medium: string | null;
}

interface LeadsSummary {
  status_breakdown: Record<string, { count: number; avg_score: number }>;
  conversion_stats: {
    total_leads: number;
    tracked_conversions: number;
    conversions: number;
    conversion_rate: number;
    total_value: number;
    avg_value: number;
  };
  utm_sources: Array<{ source: string; leads: number; conversions: number }>;
  period_days: number;
}

export default function LeadsPage() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [summary, setSummary] = useState<LeadsSummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [filters, setFilters] = useState({
    search: '',
    status: '',
    converted: '',
    form_id: ''
  });
  const [selectedLeads, setSelectedLeads] = useState<string[]>([]);
  const [openDropdown, setOpenDropdown] = useState<string | null>(null);
  const [showConversionModal, setShowConversionModal] = useState<string | null>(null);
  const [forms, setForms] = useState<Array<{ id: string; title: string }>>([]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      // Check if click is outside any dropdown
      const target = event.target as HTMLElement;
      const isInsideDropdown = target.closest('.dropdown-container');
      if (!isInsideDropdown) {
        setOpenDropdown(null);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const fetchLeads = async () => {
    try {
      setIsLoading(true);
      const params = new URLSearchParams();
      
      if (filters.status) params.append('status', filters.status);
      if (filters.converted) params.append('converted', filters.converted);
      if (filters.form_id) params.append('form_id', filters.form_id);
      
      const token = localStorage.getItem('admin_token');
      const response = await fetch(buildApiUrl(`/api/admin/leads/?${params}`), {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });
      if (!response.ok) throw new Error('Failed to fetch leads');
      
      const data = await response.json();
      if (data.success) {
        setLeads(data.data.leads);
      }
    } catch (error) {
      console.error('Error fetching leads:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchSummary = async () => {
    try {
      const params = new URLSearchParams();
      if (filters.form_id) params.append('form_id', filters.form_id);
      
      const token = localStorage.getItem('admin_token');
      const response = await fetch(buildApiUrl(`/api/admin/leads/stats/summary?${params}`), {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });
      if (!response.ok) throw new Error('Failed to fetch summary');
      
      const data = await response.json();
      if (data.success) {
        setSummary(data.data);
      }
    } catch (error) {
      console.error('Error fetching summary:', error);
    }
  };

  const fetchForms = async () => {
    try {
      const token = localStorage.getItem('admin_token');
      const response = await fetch(API_ENDPOINTS.FORMS.LIST(), {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Forms fetch error:', response.status, errorText);
        throw new Error(`Failed to fetch forms: ${response.status} ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log('Forms API response:', data);
      
      if (data.success && data.data.forms) {
        setForms(data.data.forms.map((form: any) => ({ id: form.id, title: form.title })));
      } else {
        console.error('Forms API returned unsuccessful response:', data);
        setForms([]);
      }
    } catch (error) {
      console.error('Error fetching forms:', error);
      setForms([]);
    }
  };

  useEffect(() => {
    fetchLeads();
    fetchSummary();
    fetchForms();
  }, [filters]);

  const updateConversion = async (sessionId: string, conversionData: {
    actual_conversion: boolean;
    conversion_date?: string;
    conversion_value?: number;
    conversion_type?: string;
    notes?: string;
  }) => {
    try {
      const token = localStorage.getItem('admin_token');
      const response = await fetch(buildApiUrl(`/api/admin/leads/${sessionId}/conversion`), {
        method: 'PUT',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json' 
        },
        body: JSON.stringify(conversionData)
      });
      
      if (!response.ok) throw new Error('Failed to update conversion');
      
      const data = await response.json();
      if (data.success) {
        // Refresh leads and summary
        fetchLeads();
        fetchSummary();
        setShowConversionModal(null);
      }
    } catch (error) {
      console.error('Error updating conversion:', error);
      alert('Failed to update conversion status');
    }
  };

  const handleQuickConversion = (sessionId: string, converted: boolean) => {
    updateConversion(sessionId, {
      actual_conversion: converted,
      conversion_date: converted ? new Date().toISOString() : undefined,
      conversion_type: converted ? 'quick_mark' : undefined
    });
  };

  const statusColors = {
    yes: 'bg-success-100 text-success-800',
    maybe: 'bg-warning-100 text-warning-800',
    no: 'bg-red-100 text-red-800',
    unknown: 'bg-slate-100 text-slate-800'
  };

  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString();
  };

  const formatCurrency = (value: number | null) => {
    if (!value) return '$0';
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);
  };

  if (isLoading && leads.length === 0) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div className="h-8 bg-slate-200 rounded w-32 animate-pulse"></div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="admin-card animate-pulse">
              <div className="h-6 bg-slate-200 rounded w-1/2 mb-2"></div>
              <div className="h-8 bg-slate-200 rounded w-1/3"></div>
            </div>
          ))}
        </div>
        <div className="space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="admin-card animate-pulse">
              <div className="h-6 bg-slate-200 rounded w-1/3 mb-2"></div>
              <div className="h-4 bg-slate-200 rounded w-2/3"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Leads</h1>
        <p className="mt-1 text-sm text-slate-600">
          Manage and track your lead conversions
        </p>
      </div>

      {/* Summary Stats */}
      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="admin-card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <UsersIcon className="h-6 w-6 text-admin-600" />
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-slate-600">Total Leads</p>
                <p className="text-2xl font-semibold text-slate-900">{summary.conversion_stats.total_leads}</p>
              </div>
            </div>
          </div>

          <div className="admin-card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ArrowTrendingUpIcon className="h-6 w-6 text-success-600" />
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-slate-600">Conversion Rate</p>
                <p className="text-2xl font-semibold text-slate-900">
                  {summary.conversion_stats.conversion_rate.toFixed(1)}%
                </p>
              </div>
            </div>
          </div>

          <div className="admin-card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CheckCircleIcon className="h-6 w-6 text-success-600" />
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-slate-600">Conversions</p>
                <p className="text-2xl font-semibold text-slate-900">{summary.conversion_stats.conversions}</p>
              </div>
            </div>
          </div>

          <div className="admin-card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CurrencyDollarIcon className="h-6 w-6 text-admin-600" />
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-slate-600">Total Value</p>
                <p className="text-2xl font-semibold text-slate-900">
                  {formatCurrency(summary.conversion_stats.total_value)}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="admin-card">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1 relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <MagnifyingGlassIcon className="h-4 w-4 text-slate-400" />
            </div>
            <input
              type="text"
              className="admin-input pl-10"
              placeholder="Search by name, email, or session ID..."
              value={filters.search}
              onChange={(e) => setFilters(prev => ({ ...prev, search: e.target.value }))}
            />
          </div>

          <select
            className="admin-select"
            value={filters.status}
            onChange={(e) => setFilters(prev => ({ ...prev, status: e.target.value }))}
          >
            <option value="">All Status</option>
            <option value="yes">Qualified (Yes)</option>
            <option value="maybe">Maybe</option>
            <option value="no">Not Qualified</option>
            <option value="unknown">Unknown</option>
          </select>

          <select
            className="admin-select"
            value={filters.converted}
            onChange={(e) => setFilters(prev => ({ ...prev, converted: e.target.value }))}
          >
            <option value="">All Conversions</option>
            <option value="true">Converted</option>
            <option value="false">Not Converted</option>
          </select>

          <select
            className="admin-select"
            value={filters.form_id}
            onChange={(e) => setFilters(prev => ({ ...prev, form_id: e.target.value }))}
          >
            <option value="">All Forms</option>
            {forms.map(form => (
              <option key={form.id} value={form.id}>{form.title}</option>
            ))}
          </select>

          <button 
            onClick={() => setFilters({ search: '', status: '', converted: '', form_id: '' })}
            className="admin-btn-secondary"
          >
            Clear
          </button>
        </div>
      </div>

      {/* Leads List */}
      <div className="space-y-4">
        {leads.length === 0 ? (
          <div className="admin-card text-center py-12">
            <UsersIcon className="w-12 h-12 text-slate-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-slate-900 mb-2">No leads found</h3>
            <p className="text-slate-600">
              {Object.values(filters).some(v => v) 
                ? 'No leads match your current filters.' 
                : 'Leads will appear here once users start submitting forms.'}
            </p>
          </div>
        ) : (
          leads.map((lead) => (
            <div key={lead.lead_id} className="admin-card hover:shadow-admin-md transition-shadow">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3">
                    <div className="flex items-center space-x-2">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${statusColors[lead.lead_status]}`}>
                        {lead.lead_status}
                      </span>
                      <span className="text-sm text-slate-500">Score: {lead.final_score}</span>
                    </div>
                    
                    {/* Conversion Status */}
                    <div className="flex items-center space-x-2">
                      {lead.actual_conversion === true && (
                        <span className="inline-flex items-center text-xs text-success-700">
                          <CheckCircleIconSolid className="w-4 h-4 mr-1" />
                          Converted
                        </span>
                      )}
                      {lead.actual_conversion === false && (
                        <span className="inline-flex items-center text-xs text-red-700">
                          <XCircleIconSolid className="w-4 h-4 mr-1" />
                          Not Converted
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="mt-2">
                    <p className="text-lg font-semibold text-slate-900">{lead.form_title}</p>
                    {lead.contact_name && (
                      <p className="text-sm text-slate-600 flex items-center mt-1">
                        <UsersIcon className="w-4 h-4 mr-1" />
                        {lead.contact_name}
                      </p>
                    )}
                    {lead.contact_email && (
                      <p className="text-sm text-slate-600 flex items-center mt-1">
                        <EnvelopeIcon className="w-4 h-4 mr-1" />
                        {lead.contact_email}
                      </p>
                    )}
                    {lead.contact_phone && (
                      <p className="text-sm text-slate-600 flex items-center mt-1">
                        <PhoneIcon className="w-4 h-4 mr-1" />
                        {lead.contact_phone}
                      </p>
                    )}
                  </div>

                  <div className="mt-3 flex items-center space-x-6 text-xs text-slate-500">
                    <span className="flex items-center">
                      <ClockIcon className="w-4 h-4 mr-1" />
                      Started {formatDate(lead.started_at)}
                    </span>
                    {lead.completed_at && (
                      <span>Completed {formatDate(lead.completed_at)}</span>
                    )}
                    {lead.utm_source && (
                      <span>Source: {lead.utm_source}</span>
                    )}
                    {lead.conversion_value && (
                      <span className="text-success-600 font-medium">
                        Value: {formatCurrency(lead.conversion_value)}
                      </span>
                    )}
                  </div>
                </div>

                <div className="ml-4 flex items-center space-x-2">
                  {/* Quick conversion actions */}
                  {lead.actual_conversion === null && (
                    <>
                      <button
                        onClick={() => handleQuickConversion(lead.lead_id, true)}
                        className="admin-btn-sm bg-success-600 text-white hover:bg-success-700"
                        title="Mark as converted"
                      >
                        <CheckCircleIcon className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleQuickConversion(lead.lead_id, false)}
                        className="admin-btn-sm bg-red-600 text-white hover:bg-red-700"
                        title="Mark as not converted"
                      >
                        <XCircleIcon className="w-4 h-4" />
                      </button>
                    </>
                  )}

                  <div className="relative dropdown-container">
                    <button 
                      className="admin-btn-secondary admin-btn-sm"
                      onClick={() => setOpenDropdown(openDropdown === lead.lead_id ? null : lead.lead_id)}
                    >
                      <EllipsisVerticalIcon className="w-4 h-4" />
                    </button>
                    
                    {openDropdown === lead.lead_id && (
                      <div className="absolute right-0 mt-2 w-48 bg-white border border-slate-200 rounded-lg shadow-lg z-10">
                        <div className="py-1">
                          <button
                            onClick={() => {
                              setShowConversionModal(lead.lead_id);
                              setOpenDropdown(null);
                            }}
                            className="flex items-center w-full px-4 py-2 text-sm text-slate-700 hover:bg-slate-50"
                          >
                            <PencilIcon className="w-4 h-4 mr-3" />
                            Update Conversion
                          </button>
                          <button
                            className="flex items-center w-full px-4 py-2 text-sm text-slate-700 hover:bg-slate-50"
                            disabled
                            title="Coming soon"
                          >
                            <EyeIcon className="w-4 h-4 mr-3" />
                            View Details
                          </button>
                          <button
                            className="flex items-center w-full px-4 py-2 text-sm text-slate-700 hover:bg-slate-50"
                            disabled
                            title="Coming soon"
                          >
                            <ChartBarIcon className="w-4 h-4 mr-3" />
                            View Analytics
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Conversion Modal */}
      {showConversionModal && (
        <ConversionModal
          sessionId={showConversionModal}
          lead={leads.find(l => l.lead_id === showConversionModal)!}
          onSave={updateConversion}
          onClose={() => setShowConversionModal(null)}
        />
      )}
    </div>
  );
}

// Conversion Modal Component
interface ConversionModalProps {
  sessionId: string;
  lead: Lead;
  onSave: (sessionId: string, data: any) => void;
  onClose: () => void;
}

function ConversionModal({ sessionId, lead, onSave, onClose }: ConversionModalProps) {
  const [formData, setFormData] = useState({
    actual_conversion: lead.actual_conversion ?? false,
    conversion_date: lead.conversion_date ? lead.conversion_date.split('T')[0] : '',
    conversion_value: lead.conversion_value?.toString() || '',
    conversion_type: lead.conversion_type || '',
    notes: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave(sessionId, {
      actual_conversion: formData.actual_conversion,
      conversion_date: formData.conversion_date || undefined,
      conversion_value: formData.conversion_value ? parseFloat(formData.conversion_value) : undefined,
      conversion_type: formData.conversion_type || undefined,
      notes: formData.notes || undefined
    });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div className="px-6 py-4 border-b border-slate-200">
          <h3 className="text-lg font-semibold text-slate-900">Update Conversion Status</h3>
          <p className="text-sm text-slate-600 mt-1">
            {lead.contact_name || lead.contact_email || `Lead ${sessionId.slice(0, 8)}...`}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="px-6 py-4 space-y-4">
          <div>
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={formData.actual_conversion}
                onChange={(e) => setFormData(prev => ({ ...prev, actual_conversion: e.target.checked }))}
                className="h-4 w-4 text-admin-600 focus:ring-admin-500 border-slate-300 rounded"
              />
              <span className="text-sm font-medium text-slate-700">Lead converted to customer</span>
            </label>
          </div>

          {formData.actual_conversion && (
            <>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Conversion Date
                </label>
                <input
                  type="date"
                  value={formData.conversion_date}
                  onChange={(e) => setFormData(prev => ({ ...prev, conversion_date: e.target.value }))}
                  className="admin-input"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Conversion Value ($)
                </label>
                <input
                  type="number"
                  step="0.01"
                  placeholder="0.00"
                  value={formData.conversion_value}
                  onChange={(e) => setFormData(prev => ({ ...prev, conversion_value: e.target.value }))}
                  className="admin-input"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Conversion Type
                </label>
                <select
                  value={formData.conversion_type}
                  onChange={(e) => setFormData(prev => ({ ...prev, conversion_type: e.target.value }))}
                  className="admin-select"
                >
                  <option value="">Select type...</option>
                  <option value="sale">Sale</option>
                  <option value="subscription">Subscription</option>
                  <option value="consultation">Consultation</option>
                  <option value="contract">Contract</option>
                  <option value="other">Other</option>
                </select>
              </div>
            </>
          )}

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Notes
            </label>
            <textarea
              rows={3}
              placeholder="Add any notes about this conversion..."
              value={formData.notes}
              onChange={(e) => setFormData(prev => ({ ...prev, notes: e.target.value }))}
              className="admin-input"
            />
          </div>

          <div className="flex space-x-3 pt-4">
            <button
              type="submit"
              className="flex-1 admin-btn-primary"
            >
              Save Changes
            </button>
            <button
              type="button"
              onClick={onClose}
              className="flex-1 admin-btn-secondary"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}