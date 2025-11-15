import { defineConfig } from 'vite';

export default defineConfig({
  // Development server configuration
  server: {
    port: 5173,
    open: false
  },
  // Optimize dependencies
  optimizeDeps: {
    include: ['@vapi-ai/web']
  },
  // Build configuration for library
  build: {
    outDir: 'dist',
    sourcemap: true,
    lib: {
      entry: 'src/index.ts',
      name: 'PrepWiseVoiceRecorder',
      fileName: 'index',
      formats: ['es', 'cjs']
    },
    rollupOptions: {
      external: [],
      output: {
        globals: {}
      }
    }
  },
});

