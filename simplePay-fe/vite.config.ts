import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { resolve } from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), tailwindcss()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    allowedHosts: ['localhost'],
    port: 5173,
    host: true,
    strictPort: true
  },
  preview: {
    allowedHosts: ['thesis-app-myxvz.ondigitalocean.app'],
    host: true,
    port: 4173,
    strictPort: true
  }
})
