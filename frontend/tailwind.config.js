/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'cr-blue': '#3B91E3',
        'cr-purple': '#9C4DCC',
        'cr-orange': '#FF9800',
        'brilliant': '#1DB954',
        'great': '#4CAF50',
        'good': '#8BC34A',
        'inaccuracy': '#FFC107',
        'mistake': '#FF9800',
        'blunder': '#F44336',
      }
    },
  },
  plugins: [],
}
