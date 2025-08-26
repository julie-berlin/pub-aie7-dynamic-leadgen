/**
 * PageFooter Component
 *
 * Displays the page footer with branding.
 * Used at the page layout level and consistent across all pages.
 */
export default function PageFooter() {
  return (
    <footer className="w-full" style={{ color: 'var(--color-background-light' }}>
      <div className="container mx-auto p-4 text-center">
        <p className="text-xs" style={{ color: 'var(--color-text-light' }}>Varyq - Intelligent Leads</p>
      </div>
    </footer>
  );
}
