import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Suspense, lazy, useEffect } from 'react';
import { useAdminStore } from './stores/adminStore';
import { LoadingSpinner } from './components/ui';

// Layout components (placeholder imports for now)
import AdminLayout from './components/layout/AdminLayout';
import { BreadcrumbProvider } from './components/common/BreadcrumbContext';

// Always load LoginPage immediately since it's needed for unauthenticated users
import LoginPage from './pages/LoginPage';

// Lazy load authenticated pages to prevent loading on login page
const DashboardPage = lazy(() => import('./pages/DashboardPage'));
const FormsPage = lazy(() => import('./pages/FormsPage'));
const AnalyticsPage = lazy(() => import('./pages/AnalyticsPage'));
const SettingsPage = lazy(() => import('./pages/SettingsPage'));
const FormDetailPage = lazy(() => import('./pages/FormDetailPage'));
const LeadsPage = lazy(() => import('./pages/LeadsPage'));
const ThemesPage = lazy(() => import('./pages/ThemesPage'));
const ThemeEditorPage = lazy(() => import('./pages/ThemeEditorPage'));

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
  const { isAuthenticated, isInitialized, initializeAuth } = useAdminStore();

  // Initialize authentication on app startup
  useEffect(() => {
    initializeAuth();
  }, [initializeAuth]);

  // Show loading spinner while determining auth state
  if (!isInitialized) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="text-center">
          <LoadingSpinner />
          <p className="mt-2 text-sm text-slate-600">Initializing...</p>
        </div>
      </div>
    );
  }

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
                <Suspense fallback={<div className="flex justify-center items-center min-h-64"><LoadingSpinner /></div>}>
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
                </Suspense>
              </AdminLayout>
            </BreadcrumbProvider>
          )}
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;