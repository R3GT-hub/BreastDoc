import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
	type: 'content',
	// Type-check frontmatter using a schema
	schema: z.object({
		title: z.string(),
		description: z.string(),
		// Transform string to Date object
		pubDate: z.coerce.date(),
		updatedDate: z.coerce.date().optional(),
		heroImage: z.string().optional(),
	}),
});

const treatments = defineCollection({
	schema: z.object({
		title: z.string(),
		id:z.number().optional(),
		description: z.string(),
		tags: z.array(z.string()).optional(),
		heroImage: z.string().optional(),
	}),
});

export const collections = { blog };
