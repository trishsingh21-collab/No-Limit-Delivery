// Design System - Premium Dark Luxury Theme
// "No Limit Delivery" - High-end concierge service aesthetic

export const Colors = {
  // Primary - Muted Sage
  sage: '#A3B18A',
  sageDark: '#8C9C72',
  sageLight: '#B8C9A0',
  sagePale: 'rgba(163, 177, 138, 0.15)',
  sageGlow: 'rgba(163, 177, 138, 0.4)',

  // Dark Backgrounds
  black: '#0A0A0A',
  charcoal: '#141414',
  darkGray: '#1A1A1A',
  surface: '#141414',

  // Light Neutrals
  gray: '#666666',
  lightGray: '#333333',
  paleGray: '#1A1A1A',
  white: '#FFFFFF',

  // Semantic
  success: '#A3B18A',
  error: '#E74C3C',
  warning: '#F5A623',
  info: '#A3B18A',

  // Backgrounds
  background: '#0A0A0A',
  card: '#141414',

  // Text
  textPrimary: '#FFFFFF',
  textSecondary: '#A0A0A0',
  textTertiary: '#666666',
  textInverse: '#0A0A0A',

  // Borders
  border: 'rgba(255, 255, 255, 0.08)',
  borderLight: 'rgba(255, 255, 255, 0.05)',

  // Overlays
  overlay: 'rgba(0, 0, 0, 0.7)',
  overlayLight: 'rgba(0, 0, 0, 0.4)',
  glass: 'rgba(10, 10, 10, 0.7)',
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
  xxl: 24,
  full: 999,
};

export const Typography = {
  h1: {
    fontSize: 36,
    fontWeight: '300' as const,
    lineHeight: 44,
    letterSpacing: -1,
  },
  h2: {
    fontSize: 28,
    fontWeight: '300' as const,
    lineHeight: 36,
    letterSpacing: -0.5,
  },
  h3: {
    fontSize: 22,
    fontWeight: '500' as const,
    lineHeight: 30,
  },
  h4: {
    fontSize: 18,
    fontWeight: '500' as const,
    lineHeight: 26,
  },
  body: {
    fontSize: 15,
    fontWeight: '300' as const,
    lineHeight: 22,
  },
  bodySmall: {
    fontSize: 13,
    fontWeight: '300' as const,
    lineHeight: 18,
  },
  caption: {
    fontSize: 11,
    fontWeight: '400' as const,
    lineHeight: 14,
  },
  overline: {
    fontSize: 11,
    fontWeight: '500' as const,
    lineHeight: 14,
    letterSpacing: 2,
  },
  button: {
    fontSize: 15,
    fontWeight: '500' as const,
    lineHeight: 22,
  },
};
