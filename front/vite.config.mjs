import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'node:path'
import autoprefixer from 'autoprefixer'
import commonjs from 'vite-plugin-commonjs'

export default defineConfig({
  base: './',
  build: {
    outDir: 'build',
    commonjsOptions: {
      include: [/node_modules/],
      transformMixedEsModules: true, // Allow transformation of mixed ES modules
    },
  },
  css: {
    postcss: {
      plugins: [
        autoprefixer({}), // add options if needed
      ],
    },
  },
  esbuild: {
    loader: 'jsx',
    include: /src\/.*\.jsx?$/,
    exclude: [],
  },
  optimizeDeps: {
    force: true,
    esbuildOptions: {
      loader: {
        '.js': 'jsx',
      },
    },
    include: ['react-router-named-routes'], // Include specific package
  },
  plugins: [
    react(),
    commonjs(),
  ],
  resolve: {
    alias: [
      {
        find: 'src/',
        replacement: `${path.resolve(__dirname, 'src')}/`,
      },
    ],
    extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json', '.scss'],
  },
  server: {
    port: 3000,
    proxy: {
      // https://vitejs.dev/config/server-options.html
    },
  },
})
