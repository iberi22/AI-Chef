import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://iberi22.github.io',
  base: '/AI-Chef',
  output: 'static',
  integrations: [tailwind()],
  // Disable image optimization to avoid issues with Git LFS pointers
  image: {
    service: { entrypoint: 'astro/assets/services/noop' }
  }
});
