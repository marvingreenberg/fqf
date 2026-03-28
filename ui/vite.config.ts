import { sveltekit } from '@sveltejs/kit/vite';
import tailwindcss from '@tailwindcss/vite';
import { defineConfig } from 'vitest/config';
import path from 'path';

const skeletonBase = path.resolve(import.meta.dirname, 'node_modules/@skeletonlabs/skeleton/src');

export default defineConfig({
    plugins: [tailwindcss(), sveltekit()],
    resolve: {
        alias: {
            // Allows @import 'skeleton-theme/cerberus.css' to resolve via Vite
            'skeleton-theme': path.join(skeletonBase, 'themes'),
            'skeleton-base': skeletonBase
        }
    },
    server: {
        proxy: {
            '/api': 'http://localhost:8000'
        }
    },
    test: {
        include: ['src/**/*.test.ts'],
        environment: 'jsdom'
    }
});
