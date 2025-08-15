import { ReactNode } from 'react';
import type { TableProps, TableColumn } from '../../types';

interface AdminTableProps<T = any> extends TableProps<T> {
  emptyState?: {
    icon?: ReactNode;
    title: string;
    description?: string;
    action?: ReactNode;
  };
}

export default function Table<T = any>({
  columns,
  data,
  loading = false,
  pagination,
  rowSelection,
  onRow,
  className = '',
  size = 'middle',
  bordered = false,
  showHeader = true,
  scroll,
  emptyState
}: AdminTableProps<T>) {
  const sizeClasses = {
    small: 'text-sm',
    middle: '',
    large: 'text-base'
  };

  const cellPadding = {
    small: 'px-4 py-2',
    middle: 'px-6 py-4',
    large: 'px-6 py-6'
  };

  if (loading) {
    return (
      <div className="admin-card">
        <div className="animate-pulse space-y-4">
          {showHeader && (
            <div className="h-12 bg-slate-200 rounded"></div>
          )}
          {Array.from({ length: 5 }).map((_, i) => (
            <div key={i} className="h-16 bg-slate-100 rounded"></div>
          ))}
        </div>
      </div>
    );
  }

  if (data.length === 0 && emptyState) {
    return (
      <div className="admin-card text-center py-12">
        {emptyState.icon && (
          <div className="mb-4 flex justify-center">
            {emptyState.icon}
          </div>
        )}
        <h3 className="text-lg font-medium text-slate-900 mb-2">
          {emptyState.title}
        </h3>
        {emptyState.description && (
          <p className="text-slate-600 mb-4">
            {emptyState.description}
          </p>
        )}
        {emptyState.action}
      </div>
    );
  }

  return (
    <div className={`admin-card p-0 ${className}`}>
      <div className={scroll ? 'overflow-auto' : ''} style={scroll}>
        <table className={`admin-table ${sizeClasses[size]} ${bordered ? 'border-collapse' : ''}`}>
          {showHeader && (
            <thead className="admin-table-header">
              <tr>
                {rowSelection?.type === 'checkbox' && (
                  <th className={`admin-table-header-cell ${cellPadding[size]}`}>
                    <input
                      type="checkbox"
                      className="rounded border-slate-300 text-admin-600 focus:ring-admin-500"
                      checked={rowSelection.selectedRowKeys.length === data.length}
                      onChange={(e) => {
                        if (e.target.checked) {
                          rowSelection.onChange(
                            data.map((_, index) => index),
                            data
                          );
                        } else {
                          rowSelection.onChange([], []);
                        }
                      }}
                    />
                  </th>
                )}
                {columns.map((column) => (
                  <th
                    key={column.key}
                    className={`admin-table-header-cell ${cellPadding[size]} ${
                      column.align === 'center' ? 'text-center' : 
                      column.align === 'right' ? 'text-right' : 'text-left'
                    }`}
                    style={{ width: column.width }}
                  >
                    {column.title}
                  </th>
                ))}
              </tr>
            </thead>
          )}
          <tbody className="admin-table-body">
            {data.map((record, index) => (
              <tr
                key={index}
                className="admin-table-row"
                {...(onRow ? onRow(record, index) : {})}
              >
                {rowSelection?.type === 'checkbox' && (
                  <td className={`admin-table-cell ${cellPadding[size]}`}>
                    <input
                      type="checkbox"
                      className="rounded border-slate-300 text-admin-600 focus:ring-admin-500"
                      checked={rowSelection.selectedRowKeys.includes(index)}
                      onChange={(e) => {
                        const newSelected = e.target.checked
                          ? [...rowSelection.selectedRowKeys, index]
                          : rowSelection.selectedRowKeys.filter(key => key !== index);
                        const newSelectedRows = newSelected.map(key => data[key as number]);
                        rowSelection.onChange(newSelected, newSelectedRows);
                      }}
                    />
                  </td>
                )}
                {columns.map((column) => {
                  const value = column.dataIndex ? record[column.dataIndex] : record;
                  const renderedValue = column.render 
                    ? column.render(value, record, index)
                    : value;

                  return (
                    <td
                      key={column.key}
                      className={`admin-table-cell ${cellPadding[size]} ${
                        column.align === 'center' ? 'text-center' : 
                        column.align === 'right' ? 'text-right' : 'text-left'
                      }`}
                    >
                      {renderedValue}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {pagination && (
        <div className="px-6 py-4 border-t border-slate-200 flex items-center justify-between">
          <div className="text-sm text-slate-700">
            Showing{' '}
            <span className="font-medium">
              {(pagination.current - 1) * pagination.pageSize + 1}
            </span>{' '}
            to{' '}
            <span className="font-medium">
              {Math.min(pagination.current * pagination.pageSize, pagination.total)}
            </span>{' '}
            of{' '}
            <span className="font-medium">{pagination.total}</span> results
          </div>
          
          <div className="flex items-center space-x-2">
            {pagination.showSizeChanger && (
              <select
                className="admin-select text-sm"
                value={pagination.pageSize}
                onChange={(e) => pagination.onChange(1, Number(e.target.value))}
              >
                <option value={10}>10 per page</option>
                <option value={20}>20 per page</option>
                <option value={50}>50 per page</option>
                <option value={100}>100 per page</option>
              </select>
            )}
            
            <div className="flex space-x-1">
              <button
                onClick={() => pagination.onChange(pagination.current - 1)}
                disabled={pagination.current <= 1}
                className="admin-btn-secondary admin-btn-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              
              {/* Simple pagination - show current page */}
              <span className="px-3 py-1.5 text-sm bg-admin-50 text-admin-600 border border-admin-200 rounded">
                {pagination.current}
              </span>
              
              <button
                onClick={() => pagination.onChange(pagination.current + 1)}
                disabled={pagination.current >= Math.ceil(pagination.total / pagination.pageSize)}
                className="admin-btn-secondary admin-btn-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}