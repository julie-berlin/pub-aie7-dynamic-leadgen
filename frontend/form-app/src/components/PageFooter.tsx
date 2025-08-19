/**
 * PageFooter Component
 *
 * Displays the page footer with branding.
 * Used at the page layout level and consistent across all pages.
 */
export default function PageFooter() {
  return (
    <footer className="w-full" style={{ backgroundColor: 'var(--color-background-light)' }}>
      <div className="container mx-auto p-4 text-center">
        <p className="text-sm" style={{ color: 'var(--color-text-muted)' }}>Varyq - Intelligent Leads</p>
      </div>
    </footer>
  );
}
