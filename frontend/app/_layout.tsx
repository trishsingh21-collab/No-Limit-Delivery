import { useEffect } from 'react';
import { Stack, useRouter, useSegments } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { useAuthStore } from '../store/authStore';
import { Colors } from '../constants/Colors';

function useProtectedRoute() {
  const { isAuthenticated, isLoading } = useAuthStore();
  const segments = useSegments();
  const router = useRouter();

  useEffect(() => {
    if (isLoading) return;

    const inAuthGroup = segments[0] === 'auth';
    const inOnboarding = segments[0] === 'onboarding';
    const isRoot = segments.length === 0 || segments[0] === 'index';

    if (isAuthenticated && (inAuthGroup || inOnboarding || isRoot)) {
      // User is logged in but on auth/onboarding/splash - redirect to home
      router.replace('/(tabs)/home' as any);
    }
  }, [isAuthenticated, isLoading, segments]);
}

export default function RootLayout() {
  const loadUser = useAuthStore(state => state.loadUser);

  useEffect(() => {
    loadUser();
  }, []);

  useProtectedRoute();

  return (
    <>
      <StatusBar style="light" />
      <Stack
        screenOptions={{
          headerShown: false,
          contentStyle: { backgroundColor: Colors.background },
        }}
      >
        <Stack.Screen name="index" />
        <Stack.Screen name="onboarding" />
        <Stack.Screen name="auth/login" />
        <Stack.Screen name="auth/signup" />
        <Stack.Screen name="auth/google-callback" />
        <Stack.Screen name="(tabs)" />
        <Stack.Screen name="restaurant/[id]" />
        <Stack.Screen name="cart" />
        <Stack.Screen name="checkout" />
        <Stack.Screen name="rewards" />
        <Stack.Screen name="addresses" />
        <Stack.Screen name="payment-methods" />
        <Stack.Screen name="notifications" />
        <Stack.Screen name="my-reviews" />
        <Stack.Screen name="help" />
        <Stack.Screen name="order-tracking/[id]" />
      </Stack>
    </>
  );
}
