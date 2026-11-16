import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  //base path untuk GitHub Pages (diisi saat build demo, lihat .github/workflows/pages.yml)
  base: process.env.VITE_BASE || '/',
})
