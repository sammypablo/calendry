// tailwind.config.js
module.exports = {
  darkMode: 'class', // Enable class-based dark mode
  content: [
    // Django templates
    './templates/**/*.html',
    './**/templates/**/*.html',
    
    // JavaScript files
    './static/src/**/*.js',
    
    // Django apps templates (adjust paths as needed)
    './core/templates/**/*.html',
    './calendry/templates/**/*.html',
    
    // Add any other template locations
  ],
  theme: {
    extend: {
      colors: {
        // Extended color palette
        primary: {
          light: '#6366f1',
          DEFAULT: '#4f46e5',
          dark: '#4338ca',
        },
        secondary: {
          light: '#ec4899',
          DEFAULT: '#db2777',
          dark: '#be185d',
        },
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui'],
      },
      spacing: {
        '128': '32rem',
        '144': '36rem',
      },
      borderRadius: {
        'xl': '1rem',
        '2xl': '2rem',
      }
    },
  },
  plugins: [
    // Form plugin for better form styling
    require('@tailwindcss/forms'),
    
    // Typography plugin for prose content
    require('@tailwindcss/typography'),
    
    // Aspect ratio plugin
    require('@tailwindcss/aspect-ratio'),
    
    // Line clamp plugin
    require('@tailwindcss/line-clamp'),
  ],
}