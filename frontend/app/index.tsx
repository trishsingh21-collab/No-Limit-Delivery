import React, { useEffect } from 'react';
import { View, Text, StyleSheet, Image } from 'react-native';
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
        <Ionicons name="restaurant" size={80} color={Colors.sage} />
        <Text style={styles.appName}>No Limit</Text>
        <Text style={styles.appNameSub}>Delivery</Text>
      </View>
      <Text style={styles.tagline}>Food delivered with no limits</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.white,
    alignItems: 'center',
    justifyContent: 'center',
  },
  logoContainer: {
    alignItems: 'center',
    marginBottom: Spacing.xxl,
  },
  appName: {
    ...Typography.h1,
    fontSize: 42,
    color: Colors.black,
    marginTop: Spacing.md,
    fontWeight: '700',
  },
  appNameSub: {
    ...Typography.h2,
    color: Colors.sage,
    fontWeight: '600',
  },
  tagline: {
    ...Typography.body,
    color: Colors.textSecondary,
    marginTop: Spacing.md,
  },
});
