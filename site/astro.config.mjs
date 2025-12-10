import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://iberi22.github.io',
  base: '/AI-Chef',
  output: 'static',
  integrations: [tailwind()]
});
