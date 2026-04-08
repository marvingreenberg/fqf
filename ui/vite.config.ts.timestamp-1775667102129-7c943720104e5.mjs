// vite.config.ts
import { sveltekit } from "file:///Users/mgreenberg/git/fqf/ui/node_modules/.pnpm/@sveltejs+kit@2.55.0_@sveltejs+vite-plugin-svelte@4.0.4_svelte@5.55.0_vite@5.4.21_light_01bebbeaeb735d69be2dad6136c9a997/node_modules/@sveltejs/kit/src/exports/vite/index.js";
import tailwindcss from "file:///Users/mgreenberg/git/fqf/ui/node_modules/.pnpm/@tailwindcss+vite@4.2.2_vite@5.4.21_lightningcss@1.32.0_/node_modules/@tailwindcss/vite/dist/index.mjs";
import { defineConfig } from "file:///Users/mgreenberg/git/fqf/ui/node_modules/.pnpm/vitest@2.1.9_jsdom@26.1.0_lightningcss@1.32.0/node_modules/vitest/dist/config.js";
import path from "path";
var __vite_injected_original_dirname = "/Users/mgreenberg/git/fqf/ui";
var skeletonBase = path.resolve(__vite_injected_original_dirname, "node_modules/@skeletonlabs/skeleton/src");
var vite_config_default = defineConfig({
  plugins: [tailwindcss(), sveltekit()],
  resolve: {
    alias: {
      // Allows @import 'skeleton-theme/cerberus.css' to resolve via Vite
      "skeleton-theme": path.join(skeletonBase, "themes"),
      "skeleton-base": skeletonBase
    }
  },
  server: {
    proxy: {
      "/api": "http://localhost:8000"
    }
  },
  test: {
    include: ["src/**/*.test.ts"],
    environment: "jsdom"
  }
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcudHMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCIvVXNlcnMvbWdyZWVuYmVyZy9naXQvZnFmL3VpXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ZpbGVuYW1lID0gXCIvVXNlcnMvbWdyZWVuYmVyZy9naXQvZnFmL3VpL3ZpdGUuY29uZmlnLnRzXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ltcG9ydF9tZXRhX3VybCA9IFwiZmlsZTovLy9Vc2Vycy9tZ3JlZW5iZXJnL2dpdC9mcWYvdWkvdml0ZS5jb25maWcudHNcIjtpbXBvcnQgeyBzdmVsdGVraXQgfSBmcm9tICdAc3ZlbHRlanMva2l0L3ZpdGUnO1xuaW1wb3J0IHRhaWx3aW5kY3NzIGZyb20gJ0B0YWlsd2luZGNzcy92aXRlJztcbmltcG9ydCB7IGRlZmluZUNvbmZpZyB9IGZyb20gJ3ZpdGVzdC9jb25maWcnO1xuaW1wb3J0IHBhdGggZnJvbSAncGF0aCc7XG5cbmNvbnN0IHNrZWxldG9uQmFzZSA9IHBhdGgucmVzb2x2ZShpbXBvcnQubWV0YS5kaXJuYW1lLCAnbm9kZV9tb2R1bGVzL0Bza2VsZXRvbmxhYnMvc2tlbGV0b24vc3JjJyk7XG5cbmV4cG9ydCBkZWZhdWx0IGRlZmluZUNvbmZpZyh7XG4gICAgcGx1Z2luczogW3RhaWx3aW5kY3NzKCksIHN2ZWx0ZWtpdCgpXSxcbiAgICByZXNvbHZlOiB7XG4gICAgICAgIGFsaWFzOiB7XG4gICAgICAgICAgICAvLyBBbGxvd3MgQGltcG9ydCAnc2tlbGV0b24tdGhlbWUvY2VyYmVydXMuY3NzJyB0byByZXNvbHZlIHZpYSBWaXRlXG4gICAgICAgICAgICAnc2tlbGV0b24tdGhlbWUnOiBwYXRoLmpvaW4oc2tlbGV0b25CYXNlLCAndGhlbWVzJyksXG4gICAgICAgICAgICAnc2tlbGV0b24tYmFzZSc6IHNrZWxldG9uQmFzZVxuICAgICAgICB9XG4gICAgfSxcbiAgICBzZXJ2ZXI6IHtcbiAgICAgICAgcHJveHk6IHtcbiAgICAgICAgICAgICcvYXBpJzogJ2h0dHA6Ly9sb2NhbGhvc3Q6ODAwMCdcbiAgICAgICAgfVxuICAgIH0sXG4gICAgdGVzdDoge1xuICAgICAgICBpbmNsdWRlOiBbJ3NyYy8qKi8qLnRlc3QudHMnXSxcbiAgICAgICAgZW52aXJvbm1lbnQ6ICdqc2RvbSdcbiAgICB9XG59KTtcbiJdLAogICJtYXBwaW5ncyI6ICI7QUFBc1EsU0FBUyxpQkFBaUI7QUFDaFMsT0FBTyxpQkFBaUI7QUFDeEIsU0FBUyxvQkFBb0I7QUFDN0IsT0FBTyxVQUFVO0FBSGpCLElBQU0sbUNBQW1DO0FBS3pDLElBQU0sZUFBZSxLQUFLLFFBQVEsa0NBQXFCLHlDQUF5QztBQUVoRyxJQUFPLHNCQUFRLGFBQWE7QUFBQSxFQUN4QixTQUFTLENBQUMsWUFBWSxHQUFHLFVBQVUsQ0FBQztBQUFBLEVBQ3BDLFNBQVM7QUFBQSxJQUNMLE9BQU87QUFBQTtBQUFBLE1BRUgsa0JBQWtCLEtBQUssS0FBSyxjQUFjLFFBQVE7QUFBQSxNQUNsRCxpQkFBaUI7QUFBQSxJQUNyQjtBQUFBLEVBQ0o7QUFBQSxFQUNBLFFBQVE7QUFBQSxJQUNKLE9BQU87QUFBQSxNQUNILFFBQVE7QUFBQSxJQUNaO0FBQUEsRUFDSjtBQUFBLEVBQ0EsTUFBTTtBQUFBLElBQ0YsU0FBUyxDQUFDLGtCQUFrQjtBQUFBLElBQzVCLGFBQWE7QUFBQSxFQUNqQjtBQUNKLENBQUM7IiwKICAibmFtZXMiOiBbXQp9Cg==
