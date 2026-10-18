import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  envPrefix: ['VITE_', 'REACT_APP_'],
  server: {
    // Loopback-only by default. Private remote access must opt in explicitly.
    host: process.env.NOVA_BIND_HOST || '127.0.0.1',
    port: 3000,
    strictPort: true,
    allowedHosts: (process.env.NOVA_ALLOWED_HOSTS || 'localhost,127.0.0.1')
      .split(',')
      .map((host) => host.trim())
      .filter(Boolean),
    watch: {
      usePolling: true,
    },
  },
})
