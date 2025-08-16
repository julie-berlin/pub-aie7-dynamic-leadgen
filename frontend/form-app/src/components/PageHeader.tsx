interface PageHeaderProps {
  businessName?: string;
  logoUrl?: string;
}

/**
 * PageHeader Component
 *
 * Displays the page header with logo and business name.
 * Used at the page composition level, replacing the existing header with TODO logo comment.
 */
export default function PageHeader({ businessName, logoUrl }: PageHeaderProps) {
  return (
    <header className="w-full" style={{ backgroundColor: 'var(--color-background-light)' }}>
      <div className="container mx-auto p-[30px]">
        <div className="flex items-center justify-center">
          <div className="flex items-center space-x-3">
            {/* Logo - either uploaded logo or default icon */}
            {logoUrl ? (
              <img
                src={logoUrl}
                alt={`${businessName} logo`}
                className="w-12 h-12 rounded-xl object-cover"
              />
            ) : (
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
            )}

            {/* Business Name */}
            <div className="flex flex-col">
              <span className="text-xl font-bold text-gray-900">
                {businessName || 'Varyq'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
