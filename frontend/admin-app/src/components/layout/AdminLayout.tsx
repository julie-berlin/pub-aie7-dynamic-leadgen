import { type ReactNode, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  HomeIcon,
  DocumentTextIcon,
  ChartBarIcon,
  CogIcon,
  UserIcon,
  UsersIcon,
  PaintBrushIcon
} from '@heroicons/react/24/outline';
import { useAdminStore } from '../../stores/adminStore';
import Breadcrumb, { useBreadcrumbs } from '../common/Breadcrumb';
import { useBreadcrumbContext } from '../common/BreadcrumbContext';

interface AdminLayoutProps {
  children: ReactNode;
}

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
  { name: 'Forms', href: '/forms', icon: DocumentTextIcon },
  { name: 'Leads', href: '/leads', icon: UsersIcon },
  { name: 'Analytics', href: '/analytics', icon: ChartBarIcon },
  { name: 'Themes', href: '/themes', icon: PaintBrushIcon },
  { name: 'Settings', href: '/settings', icon: CogIcon },
];

export default function AdminLayout({ children }: AdminLayoutProps) {
  const location = useLocation();
  const { user, logout, businessInfo, loadBusinessInfo } = useAdminStore();
  const { customBreadcrumbs } = useBreadcrumbContext();
  const breadcrumbs = useBreadcrumbs(customBreadcrumbs);

  useEffect(() => {
    if (!businessInfo.isLoaded) {
      loadBusinessInfo();
    }
  }, [businessInfo.isLoaded, loadBusinessInfo]);

  return (
    <div className="flex h-screen bg-slate-50">
      {/* Sidebar */}
      <div className="admin-sidebar w-64 flex-shrink-0">
        {/* Logo */}
        <div className="px-6 py-8">
          <h1 className="text-xl font-bold text-slate-900">
            Varyq
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            {!businessInfo.isLoaded ? 'Loading...' : (businessInfo.name || 'Business Admin')}
          </p>
        </div>

        {/* Navigation */}
        <nav className="admin-sidebar-nav">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={
                  isActive
                    ? 'admin-sidebar-nav-item-active'
                    : 'admin-sidebar-nav-item-inactive'
                }
              >
                <item.icon className="w-5 h-5 mr-3" />
                {item.name}
              </Link>
            );
          })}
        </nav>

        {/* User section */}
        <div className="absolute bottom-0 w-64 p-4 border-t border-slate-200 bg-white">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-admin-500 rounded-full flex items-center justify-center">
                <UserIcon className="w-4 h-4 text-white" />
              </div>
            </div>
            <div className="ml-3 flex-1 min-w-0">
              <p className="text-sm font-medium text-slate-900 truncate">
                {user?.name || 'Admin User'}
              </p>
              <p className="text-xs text-slate-500 truncate">
                {user?.email}
              </p>
            </div>
            <button
              onClick={logout}
              className="ml-2 text-slate-400 hover:text-slate-600 transition-colors"
              title="Logout"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-white border-b border-slate-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex flex-col space-y-2">
              <h2 className="text-xl font-semibold text-slate-900">
                {navigation.find(item => item.href === location.pathname)?.name || 'Admin'}
              </h2>
              <Breadcrumb items={breadcrumbs} />
            </div>

            {/* Header actions */}
            <div className="flex items-center space-x-4">
              <div className="text-sm text-slate-500">
                Last updated: {new Date().toLocaleTimeString()}
              </div>
              <div className="w-2 h-2 bg-success-500 rounded-full" title="System healthy" />
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
