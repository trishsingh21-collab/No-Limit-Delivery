import React, { useEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { useRouter } from 'expo-router';
import { useAuthStore } from '../store/authStore';
import { Colors, Typography, Spacing } from '../constants/Colors';
import { Ionicons } from '@expo/vector-icons';

export default function SplashScreen() {
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuthStore();

  useEffect(() => {
    const timer = setTimeout(() => {
      if (isLoading) return;
      if (isAuthenticated) {
        router.replace('/(tabs)/home');
      } else {
        router.replace('/onboarding');
      }
    }, 2000);
    return () => clearTimeout(timer);
  }, [isAuthenticated, isLoading]);

  return (
    <View style={styles.container}>
      <View style={styles.logoContainer}>
        <View style={styles.iconRing}>
          <Ionicons name="flash" size={48} color={Colors.sage} />
        </View>
        <Text style={styles.appName}>NO LIMIT</Text>
        <Text style={styles.appNameSub}>DELIVERY</Text>
      </View>
      <Text style={styles.tagline}>Premium delivery, no limits</Text>
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
  logoContainer: {
    alignItems: 'center',
    marginBottom: Spacing.xxl,
  },
  iconRing: {
    width: 100,
    height: 100,
    borderRadius: 50,
    borderWidth: 1,
    borderColor: Colors.sage,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: Spacing.lg,
  },
  appName: {
    fontSize: 36,
    fontWeight: '200',
    color: Colors.white,
    letterSpacing: 8,
  },
  appNameSub: {
    fontSize: 14,
    fontWeight: '500',
    color: Colors.sage,
    letterSpacing: 6,
    marginTop: Spacing.xs,
  },
  tagline: {
    ...Typography.body,
    color: Colors.textSecondary,
  },
});
