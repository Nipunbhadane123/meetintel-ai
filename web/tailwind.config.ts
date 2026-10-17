import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#F0ECFF",
          100: "#E3DCFF",
          200: "#C7B9FF",
          300: "#AA96FF",
          400: "#8E73FF",
          500: "#6C4DFF",
          600: "#5536E8",
          700: "#4427C6",
          800: "#341DA0",
          900: "#241378",
        },
        surface: {
          light: "#FFFFFF",
          "light-soft": "#F1F4F9",
          "light-hover": "#F8FAFD",
          dark: "#161D2E",
          "dark-soft": "#1C253B",
          "dark-hover": "#202B44",
        },
        border: {
          light: "#E9ECF4",
          dark: "#232D42",
        },
      },
      fontFamily: {
        sans: [
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "Roboto",
          "Helvetica Neue",
          "Arial",
          "sans-serif",
        ],
      },
      boxShadow: {
        card: "0 1px 3px rgba(23, 32, 51, 0.04), 0 1px 2px rgba(23, 32, 51, 0.02)",
        "card-hover": "0 6px 16px -2px rgba(108, 77, 255, 0.08), 0 2px 6px -1px rgba(23, 32, 51, 0.04)",
        dropdown: "0 10px 25px -5px rgba(23, 32, 51, 0.1), 0 8px 10px -6px rgba(23, 32, 51, 0.08)",
      },
    },
  },
  plugins: [],
};

export default config;
