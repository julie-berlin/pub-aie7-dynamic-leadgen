import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  base: '/admin/', // Serve admin app under /admin path
  server: {
    port: 5174, // Different port to avoid clashing with form app
    host: true
  },
  preview: {
    port: 4174
  }
})
