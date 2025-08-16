import { ReactNode } from 'react';
import PageHeader from './PageHeader';
import PageFooter from './PageFooter';

interface PageLayoutProps {
  children: ReactNode;
  businessName?: string;
  logoUrl?: string;
}

/**
 * PageLayout Component
 * 
 * Provides the shared layout structure for all pages in the app.
 * Includes consistent header and footer across all pages.
 */
export default function PageLayout({ children, businessName, logoUrl }: PageLayoutProps) {
  return (
    <div className="min-h-screen bg-gray-200 flex flex-col">
      {/* Page Header with Logo */}
      <PageHeader 
        businessName={businessName}
        logoUrl={logoUrl}
      />

      {/* Main Content */}
      <main className="flex-1 py-8 px-4">
        <div className="container mx-auto max-w-4xl">
          <div className="bg-white rounded-2xl" style={{ padding: 'var(--spacing-page)' }}>
            {children}
          </div>
        </div>
      </main>

      {/* Page Footer */}
      <PageFooter />
    </div>
  );
}