import { defineCollection, z } from 'astro:content';

const dishesCollection = defineCollection({
  type: 'content',
  schema: z.object({}).passthrough(),
});

const tipsCollection = defineCollection({
  type: 'content',
  schema: z.object({}).passthrough(),
});

export const collections = {
  'dishes': dishesCollection,
  'tips': tipsCollection,
};