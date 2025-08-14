# Dynamic Surveys Admin App

Admin frontend for the Dynamic Lead Generation Platform built with React + TypeScript + Vite.

## Overview

This is the admin interface for managing forms, analytics, and client data for the Dynamic Lead Generation Platform. It provides a comprehensive dashboard for business users to:

- Create and manage lead generation forms
- View detailed analytics and performance metrics
- Configure themes and branding
- Manage business settings and team members
- Monitor real-time form activity

## Development Setup

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Backend API running on port 8000

### Installation
```bash
npm install
```

### Development Server
```bash
npm run dev
```
The admin app will be available at: **http://localhost:5174/admin/**

### Build for Production
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```
Preview will be available at: **http://localhost:4174/admin/**

## Architecture

### Routing
- **Base Path**: `/admin/` - All admin routes are prefixed with `/admin` to avoid conflicts with the main form application
- **Port**: 5174 (development) / 4174 (preview) - Different from form app to prevent port conflicts

### Key Features
- **Authentication**: JWT-based admin authentication
- **State Management**: Zustand stores for admin, forms, and analytics data
- **Data Fetching**: React Query for server state management
- **Styling**: TailwindCSS v4 with custom admin design system
- **Charts**: Recharts for analytics visualizations
- **Forms**: React Hook Form with Zod validation

### API Integration
The admin app connects to backend APIs at:
- `POST /api/admin/auth/login` - Admin authentication
- `GET /api/admin/forms` - Form management
- `GET /api/admin/analytics/dashboard` - Dashboard metrics
- `GET /api/admin/themes` - Theme management
- `GET /api/admin/business/info` - Business settings

### Project Structure
```
src/
├── components/          # Reusable UI components
│   ├── charts/         # Chart components for analytics
│   ├── common/         # Shared components
│   ├── dashboard/      # Dashboard-specific components
│   ├── forms/          # Form management components
│   ├── layout/         # Layout components
│   └── tables/         # Data table components
├── hooks/              # Custom React hooks
├── pages/              # Main page components
│   ├── DashboardPage.tsx
│   ├── FormsPage.tsx
│   ├── AnalyticsPage.tsx
│   └── LoginPage.tsx
├── services/           # API service functions
├── stores/             # Zustand state stores
│   ├── adminStore.ts
│   ├── formsStore.ts
│   └── analyticsStore.ts
├── types/              # TypeScript type definitions
└── utils/              # Utility functions
```

## Technology Stack

- **Framework**: React 19.1.1
- **Language**: TypeScript 5.8+
- **Build Tool**: Vite 7.1.2
- **Styling**: TailwindCSS v4 with custom admin design system
- **State Management**: Zustand 5.0.7
- **Data Fetching**: React Query 5.85.3
- **Forms**: React Hook Form 7.62.0 + Zod 4.0.17
- **Charts**: Recharts 3.1.2
- **Icons**: Heroicons 2.2.0
- **UI Components**: Headless UI 2.2.7

## Design System

The admin app uses a custom design system optimized for data management:

### Colors
- **Primary**: Blue palette (`admin-*`) for primary actions and branding
- **Success**: Green palette for positive states and success messages
- **Warning**: Orange palette for warnings and caution states  
- **Danger**: Red palette for errors and destructive actions
- **Neutral**: Slate palette for text, borders, and backgrounds

### Components
The app uses standard Tailwind classes instead of custom component classes for better maintainability with TailwindCSS v4.

## Development Guidelines

### Adding New Features
1. Create components in appropriate subdirectory
2. Use TypeScript interfaces for all props and data structures
3. Implement proper error handling and loading states
4. Follow the existing design patterns and styling conventions
5. Add appropriate tests for complex logic

### API Integration
- Use React Query for all server state management
- Implement proper error handling for API calls
- Use TypeScript interfaces for API responses
- Handle authentication and authorization properly

### Styling
- Use standard TailwindCSS classes
- Follow the custom color palette defined in index.css
- Ensure responsive design for all components
- Maintain consistency with the admin design system

## Deployment

The admin app is designed to be served under the `/admin` path of the main application server. In production:

1. Build the app: `npm run build`
2. Serve the `dist/` folder under the `/admin` route of your web server
3. Ensure the backend APIs are accessible at `/api/admin/*`

## Authentication

The admin app uses JWT-based authentication:
- Login credentials are sent to `/api/admin/auth/login`
- JWT tokens are stored in localStorage
- Tokens are automatically refreshed when needed
- Unauthenticated users are redirected to `/admin/login`

## Demo Credentials
For development/demo purposes:
- **Email**: admin@example.com
- **Password**: password