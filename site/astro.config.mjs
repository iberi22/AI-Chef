import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import { passthroughImageService } from 'astro/config';

export default defineConfig({
  site: 'https://iberi22.github.io',
  base: '/AI-Chef',
  output: 'static',
  integrations: [tailwind()],
  // Disable image optimization to avoid issues with Git LFS pointers
  image: {
    service: passthroughImageService()
  }
});
