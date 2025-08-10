/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // Custom CSS properties for dynamic theming
      colors: {
        'primary': 'var(--color-primary)',
        'primary-hover': 'var(--color-primary-hover)',
        'primary-light': 'var(--color-primary-light)',
        'secondary': 'var(--color-secondary)',
        'secondary-hover': 'var(--color-secondary-hover)',
        'secondary-light': 'var(--color-secondary-light)',
        'accent': 'var(--color-accent)',
        'text': 'var(--color-text)',
        'text-light': 'var(--color-text-light)',
        'text-muted': 'var(--color-text-muted)',
        'background': 'var(--color-background)',
        'background-light': 'var(--color-background-light)',
        'border': 'var(--color-border)',
        'error': 'var(--color-error)',
        'success': 'var(--color-success)',
        'warning': 'var(--color-warning)',
      },
      fontFamily: {
        'primary': 'var(--font-primary)',
        'secondary': 'var(--font-secondary)',
      },
      spacing: {
        'section': 'var(--spacing-section)',
        'element': 'var(--spacing-element)',
      },
      borderRadius: {
        'theme': 'var(--border-radius)',
        'theme-lg': 'var(--border-radius-lg)',
      },
      boxShadow: {
        'theme': 'var(--shadow)',
        'theme-lg': 'var(--shadow-lg)',
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}