import { fileURLToPath, URL } from "url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
  // MARK: start vite build config

  // vite creates a manifest and assets during the build process (local and prod)
  // django collectstatics will put assets in '/static/app_name/assets'
  // django will put the manifest in '/static/manifest.json'
  // vite manifest prefaces all files with the path 'app_name/assets/xxxx'
  build: {
    manifest: true,
    sourcemap: true,
    rollupOptions: {
      input: [
        // list all entry points
        "./coursedashboards_vue/main.js",
      ],
    },
    outDir: "./coursedashboards/static/", // relative path to django's static directory
    assetsDir: "coursedashboards/assets", // default ('assets')... this is the namespaced subdirectory of outDir that vite uses
    emptyOutDir: true, // set to false to ensure favicon is not overwritten
  },
  base: "/static/", // allows for proper css url path creation during the build process

  // MARK: standard vite/vue plugin and resolver config
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./coursedashboards_vue", import.meta.url)),
    },
  },
});
