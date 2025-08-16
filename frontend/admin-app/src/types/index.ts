// Re-export store types for convenience
export type { 
  AdminUser, 
  AdminStore 
} from '../stores/adminStore';

export type { 
  AdminForm, 
  FormsStore 
} from '../stores/formsStore';

export type { 
  DashboardMetrics, 
  FormAnalytics, 
  RealTimeMetrics, 
  DateRange, 
  AnalyticsStore 
} from '../stores/analyticsStore';

// Common UI component types
export interface TableColumn<T = any> {
  key: string;
  title: string;
  dataIndex?: keyof T;
  render?: (value: any, record: T, index: number) => React.ReactNode;
  width?: string | number;
  align?: 'left' | 'center' | 'right';
  sortable?: boolean;
  filterable?: boolean;
  fixed?: 'left' | 'right';
}

export interface TableProps<T = any> {
  columns: TableColumn<T>[];
  data: T[];
  loading?: boolean;
  pagination?: {
    current: number;
    pageSize: number;
    total: number;
    onChange: (page: number, pageSize?: number) => void;
    showSizeChanger?: boolean;
  };
  rowSelection?: {
    selectedRowKeys: string[] | number[];
    onChange: (selectedRowKeys: string[] | number[], selectedRows: T[]) => void;
    type?: 'checkbox' | 'radio';
  };
  onRow?: (record: T, index: number) => React.HTMLAttributes<HTMLTableRowElement>;
  className?: string;
  size?: 'small' | 'middle' | 'large';
  bordered?: boolean;
  showHeader?: boolean;
  scroll?: { x?: number; y?: number };
}

// Chart configuration types
export interface ChartConfig {
  type: 'line' | 'bar' | 'pie' | 'doughnut' | 'area';
  data: {
    labels: string[];
    datasets: Array<{
      label: string;
      data: number[];
      backgroundColor?: string | string[];
      borderColor?: string;
      borderWidth?: number;
      fill?: boolean;
    }>;
  };
  options?: {
    responsive?: boolean;
    maintainAspectRatio?: boolean;
    plugins?: {
      legend?: { display: boolean; position?: 'top' | 'bottom' | 'left' | 'right' };
      title?: { display: boolean; text?: string };
    };
    scales?: {
      x?: { display: boolean; title?: { display: boolean; text?: string } };
      y?: { display: boolean; title?: { display: boolean; text?: string } };
    };
  };
}

// Form builder types
export interface FormField {
  id: string;
  type: 'text' | 'textarea' | 'email' | 'phone' | 'number' | 'select' | 'radio' | 'checkbox' | 'rating' | 'date' | 'file';
  label: string;
  description?: string;
  placeholder?: string;
  required: boolean;
  validation?: {
    minLength?: number;
    maxLength?: number;
    min?: number;
    max?: number;
    pattern?: string;
    message?: string;
  };
  options?: Array<{
    id: string;
    label: string;
    value: string;
  }>;
  conditional?: {
    dependsOn: string;
    condition: 'equals' | 'contains' | 'greaterThan' | 'lessThan';
    value: any;
  };
  order: number;
}

export interface FormStep {
  id: string;
  title: string;
  description?: string;
  fields: FormField[];
  order: number;
}

// API response types
export interface ApiResponse<T = any> {
  success: boolean;
  data: T;
  message?: string;
  errors?: Record<string, string[]>;
}

export interface PaginatedResponse<T = any> {
  data: T[];
  pagination: {
    current: number;
    pageSize: number;
    total: number;
    totalPages: number;
  };
}

// Navigation types
export interface NavItem {
  key: string;
  label: string;
  icon?: React.ComponentType<{ className?: string }>;
  path?: string;
  children?: NavItem[];
  badge?: {
    count: number;
    color?: 'red' | 'blue' | 'green' | 'yellow' | 'gray';
  };
}

// Notification types
export interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message?: string;
  duration?: number; // milliseconds, 0 for persistent
  action?: {
    label: string;
    onClick: () => void;
  };
  createdAt: string;
  read: boolean;
}

// Theme types for admin interface
export interface AdminTheme {
  colors: {
    primary: string;
    secondary: string;
    success: string;
    warning: string;
    error: string;
    info: string;
    text: {
      primary: string;
      secondary: string;
      disabled: string;
    };
    background: {
      default: string;
      paper: string;
      elevated: string;
    };
    border: {
      default: string;
      light: string;
      focus: string;
    };
  };
  typography: {
    fontFamily: string;
    fontSize: {
      xs: string;
      sm: string;
      base: string;
      lg: string;
      xl: string;
      '2xl': string;
      '3xl': string;
    };
    fontWeight: {
      normal: number;
      medium: number;
      semibold: number;
      bold: number;
    };
  };
  spacing: {
    xs: string;
    sm: string;
    md: string;
    lg: string;
    xl: string;
    '2xl': string;
  };
  borderRadius: {
    sm: string;
    md: string;
    lg: string;
    full: string;
  };
  shadows: {
    sm: string;
    md: string;
    lg: string;
    xl: string;
  };
}

// Utility types
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

export type RequireAtLeastOne<T, Keys extends keyof T = keyof T> = 
  Pick<T, Exclude<keyof T, Keys>> & 
  { [K in Keys]-?: Required<Pick<T, K>> & Partial<Pick<T, Exclude<Keys, K>>> }[Keys];

export type Prettify<T> = {
  [K in keyof T]: T[K];
} & {};

// Permission types
export type Permission = 
  | 'forms.view'
  | 'forms.create'
  | 'forms.edit'
  | 'forms.delete'
  | 'analytics.view'
  | 'analytics.export'
  | 'users.view'
  | 'users.manage'
  | 'settings.view'
  | 'settings.edit';

export interface Role {
  id: string;
  name: string;
  description: string;
  permissions: Permission[];
  isDefault: boolean;
}

// Export status types
export type ExportStatus = 'pending' | 'processing' | 'completed' | 'failed';

// Form status types
export type FormStatus = 'draft' | 'active' | 'paused' | 'archived';

export interface ExportJob {
  id: string;
  type: 'analytics' | 'forms' | 'responses';
  status: ExportStatus;
  progress: number; // 0-100
  createdAt: string;
  completedAt?: string;
  downloadUrl?: string;
  error?: string;
  parameters: Record<string, any>;
}