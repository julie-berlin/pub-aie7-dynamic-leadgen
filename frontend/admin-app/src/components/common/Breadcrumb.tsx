import { Fragment } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ChevronRightIcon, HomeIcon } from '@heroicons/react/24/outline';

export interface BreadcrumbItem {
  label: string;
  href?: string;
  icon?: React.ComponentType<{ className?: string }>;
  current?: boolean;
}

interface BreadcrumbProps {
  items: BreadcrumbItem[];
  showHome?: boolean;
}

export default function Breadcrumb({ items, showHome = true }: BreadcrumbProps) {
  const location = useLocation();

  // Build breadcrumb items with home
  const breadcrumbItems = showHome
    ? [
        {
          label: 'Dashboard',
          href: '/dashboard',
          icon: HomeIcon,
          current: location.pathname === '/dashboard'
        },
        ...items
      ]
    : items;

  return (
    <nav className="flex" aria-label="Breadcrumb">
      <ol className="flex items-center space-x-2">
        {breadcrumbItems.map((item, index) => (
          <li key={index} className="flex items-center">
            {/* Separator */}
            {index > 0 && (
              <ChevronRightIcon className="w-4 h-4 text-slate-400 mx-2" />
            )}
            
            {/* Breadcrumb item */}
            <div className="flex items-center">
              {item.current || !item.href ? (
                <span className="flex items-center text-sm font-medium text-slate-500">
                  {item.icon && (
                    <item.icon className="w-4 h-4 mr-1.5" />
                  )}
                  {item.label}
                </span>
              ) : (
                <Link
                  to={item.href}
                  className="flex items-center text-sm font-medium text-slate-700 hover:text-admin-600 transition-colors"
                >
                  {item.icon && (
                    <item.icon className="w-4 h-4 mr-1.5" />
                  )}
                  {item.label}
                </Link>
              )}
            </div>
          </li>
        ))}
      </ol>
    </nav>
  );
}

/**
 * Hook to generate breadcrumbs based on current route
 */
export function useBreadcrumbs(customBreadcrumbs?: BreadcrumbItem[]): BreadcrumbItem[] {
  const location = useLocation();
  const pathSegments = location.pathname.split('/').filter(Boolean);

  // If custom breadcrumbs provided, use them
  if (customBreadcrumbs) {
    return customBreadcrumbs;
  }

  const breadcrumbs: BreadcrumbItem[] = [];

  // Generate breadcrumbs based on route
  if (pathSegments.length === 0 || pathSegments[0] === 'dashboard') {
    return [{ label: 'Dashboard', href: '/dashboard', current: true }];
  }

  switch (pathSegments[0]) {
    case 'forms':
      breadcrumbs.push({
        label: 'Forms',
        href: '/forms',
        current: pathSegments.length === 1
      });

      if (pathSegments.length > 1) {
        // Form detail page
        const formId = pathSegments[1];
        breadcrumbs.push({
          label: 'Form Details',
          current: true
        });
      }
      break;

    case 'analytics':
      breadcrumbs.push({
        label: 'Analytics',
        href: '/analytics',
        current: true
      });
      break;

    case 'settings':
      breadcrumbs.push({
        label: 'Company Settings',
        href: '/settings',
        current: true
      });
      break;

    default:
      breadcrumbs.push({
        label: 'Page',
        current: true
      });
  }

  return breadcrumbs;
}

/**
 * Helper function to create form detail breadcrumbs
 */
export function createFormDetailBreadcrumbs(formTitle?: string): BreadcrumbItem[] {
  return [
    {
      label: 'Forms',
      href: '/forms'
    },
    {
      label: formTitle || 'Form Details',
      current: true
    }
  ];
}