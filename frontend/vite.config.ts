import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: true, // Listen on all addresses, including LAN and public addresses
    proxy: {
      // Proxy API requests to Django backend
      '/api': {
        target: 'https://api.7sanah.com',
        changeOrigin: true,
        secure: true,
      }
    },
    // Allow all hosts to access the dev server
    allowedHosts: true
  }
})
