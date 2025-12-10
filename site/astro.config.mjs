import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://iberi22.github.io',
  base: '/AI-Chef',
  output: 'static',
  integrations: [tailwind()],
  // Disable image optimization completely
  image: {
    service: { entrypoint: import.meta.env.DEV ? 'astro/assets/services/sharp' : 'astro/assets/services/noop' }
  }
});
