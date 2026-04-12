// Design System - Black, White, and Sage Color Palette

export const Colors = {
  // Primary Colors
  sage: '#87A96B',
  sageDark: '#6B8A4F',
  sageLight: '#A8C48F',
  sagePale: '#D4E4C7',
  
  // Neutrals
  black: '#000000',
  charcoal: '#1A1A1A',
  darkGray: '#333333',
  gray: '#666666',
  lightGray: '#CCCCCC',
  paleGray: '#F5F5F5',
  white: '#FFFFFF',
  
  // Semantic Colors
  success: '#87A96B',
  error: '#E74C3C',
  warning: '#F39C12',
  info: '#87A96B',
  
  // Backgrounds
  background: '#FFFFFF',
  surface: '#F5F5F5',
  card: '#FFFFFF',
  
  // Text
  textPrimary: '#000000',
  textSecondary: '#666666',
  textTertiary: '#999999',
  textInverse: '#FFFFFF',
  
  // Borders
  border: '#E0E0E0',
  borderLight: '#F0F0F0',
  
  // Overlays
  overlay: 'rgba(0, 0, 0, 0.5)',
  overlayLight: 'rgba(0, 0, 0, 0.3)',
};

export const Spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

export const BorderRadius = {
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  full: 999,
};

export const Typography = {
  h1: {
    fontSize: 32,
    fontWeight: '700' as const,
    lineHeight: 40,
  },
  h2: {
    fontSize: 28,
    fontWeight: '700' as const,
    lineHeight: 36,
  },
  h3: {
    fontSize: 24,
    fontWeight: '600' as const,
    lineHeight: 32,
  },
  h4: {
    fontSize: 20,
    fontWeight: '600' as const,
    lineHeight: 28,
  },
  body: {
    fontSize: 16,
    fontWeight: '400' as const,
    lineHeight: 24,
  },
  bodySmall: {
    fontSize: 14,
    fontWeight: '400' as const,
    lineHeight: 20,
  },
  caption: {
    fontSize: 12,
    fontWeight: '400' as const,
    lineHeight: 16,
  },
  button: {
    fontSize: 16,
    fontWeight: '600' as const,
    lineHeight: 24,
  },
};
