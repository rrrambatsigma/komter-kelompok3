import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      '/api/rambat': {
        target: 'http://100.87.168.12:5000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/rambat/, ''),
      },
      '/api/meiva': {
        target: 'http://100.78.200.58:5000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/meiva/, ''),
      },
    },
  },
})
