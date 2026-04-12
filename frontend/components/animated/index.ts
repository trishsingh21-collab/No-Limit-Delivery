import React, { useEffect } from 'react';
import { ViewStyle, StyleProp } from 'react-native';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withSpring,
  withDelay,
  withSequence,
  Easing,
  FadeIn,
  FadeInDown,
  FadeInUp,
  FadeInLeft,
  FadeInRight,
  SlideInDown,
  SlideInLeft,
  SlideInRight,
  ZoomIn,
  BounceIn,
} from 'react-native-reanimated';

// ==================== PRESET ANIMATIONS ====================

export const PRESETS = {
  fadeIn: FadeIn.duration(400),
  fadeInDown: FadeInDown.duration(400).springify(),
  fadeInUp: FadeInUp.duration(400).springify(),
  fadeInLeft: FadeInLeft.duration(350),
  fadeInRight: FadeInRight.duration(350),
  slideInDown: SlideInDown.duration(400).springify(),
  slideInLeft: SlideInLeft.duration(350),
  slideInRight: SlideInRight.duration(350),
  zoomIn: ZoomIn.duration(300),
  bounceIn: BounceIn.duration(500),
};

// ==================== STAGGER ITEM ====================

interface StaggerItemProps {
  index: number;
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
  delay?: number;
}

export function StaggerItem({ index, children, style, delay = 80 }: StaggerItemProps) {
  const opacity = useSharedValue(0);
  const translateY = useSharedValue(20);

  useEffect(() => {
    opacity.value = withDelay(index * delay, withTiming(1, { duration: 350, easing: Easing.out(Easing.ease) }));
    translateY.value = withDelay(index * delay, withSpring(0, { damping: 15, stiffness: 120 }));
  }, []);

  const animStyle = useAnimatedStyle(() => ({
    opacity: opacity.value,
    transform: [{ translateY: translateY.value }],
  }));

  return <Animated.View style={[animStyle, style]}>{children}</Animated.View>;
}

// ==================== FADE IN VIEW ====================

interface FadeInViewProps {
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
  delay?: number;
  duration?: number;
}

export function FadeInView({ children, style, delay = 0, duration = 400 }: FadeInViewProps) {
  const opacity = useSharedValue(0);

  useEffect(() => {
    opacity.value = withDelay(delay, withTiming(1, { duration, easing: Easing.out(Easing.ease) }));
  }, []);

  const animStyle = useAnimatedStyle(() => ({
    opacity: opacity.value,
  }));

  return <Animated.View style={[animStyle, style]}>{children}</Animated.View>;
}

// ==================== SLIDE IN VIEW ====================

interface SlideInViewProps {
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
  delay?: number;
  from?: 'left' | 'right' | 'bottom' | 'top';
  distance?: number;
}

export function SlideInView({ children, style, delay = 0, from = 'bottom', distance = 30 }: SlideInViewProps) {
  const opacity = useSharedValue(0);
  const translateX = useSharedValue(from === 'left' ? -distance : from === 'right' ? distance : 0);
  const translateY = useSharedValue(from === 'bottom' ? distance : from === 'top' ? -distance : 0);

  useEffect(() => {
    opacity.value = withDelay(delay, withTiming(1, { duration: 350 }));
    translateX.value = withDelay(delay, withSpring(0, { damping: 15, stiffness: 120 }));
    translateY.value = withDelay(delay, withSpring(0, { damping: 15, stiffness: 120 }));
  }, []);

  const animStyle = useAnimatedStyle(() => ({
    opacity: opacity.value,
    transform: [{ translateX: translateX.value }, { translateY: translateY.value }],
  }));

  return <Animated.View style={[animStyle, style]}>{children}</Animated.View>;
}

// ==================== SCALE PRESS ====================

interface ScalePressProps {
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
  onPress?: () => void;
  scale?: number;
}

export function ScalePress({ children, style, onPress, scale = 0.96 }: ScalePressProps) {
  const scaleVal = useSharedValue(1);

  const animStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scaleVal.value }],
  }));

  const handlePressIn = () => {
    scaleVal.value = withSpring(scale, { damping: 15, stiffness: 200 });
  };

  const handlePressOut = () => {
    scaleVal.value = withSpring(1, { damping: 15, stiffness: 200 });
  };

  return (
    <Animated.View style={[animStyle, style]}>
      {React.cloneElement(children as React.ReactElement, {
        onPressIn: handlePressIn,
        onPressOut: handlePressOut,
        onPress,
      })}
    </Animated.View>
  );
}

// ==================== PULSE ANIMATION ====================

interface PulseProps {
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
  active?: boolean;
}

export function Pulse({ children, style, active = true }: PulseProps) {
  const scaleVal = useSharedValue(1);

  useEffect(() => {
    if (active) {
      scaleVal.value = withSequence(
        withTiming(1.15, { duration: 600 }),
        withTiming(1, { duration: 600 }),
        withTiming(1.15, { duration: 600 }),
        withTiming(1, { duration: 600 })
      );

      const interval = setInterval(() => {
        scaleVal.value = withSequence(
          withTiming(1.15, { duration: 600 }),
          withTiming(1, { duration: 600 })
        );
      }, 1200);

      return () => clearInterval(interval);
    }
  }, [active]);

  const animStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scaleVal.value }],
  }));

  return <Animated.View style={[animStyle, style]}>{children}</Animated.View>;
}

// ==================== BOUNCE IN VIEW ====================

interface BounceInViewProps {
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
  delay?: number;
}

export function BounceInView({ children, style, delay = 0 }: BounceInViewProps) {
  const scaleVal = useSharedValue(0);
  const opacity = useSharedValue(0);

  useEffect(() => {
    opacity.value = withDelay(delay, withTiming(1, { duration: 200 }));
    scaleVal.value = withDelay(delay, withSpring(1, { damping: 12, stiffness: 150 }));
  }, []);

  const animStyle = useAnimatedStyle(() => ({
    opacity: opacity.value,
    transform: [{ scale: scaleVal.value }],
  }));

  return <Animated.View style={[animStyle, style]}>{children}</Animated.View>;
}

// ==================== COUNTER ANIMATION ====================

interface AnimatedCounterProps {
  value: number;
  style?: any;
  prefix?: string;
  decimals?: number;
}

export function AnimatedCounter({ value, style, prefix = '$', decimals = 2 }: AnimatedCounterProps) {
  const animVal = useSharedValue(0);

  useEffect(() => {
    animVal.value = withTiming(value, { duration: 400, easing: Easing.out(Easing.ease) });
  }, [value]);

  const animStyle = useAnimatedStyle(() => ({
    // We can't directly render text from animated values in RN easily,
    // so we use opacity animation as a visual indicator of change
    opacity: withSequence(
      withTiming(0.5, { duration: 100 }),
      withTiming(1, { duration: 200 })
    ),
  }));

  return (
    <Animated.Text style={[style, animStyle]}>
      {prefix}{value.toFixed(decimals)}
    </Animated.Text>
  );
}
