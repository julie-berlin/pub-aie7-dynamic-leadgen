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
    <header className="w-full bg-white border-b-2" style={{ borderBottomColor: 'var(--color-text)' }}>
      <div className="container mx-auto p-[10px]">
        <div className="flex items-center justify-center">
          <div className="flex items-center space-x-3">
            {/* Logo - either uploaded logo or default icon */}
            {logoUrl ? (
              <img
                src={logoUrl}
                alt={`${businessName}`}
                className="object-contain max-h-[250px] w-auto"
              />
            ) : (
            <div className="flex flex-col">
              <span className="text-xl font-bold" style={{ color: 'var(--color-primary)' }}>
                {businessName || 'Varyq'}
              </span>
            </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
