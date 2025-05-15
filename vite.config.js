import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// Conection https://ipaddress:5000

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 5000,
    strictPort: true
  }
})
