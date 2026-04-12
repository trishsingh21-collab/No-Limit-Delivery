import React, { useEffect, useRef } from 'react';
import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { useAuthStore } from '../../store/authStore';
import { api } from '../../utils/api';
import { Colors, Typography, Spacing } from '../../constants/Colors';

export default function GoogleCallbackScreen() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const login = useAuthStore(state => state.login);
  const hasProcessed = useRef(false);
  
  useEffect(() => {
    if (hasProcessed.current) return;
    hasProcessed.current = true;
    
    const processSession = async () => {
      try {
        // Get session_id from URL fragment
        const hash = typeof window !== 'undefined' ? window.location.hash : '';
        const sessionId = hash.split('session_id=')[1]?.split('&')[0];
        
        if (!sessionId) {
          throw new Error('No session ID found');
        }
        
        // Exchange session_id for user data and app session
        const data = await api.googleSessionExchange(sessionId);
        
        // Login user
        await login(data.user, data.session_token);
        
        // Navigate to home
        router.replace('/(tabs)/home');
      } catch (error: any) {
        console.error('Google auth error:', error);
        // Navigate back to login on error
        router.replace('/auth/login');
      }
    };
    
    processSession();
  }, []);
  
  return (
    <View style={styles.container}>
      <ActivityIndicator size="large" color={Colors.sage} />
      <Text style={styles.text}>Completing sign in...</Text>
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
  text: {
    ...Typography.body,
    color: Colors.textSecondary,
    marginTop: Spacing.md,
  },
});
