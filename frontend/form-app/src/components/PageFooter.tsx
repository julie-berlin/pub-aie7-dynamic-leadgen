/**
 * PageFooter Component
 * 
 * Displays the page footer with branding.
 * Used at the page layout level and consistent across all pages.
 */
export default function PageFooter() {
  return (
    <footer className="w-full p-4 text-center" style={{ backgroundColor: 'var(--color-background-light)' }}>
      <div className="container mx-auto">
        <span className="text-sm" style={{ color: 'var(--color-text-muted)' }}>
          Varyq - Intelligent Leads
        </span>
      </div>
    </footer>
  );
}