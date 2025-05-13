import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',      // Permet d’accepter les connexions réseau
    port: 5173,           // Tu peux changer ce port si besoin
    strictPort: true      // Empêche Vite de changer le port automatiquement
  }
})
