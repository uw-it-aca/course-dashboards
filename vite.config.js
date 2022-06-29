import { fileURLToPath, URL } from "url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({

  // MARK: start vite build config
  build: {
    manifest: true,
    rollupOptions: {
      input: [
        // MARK: list all entry points
        './coursedashboards_vue/main.js',
      ]
    },
    outDir: './coursedashboards/static/', // NOTE: '/static/'
    assetsDir: 'coursedashboards/assets', // NOTE: '/static/coursedashboards/assets/xxxx.js'
    emptyOutDir: true,
  },
  base: "/static/", // MARK: allows for proper css url path creation
  // root: "./coursedashboards_vue",

  // MARK: standard vite/vue plugin and resolver
  plugins: [vue(),],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./coursedashboards_vue", import.meta.url)),
    },
  },
});
