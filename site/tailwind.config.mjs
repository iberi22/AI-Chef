/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
	darkMode: 'class',
	theme: {
		extend: {
			colors: {
				"primary": "#f9f506",
				"background-light": "#f8f8f5",
				"background-dark": "#121212",
				"surface-light": "#ffffff",
				"surface-dark": "#1e1e1e",
				"text-light": "#181811",
				"text-dark": "#e0e0e0",
				"neutral-border": "#e6e6db",
				"neutral-border-dark": "#44433a",
			},
			fontFamily: {
				"display": ["Spline Sans", "sans-serif"],
				"mono": ["Space Mono", "monospace"],
			},
			borderRadius: { "DEFAULT": "1rem", "lg": "1.5rem", "xl": "2rem", "2xl": "2.5rem", "full": "9999px" },
			boxShadow: {
				"neon": "0 0 10px rgba(249, 245, 6, 0.5)",
				"neon-hover": "0 0 20px rgba(249, 245, 6, 0.8)",
			}
		},
	},
	plugins: [
		require('@tailwindcss/forms'),
		require('@tailwindcss/container-queries'),
	],
}
