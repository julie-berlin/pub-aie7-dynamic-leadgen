import { ReactNode } from 'react';

interface SimpleLayoutProps {
  children: ReactNode;
}

/**
 * SimpleLayout Component
 * 
 * Provides a simple, non-branded layout for error pages and other non-branded content.
 * No header or footer, just centered content on a clean background.
 */
export default function SimpleLayout({ children }: SimpleLayoutProps) {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {children}
      </div>
    </div>
  );
}