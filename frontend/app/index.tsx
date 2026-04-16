import React, { useEffect, useRef, useState } from 'react';
import { View, Text, StyleSheet, Image, Animated as RNAnimated } from 'react-native';
import { useRouter } from 'expo-router';
import { useAuthStore } from '../store/authStore';
import { Colors, Spacing } from '../constants/Colors';

const ICON_URL = 'https://static.prod-images.emergentagent.com/jobs/d9dce736-ec31-45a5-8f71-a124d3cd6030/images/47aab7b6590a09b1f0856621efe0291e4d9a0f2ec42ccc4cc7c9b6374114ba67.png';

const SPLASH_DURATION = 12000; // 12 seconds

export default function SplashScreen() {
  const router = useRouter();
  const hasNavigated = useRef(false);
  const fadeAnim = useRef(new RNAnimated.Value(0)).current;
  const taglineFade = useRef(new RNAnimated.Value(0)).current;
  const [dots, setDots] = useState('');

  // Fade in animation
  useEffect(() => {
    RNAnimated.sequence([
      RNAnimated.timing(fadeAnim, {
        toValue: 1,
        duration: 1500,
        useNativeDriver: true,
      }),
      RNAnimated.timing(taglineFade, {
        toValue: 1,
        duration: 1000,
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  // Animated dots
  useEffect(() => {
    const interval = setInterval(() => {
      setDots(prev => prev.length >= 3 ? '' : prev + '.');
    }, 600);
    return () => clearInterval(interval);
  }, []);

  // Fixed timer - always waits SPLASH_DURATION regardless of auth state changes
  useEffect(() => {
    const timer = setTimeout(() => {
      if (hasNavigated.current) return;
      hasNavigated.current = true;

      const { isAuthenticated, isLoading } = useAuthStore.getState();
      if (isLoading) {
        setTimeout(() => {
          const state = useAuthStore.getState();
          if (state.isAuthenticated) {
            router.replace('/(tabs)/home');
          } else {
            router.replace('/onboarding');
          }
        }, 2000);
      } else if (isAuthenticated) {
        router.replace('/(tabs)/home');
      } else {
        router.replace('/onboarding');
      }
    }, SPLASH_DURATION);

    return () => clearTimeout(timer);
  }, []);

  return (
    <View style={styles.container}>
      <RNAnimated.View style={[styles.content, { opacity: fadeAnim }]}>
        <Image source={{ uri: ICON_URL }} style={styles.icon} resizeMode="contain" />
        <Text style={styles.brandName}>NO LIMIT</Text>
        <Text style={styles.brandSub}>DELIVERY</Text>
      </RNAnimated.View>
      <RNAnimated.View style={{ opacity: taglineFade }}>
        <Text style={styles.tagline}>Limitless delivery locally</Text>
        <Text style={styles.loadingText}>Loading{dots}</Text>
      </RNAnimated.View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
    alignItems: 'center',
    justifyContent: 'center',
  },
  content: {
    alignItems: 'center',
  },
  icon: {
    width: 130,
    height: 130,
    borderRadius: 32,
    marginBottom: Spacing.lg,
  },
  brandName: {
    fontSize: 32,
    fontWeight: '700',
    color: Colors.textPrimary,
    letterSpacing: 3,
    textAlign: 'center',
  },
  brandSub: {
    fontSize: 14,
    fontWeight: '400',
    color: Colors.textSecondary,
    letterSpacing: 6,
    textAlign: 'center',
    marginBottom: Spacing.lg,
  },
  tagline: {
    fontSize: 15,
    fontWeight: '300',
    color: Colors.textSecondary,
    letterSpacing: 1,
    textAlign: 'center',
  },
  loadingText: {
    fontSize: 12,
    fontWeight: '400',
    color: Colors.gray,
    textAlign: 'center',
    marginTop: Spacing.md,
    minWidth: 80,
  },
});
