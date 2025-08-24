import { useEffect } from 'react';
import { 
  DocumentTextIcon, 
  EyeIcon, 
  UsersIcon, 
  ArrowTrendingUpIcon,
  ChartBarIcon,
  ClockIcon
} from '@heroicons/react/24/outline';
import { useAnalyticsStore } from '../stores/analyticsStore';

export default function DashboardPage() {
  const { 
    dashboardMetrics, 
    realTimeMetrics, 
    fetchDashboardMetrics, 
    fetchRealTimeMetrics,
    isLoading 
  } = useAnalyticsStore();

  useEffect(() => {
    // Auth is guaranteed to be ready when this component renders
    fetchDashboardMetrics();
    fetchRealTimeMetrics();
  }, [fetchDashboardMetrics, fetchRealTimeMetrics]);

  const metrics = dashboardMetrics ? [
    {
      title: 'Total Forms',
      value: dashboardMetrics.totalForms.toLocaleString(),
      change: '+12%',
      changeType: 'positive' as const,
      icon: DocumentTextIcon,
    },
    {
      title: 'Active Forms',
      value: dashboardMetrics.activeForms.toLocaleString(),
      change: '+8%',
      changeType: 'positive' as const,
      icon: EyeIcon,
    },
    {
      title: 'Total Responses',
      value: dashboardMetrics.totalResponses.toLocaleString(),
      change: '+23%',
      changeType: 'positive' as const,
      icon: UsersIcon,
    },
    {
      title: 'Avg Conversion Rate',
      value: `${(dashboardMetrics.averageConversionRate * 100).toFixed(1)}%`,
      change: '+5.2%',
      changeType: 'positive' as const,
      icon: ArrowTrendingUpIcon,
    },
    {
      title: 'Total Views',
      value: dashboardMetrics.totalViews.toLocaleString(),
      change: '+18%',
      changeType: 'positive' as const,
      icon: ChartBarIcon,
    },
    {
      title: 'Avg Completion Time',
      value: `${Math.round(dashboardMetrics.averageCompletionTime / 60)}m`,
      change: '-2.1%',
      changeType: 'positive' as const,
      icon: ClockIcon,
    },
  ] : [];

  if (isLoading && !dashboardMetrics) {
    return (
      <div className="space-y-6">
        {/* Loading skeleton */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(6)].map((_, i) => (
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
      {/* Welcome section */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
        <p className="mt-1 text-sm text-slate-600">
          Welcome back! Here's what's happening with your forms today.
        </p>
      </div>

      {/* Key metrics grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {metrics.map((metric) => (
          <div key={metric.title} className="admin-metric">
            <div className="flex items-center justify-between">
              <div>
                <p className="admin-metric-label">{metric.title}</p>
                <p className="admin-metric-value">{metric.value}</p>
                <p className={`admin-metric-change-${metric.changeType}`}>
                  {metric.change} from last month
                </p>
              </div>
              <div className="ml-4">
                <metric.icon className="w-8 h-8 text-slate-400" />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Real-time activity */}
      {realTimeMetrics && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Active users */}
          <div className="admin-card">
            <div className="admin-card-header">
              <h3 className="admin-card-title">Real-time Activity</h3>
              <p className="admin-card-subtitle">Currently active users and sessions</p>
            </div>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-slate-600">Active Users</span>
                <span className="text-lg font-semibold text-slate-900">
                  {realTimeMetrics.activeUsers}
                </span>
              </div>
              <div className="space-y-2">
                {realTimeMetrics.activeForms.map((form) => (
                  <div key={form.formId} className="flex items-center justify-between text-sm">
                    <span className="text-slate-600 truncate">{form.formTitle}</span>
                    <div className="flex items-center space-x-2 text-slate-500">
                      <span>{form.activeUsers} users</span>
                      <span>•</span>
                      <span>{form.responsesInLastHour} responses/hr</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* System health */}
          <div className="admin-card">
            <div className="admin-card-header">
              <h3 className="admin-card-title">System Health</h3>
              <p className="admin-card-subtitle">Performance metrics and status</p>
            </div>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-slate-600">Status</span>
                <div className="flex items-center">
                  <div className={`w-2 h-2 rounded-full mr-2 ${
                    realTimeMetrics.systemHealth.status === 'healthy' 
                      ? 'bg-success-500' 
                      : realTimeMetrics.systemHealth.status === 'warning'
                      ? 'bg-warning-500'
                      : 'bg-danger-500'
                  }`} />
                  <span className="text-sm font-medium capitalize">
                    {realTimeMetrics.systemHealth.status}
                  </span>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-slate-600">API Response</span>
                  <p className="font-semibold">{realTimeMetrics.systemHealth.apiResponseTime}ms</p>
                </div>
                <div>
                  <span className="text-slate-600">DB Response</span>
                  <p className="font-semibold">{realTimeMetrics.systemHealth.dbResponseTime}ms</p>
                </div>
                <div>
                  <span className="text-slate-600">Error Rate</span>
                  <p className="font-semibold">{(realTimeMetrics.systemHealth.errorRate * 100).toFixed(2)}%</p>
                </div>
                <div>
                  <span className="text-slate-600">Uptime</span>
                  <p className="font-semibold text-success-600">99.9%</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Top performing form */}
      {dashboardMetrics?.topPerformingForm && (
        <div className="admin-card">
          <div className="admin-card-header">
            <h3 className="admin-card-title">Top Performing Form</h3>
            <p className="admin-card-subtitle">Your best converting form this month</p>
          </div>
          <div className="flex items-center justify-between">
            <div>
              <h4 className="text-lg font-semibold text-slate-900">
                {dashboardMetrics.topPerformingForm.title}
              </h4>
              <p className="text-sm text-slate-600 mt-1">
                Form ID: {dashboardMetrics.topPerformingForm.id}
              </p>
            </div>
            <div className="text-right">
              <p className="text-2xl font-bold text-success-600">
                {(dashboardMetrics.topPerformingForm.conversionRate * 100).toFixed(1)}%
              </p>
              <p className="text-sm text-slate-500">conversion rate</p>
            </div>
          </div>
        </div>
      )}

      {/* Quick actions */}
      <div className="admin-card">
        <div className="admin-card-header">
          <h3 className="admin-card-title">Quick Actions</h3>
          <p className="admin-card-subtitle">Common tasks and shortcuts</p>
        </div>
        <div className="flex flex-wrap gap-3">
          <button className="admin-btn-primary admin-btn-sm">
            Create New Form
          </button>
          <button className="admin-btn-secondary admin-btn-sm">
            Export Analytics
          </button>
          <button className="admin-btn-secondary admin-btn-sm">
            View All Forms
          </button>
          <button className="admin-btn-secondary admin-btn-sm">
            System Settings
          </button>
        </div>
      </div>
    </div>
  );
}