import React, { useEffect } from 'react';
import { View, Text, StyleSheet, Image } from 'react-native';
import { useRouter } from 'expo-router';
import { useAuthStore } from '../store/authStore';
import { Colors, Spacing } from '../constants/Colors';

const ICON_URL = 'https://static.prod-images.emergentagent.com/jobs/d9dce736-ec31-45a5-8f71-a124d3cd6030/images/fbc42bd4fce64eda9d87b3c2088d37d8aa9637f56451d288c0e41be214db92c6.png';
const LOGO_URL = 'https://static.prod-images.emergentagent.com/jobs/d9dce736-ec31-45a5-8f71-a124d3cd6030/images/ef138190ead02ebe8a98101f1b1ce17d392af0f16a2c371c56604c3d9f3cf927.png';

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
    }, 3000);
    return () => clearTimeout(timer);
  }, [isAuthenticated, isLoading]);

  return (
    <View style={styles.container}>
      <Image source={{ uri: ICON_URL }} style={styles.icon} resizeMode="contain" />
      <Image source={{ uri: LOGO_URL }} style={styles.logo} resizeMode="contain" />
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
  icon: {
    width: 120,
    height: 120,
    borderRadius: 28,
    marginBottom: Spacing.lg,
  },
  logo: {
    width: 240,
    height: 80,
    marginBottom: Spacing.md,
  },
  tagline: {
    fontSize: 14,
    fontWeight: '300',
    color: Colors.textSecondary,
    letterSpacing: 1,
  },
});
