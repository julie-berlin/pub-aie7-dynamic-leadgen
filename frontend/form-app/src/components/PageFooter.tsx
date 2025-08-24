/**
 * PageFooter Component
 *
 * Displays the page footer with branding.
 * Used at the page layout level and consistent across all pages.
 */
export default function PageFooter() {
  return (
    <footer className="w-full bg-neutral-100">
      <div className="container mx-auto p-4 text-center">
        <p className="text-sm text-neutral-400">Varyq - Intelligent Leads</p>
      </div>
    </footer>
  );
}
