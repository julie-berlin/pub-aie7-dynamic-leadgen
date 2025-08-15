import { useEffect, useState } from 'react';
import { 
  CalendarIcon,
  ChartBarIcon,
  EyeIcon,
  UsersIcon,
  ArrowTrendingUpIcon
} from '@heroicons/react/24/outline';
import { useAnalyticsStore } from '../stores/analyticsStore';
import { useFormsStore } from '../stores/formsStore';

export default function AnalyticsPage() {
  const {
    dashboardMetrics,
    dateRange,
    setDateRange,
    fetchDashboardMetrics,
    exportAnalytics,
    isLoading,
  } = useAnalyticsStore();
  
  const {
    forms,
    fetchForms,
    isLoading: formsLoading,
  } = useFormsStore();

  const [selectedPreset, setSelectedPreset] = useState<string>(dateRange.preset || 'last30days');

  useEffect(() => {
    fetchDashboardMetrics();
    fetchForms();
  }, [fetchDashboardMetrics, fetchForms]);

  const handlePresetChange = (preset: string) => {
    setSelectedPreset(preset);
    
    let newDateRange;
    const now = new Date();
    
    switch (preset) {
      case 'today':
        newDateRange = {
          start: now.toISOString().split('T')[0],
          end: now.toISOString().split('T')[0],
          preset: 'today' as const,
        };
        break;
      case 'yesterday':
        const yesterday = new Date(now.getTime() - 24 * 60 * 60 * 1000);
        newDateRange = {
          start: yesterday.toISOString().split('T')[0],
          end: yesterday.toISOString().split('T')[0],
          preset: 'yesterday' as const,
        };
        break;
      case 'last7days':
        newDateRange = {
          start: new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          end: now.toISOString().split('T')[0],
          preset: 'last7days' as const,
        };
        break;
      case 'last30days':
      default:
        newDateRange = {
          start: new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          end: now.toISOString().split('T')[0],
          preset: 'last30days' as const,
        };
        break;
    }
    
    setDateRange(newDateRange);
  };

  const handleExport = async (format: 'csv' | 'xlsx' | 'pdf') => {
    await exportAnalytics(undefined, format);
  };

  if (isLoading && !dashboardMetrics) {
    return (
      <div className="space-y-6">
        {/* Loading skeleton */}
        <div className="flex justify-between items-center">
          <div className="h-8 bg-slate-200 rounded w-32 animate-pulse"></div>
          <div className="flex space-x-2">
            <div className="h-10 bg-slate-200 rounded w-32 animate-pulse"></div>
            <div className="h-10 bg-slate-200 rounded w-24 animate-pulse"></div>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="admin-card animate-pulse">
              <div className="h-4 bg-slate-200 rounded w-1/2 mb-2"></div>
              <div className="h-8 bg-slate-200 rounded w-3/4 mb-2"></div>
              <div className="h-3 bg-slate-200 rounded w-1/4"></div>
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
          <h1 className="text-2xl font-bold text-slate-900">Analytics</h1>
          <p className="mt-1 text-sm text-slate-600">
            Detailed insights and performance metrics for your forms
          </p>
        </div>
        <div className="flex space-x-3">
          {/* Date range selector */}
          <div className="flex items-center space-x-2">
            <CalendarIcon className="w-4 h-4 text-slate-400" />
            <select
              className="admin-select"
              value={selectedPreset}
              onChange={(e) => handlePresetChange(e.target.value)}
            >
              <option value="today">Today</option>
              <option value="yesterday">Yesterday</option>
              <option value="last7days">Last 7 days</option>
              <option value="last30days">Last 30 days</option>
            </select>
          </div>

          {/* Export dropdown */}
          <div className="relative">
            <select
              className="admin-select"
              onChange={(e) => e.target.value && handleExport(e.target.value as any)}
              value=""
            >
              <option value="">Export</option>
              <option value="csv">Export as CSV</option>
              <option value="xlsx">Export as Excel</option>
              <option value="pdf">Export as PDF</option>
            </select>
          </div>
        </div>
      </div>

      {/* Key metrics */}
      {dashboardMetrics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="admin-metric">
            <div className="flex items-center justify-between">
              <div>
                <p className="admin-metric-label">Total Views</p>
                <p className="admin-metric-value">{(dashboardMetrics.totalViews || 0).toLocaleString()}</p>
                <p className="admin-metric-change-positive">+12% vs previous period</p>
              </div>
              <EyeIcon className="w-8 h-8 text-slate-400" />
            </div>
          </div>

          <div className="admin-metric">
            <div className="flex items-center justify-between">
              <div>
                <p className="admin-metric-label">Total Responses</p>
                <p className="admin-metric-value">{(dashboardMetrics.totalResponses || 0).toLocaleString()}</p>
                <p className="admin-metric-change-positive">+18% vs previous period</p>
              </div>
              <UsersIcon className="w-8 h-8 text-slate-400" />
            </div>
          </div>

          <div className="admin-metric">
            <div className="flex items-center justify-between">
              <div>
                <p className="admin-metric-label">Response Rate</p>
                <p className="admin-metric-value">{((dashboardMetrics.responseRate || 0) * 100).toFixed(1)}%</p>
                <p className="admin-metric-change-positive">+5.2% vs previous period</p>
              </div>
              <ArrowTrendingUpIcon className="w-8 h-8 text-slate-400" />
            </div>
          </div>

          <div className="admin-metric">
            <div className="flex items-center justify-between">
              <div>
                <p className="admin-metric-label">Avg Completion</p>
                <p className="admin-metric-value">{Math.round((dashboardMetrics.averageCompletionTime || 0) / 60)}m</p>
                <p className="admin-metric-change-positive">-8% vs previous period</p>
              </div>
              <ChartBarIcon className="w-8 h-8 text-slate-400" />
            </div>
          </div>
        </div>
      )}

      {/* Charts placeholder */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="admin-card">
          <div className="admin-card-header">
            <h3 className="admin-card-title">Response Trends</h3>
            <p className="admin-card-subtitle">Daily form responses over time</p>
          </div>
          <div className="h-64 bg-slate-50 rounded flex items-center justify-center">
            <div className="text-center">
              <ChartBarIcon className="w-12 h-12 text-slate-400 mx-auto mb-2" />
              <p className="text-sm text-slate-500">Chart visualization would appear here</p>
              <p className="text-xs text-slate-400 mt-1">Line chart showing daily trends</p>
            </div>
          </div>
        </div>

        <div className="admin-card">
          <div className="admin-card-header">
            <h3 className="admin-card-title">Conversion Funnel</h3>
            <p className="admin-card-subtitle">User journey from view to completion</p>
          </div>
          <div className="h-64 bg-slate-50 rounded flex items-center justify-center">
            <div className="text-center">
              <ArrowTrendingUpIcon className="w-12 h-12 text-slate-400 mx-auto mb-2" />
              <p className="text-sm text-slate-500">Funnel visualization would appear here</p>
              <p className="text-xs text-slate-400 mt-1">Step-by-step conversion rates</p>
            </div>
          </div>
        </div>
      </div>

      {/* Top forms performance */}
      <div className="admin-card">
        <div className="admin-card-header">
          <h3 className="admin-card-title">Form Performance</h3>
          <p className="admin-card-subtitle">Your best and worst performing forms</p>
        </div>
        <div className="overflow-hidden">
          <table className="admin-table">
            <thead className="admin-table-header">
              <tr>
                <th className="admin-table-header-cell">Form Name</th>
                <th className="admin-table-header-cell">Views</th>
                <th className="admin-table-header-cell">Responses</th>
                <th className="admin-table-header-cell">Conversion Rate</th>
                <th className="admin-table-header-cell">Avg. Time</th>
                <th className="admin-table-header-cell">Status</th>
              </tr>
            </thead>
            <tbody className="admin-table-body">
              {forms.length === 0 ? (
                <tr className="admin-table-row">
                  <td colSpan={6} className="admin-table-cell text-center py-8 text-slate-500">
                    {formsLoading ? 'Loading forms...' : 'No forms found'}
                  </td>
                </tr>
              ) : (
                forms.map((form) => (
                  <tr key={form.id} className="admin-table-row">
                    <td className="admin-table-cell font-medium">{form.title}</td>
                    <td className="admin-table-cell">
                      {form.conversionRate > 0 
                        ? Math.floor(form.totalResponses / form.conversionRate).toLocaleString()
                        : (form.totalResponses + 120).toLocaleString()
                      }
                    </td>
                    <td className="admin-table-cell">{form.totalResponses.toLocaleString()}</td>
                    <td className="admin-table-cell">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        form.conversionRate >= 0.3 ? 'bg-success-100 text-success-800' :
                        form.conversionRate >= 0.2 ? 'bg-warning-100 text-warning-800' :
                        'bg-danger-100 text-danger-800'
                      }`}>
                        {(form.conversionRate * 100).toFixed(1)}%
                      </span>
                    </td>
                    <td className="admin-table-cell">{Math.round((form.averageCompletionTime || 0) / 60)}m</td>
                    <td className="admin-table-cell">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        form.status === 'active' ? 'bg-success-100 text-success-800' :
                        form.status === 'paused' ? 'bg-warning-100 text-warning-800' :
                        'bg-slate-100 text-slate-800'
                      }`}>
                        {form.status}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Insights and recommendations */}
      <div className="admin-card">
        <div className="admin-card-header">
          <h3 className="admin-card-title">Insights & Recommendations</h3>
          <p className="admin-card-subtitle">AI-powered suggestions to improve your forms</p>
        </div>
        <div className="space-y-4">
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0 w-2 h-2 bg-success-500 rounded-full mt-2"></div>
            <div>
              <h4 className="text-sm font-medium text-slate-900">High Converting Forms</h4>
              <p className="text-sm text-slate-600">Your tech consultation form has a 37% conversion rate - 23% above average. Consider using similar question patterns in other forms.</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0 w-2 h-2 bg-warning-500 rounded-full mt-2"></div>
            <div>
              <h4 className="text-sm font-medium text-slate-900">Optimization Opportunity</h4>
              <p className="text-sm text-slate-600">The workshop registration form takes 7 minutes on average to complete. Consider reducing the number of required fields to improve completion rates.</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0 w-2 h-2 bg-admin-500 rounded-full mt-2"></div>
            <div>
              <h4 className="text-sm font-medium text-slate-900">Mobile Performance</h4>
              <p className="text-sm text-slate-600">Mobile users have a 15% higher abandonment rate. Review form layouts for mobile optimization.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}