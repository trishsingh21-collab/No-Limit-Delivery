import { useEffect } from 'react';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { useAuthStore } from '../store/authStore';
import { Colors } from '../constants/Colors';

export default function RootLayout() {
  const loadUser = useAuthStore(state => state.loadUser);
  
  useEffect(() => {
    loadUser();
  }, []);
  
  return (
    <>
      <StatusBar style="dark" />
      <Stack
        screenOptions={{
          headerShown: false,
          contentStyle: { backgroundColor: Colors.white },
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
