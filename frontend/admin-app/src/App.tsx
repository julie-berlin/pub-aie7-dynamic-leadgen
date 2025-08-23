import { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useAdminStore } from './stores/adminStore';
import { useAnalyticsStore } from './stores/analyticsStore';

// Layout components (placeholder imports for now)
import AdminLayout from './components/layout/AdminLayout';
import { BreadcrumbProvider } from './components/common/BreadcrumbContext';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import FormsPage from './pages/FormsPage';
import AnalyticsPage from './pages/AnalyticsPage';
import SettingsPage from './pages/SettingsPage';
import FormDetailPage from './pages/FormDetailPage';
import LeadsPage from './pages/LeadsPage';
import ThemesPage from './pages/ThemesPage';
import ThemeEditorPage from './pages/ThemeEditorPage';

// Create Query Client for data fetching
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      gcTime: 1000 * 60 * 10, // 10 minutes (formerly cacheTime)
      retry: 2,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  const { isAuthenticated, refreshToken } = useAdminStore();
  const { startRealTimeUpdates: startAnalyticsUpdates } = useAnalyticsStore();

  useEffect(() => {
    // Check authentication on app load
    if (localStorage.getItem('admin_token')) {
      refreshToken();
    }
  }, [refreshToken]);

  useEffect(() => {
    // Start real-time updates when authenticated
    if (isAuthenticated) {
      startAnalyticsUpdates();
    }
  }, [isAuthenticated, startAnalyticsUpdates]);

  return (
    <QueryClientProvider client={queryClient}>
      <Router basename="/admin">
        <div className="min-h-screen bg-slate-50">
          {!isAuthenticated ? (
            <Routes>
              <Route path="/login" element={<LoginPage />} />
              <Route path="*" element={<Navigate to="/login" replace />} />
            </Routes>
          ) : (
            <BreadcrumbProvider>
              <AdminLayout>
                <Routes>
                  <Route path="/" element={<Navigate to="/dashboard" replace />} />
                  <Route path="/dashboard" element={<DashboardPage />} />
                  <Route path="/forms" element={<FormsPage />} />
                  <Route path="/forms/:id" element={<FormDetailPage />} />
                  <Route path="/leads" element={<LeadsPage />} />
                  <Route path="/analytics" element={<AnalyticsPage />} />
                  <Route path="/themes" element={<ThemesPage />} />
                  <Route path="/themes/new" element={<ThemeEditorPage />} />
                  <Route path="/themes/:id/edit" element={<ThemeEditorPage />} />
                  <Route path="/settings" element={<SettingsPage />} />
                  <Route path="/login" element={<Navigate to="/dashboard" replace />} />
                  <Route path="*" element={<Navigate to="/dashboard" replace />} />
                </Routes>
              </AdminLayout>
            </BreadcrumbProvider>
          )}
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;