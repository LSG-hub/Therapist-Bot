import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // This makes the server accessible externally
    port: 3000, // Ensure this matches your Dockerfile EXPOSE port if running dev server
  },
  preview: {
    host: true, // Allow external access for preview server
    port: 8080, // Ensure this matches your App Runner port configuration
    strictPort: true,
    allowedHosts: ['*'], // Allow all hosts for preview (use with caution in production)
  },
})
