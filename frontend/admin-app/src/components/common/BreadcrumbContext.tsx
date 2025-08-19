import { createContext, useContext, useState, type ReactNode } from 'react';
import type { BreadcrumbItem } from './Breadcrumb';

interface BreadcrumbContextType {
  customBreadcrumbs: BreadcrumbItem[] | undefined;
  setCustomBreadcrumbs: (breadcrumbs: BreadcrumbItem[] | undefined) => void;
}

const BreadcrumbContext = createContext<BreadcrumbContextType | undefined>(undefined);

export function BreadcrumbProvider({ children }: { children: ReactNode }) {
  const [customBreadcrumbs, setCustomBreadcrumbs] = useState<BreadcrumbItem[] | undefined>(undefined);

  return (
    <BreadcrumbContext.Provider value={{ customBreadcrumbs, setCustomBreadcrumbs }}>
      {children}
    </BreadcrumbContext.Provider>
  );
}

export function useBreadcrumbContext() {
  const context = useContext(BreadcrumbContext);
  if (context === undefined) {
    throw new Error('useBreadcrumbContext must be used within a BreadcrumbProvider');
  }
  return context;
}