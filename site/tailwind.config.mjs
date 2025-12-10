/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
	theme: {
		extend: {
			colors: {
				primary: '#00f0ff', // Cyber Cyan
				secondary: '#7000ff', // Cyber Purple
				accent: '#ff003c', // Cyber Red
				dark: '#050505', // Deep Black
				surface: '#111111', // Dark Gray
				light: '#eeeeee', // Off-white text
				muted: '#888888', // Gray text
			},
			fontFamily: {
				sans: ['Inter', 'sans-serif'],
				mono: ['"Space Mono"', '"Courier New"', 'monospace'],
			},
			boxShadow: {
				'neon': '0 0 5px theme("colors.primary"), 0 0 20px theme("colors.primary")',
				'neon-secondary': '0 0 5px theme("colors.secondary"), 0 0 20px theme("colors.secondary")',
			},
		},
	},
	plugins: [],
}
