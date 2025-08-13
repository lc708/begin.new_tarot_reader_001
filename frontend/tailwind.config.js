/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/features/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#6B46C1',      // 深紫色
        secondary: '#F59E0B',    // 金色
        background: '#0F0F23',   // 深蓝黑
        surface: '#1E1B4B',      // 深紫蓝
        accent: '#8B5CF6',       // 亮紫色
        mystical: {
          50: '#F3F4F6',
          100: '#E5E7EB',
          200: '#D1D5DB',
          300: '#9CA3AF',
          400: '#6B7280',
          500: '#374151',
          600: '#1F2937',
          700: '#111827',
          800: '#0F0F23',
          900: '#030712',
        }
      },
      fontFamily: {
        'mystical': ['serif'],
      },
      backgroundImage: {
        'starry': "url('/images/starry-bg.jpg')",
        'mystical-gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      },
      animation: {
        'card-flip': 'cardFlip 0.8s ease-in-out',
        'card-shuffle': 'cardShuffle 2s infinite',
        'mystical-glow': 'mysticalGlow 3s ease-in-out infinite alternate',
      },
      keyframes: {
        cardFlip: {
          '0%': { transform: 'rotateY(0deg)' },
          '50%': { transform: 'rotateY(90deg)' },
          '100%': { transform: 'rotateY(0deg)' },
        },
        cardShuffle: {
          '0%, 100%': { transform: 'translateX(0px) rotate(0deg)' },
          '25%': { transform: 'translateX(-2px) rotate(-1deg)' },
          '75%': { transform: 'translateX(2px) rotate(1deg)' },
        },
        mysticalGlow: {
          '0%': { boxShadow: '0 0 20px rgba(139, 92, 246, 0.3)' },
          '100%': { boxShadow: '0 0 40px rgba(139, 92, 246, 0.6)' },
        },
      },
    },
  },
  plugins: [],
}

