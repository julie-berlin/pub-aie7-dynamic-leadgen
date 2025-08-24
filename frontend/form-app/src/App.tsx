import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import FormPage from './pages/FormPage';
import CompletionPage from './pages/CompletionPage';
import ErrorPage from './pages/ErrorPage';
import NotFoundPage from './pages/NotFoundPage';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background">
        <Routes>
          {/* Main form route */}
          <Route path="/form/:formId" element={<FormPage />} />
          
          {/* Form completion route */}
          <Route path="/form/:formId/complete" element={<CompletionPage />} />
          
          {/* Error page */}
          <Route path="/error" element={<ErrorPage />} />
          
          {/* 404 page */}
          <Route path="/404" element={<NotFoundPage />} />
          
          {/* Root redirect to 404 */}
          <Route path="/" element={<Navigate to="/404" replace />} />
          
          {/* Catch all other routes */}
          <Route path="*" element={<Navigate to="/404" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App
