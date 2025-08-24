import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ mode }) => ({
  plugins: [react()],
  // In development, no base path (direct access). In production, use /admin/ base path
  base: mode === 'production' ? '/admin/' : '/',
  server: {
    port: 5174, // Different port to avoid clashing with form app
    host: true,
    proxy: {
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true,
        secure: false,
        timeout: 60000,
        proxyTimeout: 60000,
        configure: (proxy) => {
          proxy.on('error', (err) => {
            console.log('proxy error', err);
          });
          proxy.on('proxyReq', (proxyReq, req) => {
            console.log('Sending Request to the Target:', req.method, req.url);
          });
          proxy.on('proxyRes', (proxyRes, req) => {
            console.log('Received Response from the Target:', proxyRes.statusCode, req.url);
          });
        },
      }
    }
  },
  preview: {
    port: 4174
  }
}))
