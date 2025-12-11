/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
	darkMode: 'class',
	theme: {
		extend: {
			colors: {
				"primary": "#06b6d4",
				"secondary": "#a855f7",
				"accent": "#f472b6",
				"background-light": "#f8f8f5",
				"background-dark": "#050505",
				"surface-light": "#ffffff",
				"surface-dark": "#121212",
				"surface-highlight": "#1e1e1e",
				"text-light": "#181811",
				"text-dark": "#ededed",
				"text-muted": "#a1a1aa",
				"neutral-border": "#e6e6db",
				"neutral-border-dark": "#44433a",
			},
			fontFamily: {
				"display": ["Inter", "sans-serif"],
				"mono": ["Space Mono", "monospace"],
			},
			boxShadow: {
				"neon": "0 0 15px rgba(6, 182, 212, 0.4)",
				"neon-hover": "0 0 30px rgba(6, 182, 212, 0.6)",
				"neon-purple": "0 0 20px rgba(168, 85, 247, 0.3)",
			}
		},
	},
	plugins: [
		require('@tailwindcss/forms'),
		require('@tailwindcss/container-queries'),
	],
}
