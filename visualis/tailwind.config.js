/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './app/**/*.{js,ts,jsx,tsx,mdx}',
        './components/**/*.{js,ts,jsx,tsx,mdx}'
    ],
    theme: {
        extend: {
            colors: {
                background: 'var(--background)',
                foreground: 'var(--foreground)',
                card: 'var(--card)',
                'card-foreground': 'var(--card-foreground)',
                primary: {
                    DEFAULT: 'rgb(var(--primary-500))',
                    foreground: 'rgb(var(--primary-foreground))',
                },
                // ALIAS SKY TO PRIMARY for backward compatibility & theming
                sky: {
                    50: '#f0f9ff',
                    100: '#e0f2fe',
                    200: '#bae6fd',
                    300: 'rgb(var(--primary-300) / <alpha-value>)',
                    400: 'rgb(var(--primary-400) / <alpha-value>)',
                    500: 'rgb(var(--primary-500) / <alpha-value>)',
                    600: 'rgb(var(--primary-600) / <alpha-value>)',
                    700: '#0369a1',
                    800: '#075985',
                    900: '#0c4a6e',
                    950: '#082f49',
                },
                // DYNAMIC SLATE PALETTE (Mapped to CSS variables)
                slate: {
                    50: 'rgb(var(--bg-50) / <alpha-value>)',
                    100: 'rgb(var(--bg-100) / <alpha-value>)',
                    200: 'rgb(var(--bg-200) / <alpha-value>)',
                    300: 'rgb(var(--bg-300) / <alpha-value>)',
                    400: 'rgb(var(--bg-400) / <alpha-value>)',
                    500: 'rgb(var(--bg-500) / <alpha-value>)',
                    600: 'rgb(var(--bg-600) / <alpha-value>)',
                    700: 'rgb(var(--bg-700) / <alpha-value>)',
                    800: 'rgb(var(--bg-800) / <alpha-value>)',
                    900: 'rgb(var(--bg-900) / <alpha-value>)',
                    950: 'rgb(var(--bg-950) / <alpha-value>)',
                },
            },
            fontFamily: {
                sans: ['var(--font-outfit)', 'sans-serif'],
            },
        },
    },
    plugins: [],
}
