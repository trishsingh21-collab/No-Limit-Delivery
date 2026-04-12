// Design System - Premium Sage & White with Gradient Feel
// "No Limit Delivery" - Elegant, warm, premium

export const Colors = {
  // Primary Sage
  sage: '#87A96B',
  sageDark: '#6B8A4F',
  sageLight: '#A8C48F',
  sagePale: 'rgba(135, 169, 107, 0.12)',
  sageGlow: 'rgba(135, 169, 107, 0.25)',
  sageMuted: '#B8C9A0',

  // Backgrounds - Warm sage-gray gradient feel
  background: '#F0F2ED',     // Soft sage-gray
  surface: '#FFFFFF',         // White cards
  surfaceAlt: '#E8EBE4',     // Slightly darker sage-gray
  card: '#FFFFFF',

  // Neutrals
  black: '#1A1A1A',
  charcoal: '#2A2A2A',
  darkGray: '#3A3A3A',
  gray: '#7A7A7A',
  lightGray: '#C8C8C8',
  paleGray: '#E8EBE4',
  white: '#FFFFFF',

  // Semantic
  success: '#87A96B',
  error: '#D94F4F',
  warning: '#E8A838',
  info: '#87A96B',

  // Text
  textPrimary: '#1A1A1A',
  textSecondary: '#6B6B6B',
  textTertiary: '#999999',
  textInverse: '#FFFFFF',

  // Borders
  border: 'rgba(0, 0, 0, 0.08)',
  borderLight: 'rgba(0, 0, 0, 0.04)',

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
  xxl: 24,
  full: 999,
};

export const Typography = {
  h1: {
    fontSize: 34,
    fontWeight: '300' as const,
    lineHeight: 42,
    letterSpacing: -0.5,
  },
  h2: {
    fontSize: 26,
    fontWeight: '400' as const,
    lineHeight: 34,
  },
  h3: {
    fontSize: 22,
    fontWeight: '600' as const,
    lineHeight: 30,
  },
  h4: {
    fontSize: 18,
    fontWeight: '600' as const,
    lineHeight: 26,
  },
  body: {
    fontSize: 15,
    fontWeight: '400' as const,
    lineHeight: 22,
  },
  bodySmall: {
    fontSize: 13,
    fontWeight: '400' as const,
    lineHeight: 18,
  },
  caption: {
    fontSize: 11,
    fontWeight: '500' as const,
    lineHeight: 14,
  },
  overline: {
    fontSize: 11,
    fontWeight: '600' as const,
    lineHeight: 14,
    letterSpacing: 2,
  },
  button: {
    fontSize: 15,
    fontWeight: '600' as const,
    lineHeight: 22,
  },
};
