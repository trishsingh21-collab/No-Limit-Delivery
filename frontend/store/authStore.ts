import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface User {
  user_id: string;
  email: string;
  name: string;
  phone?: string;
  addresses?: any[];
  loyalty_points?: number;
}

interface AuthState {
  user: User | null;
  session_token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (user: User, token: string) => Promise<void>;
  logout: () => Promise<void>;
  loadUser: () => Promise<void>;
  updateUser: (user: User) => void;
}

const BACKEND_URL = process.env.EXPO_PUBLIC_BACKEND_URL || '';

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  session_token: null,
  isAuthenticated: false,
  isLoading: true,

  login: async (user: User, token: string) => {
    await AsyncStorage.setItem('session_token', token);
    set({ user, session_token: token, isAuthenticated: true, isLoading: false });
  },

  logout: async () => {
    await AsyncStorage.removeItem('session_token');
    set({ user: null, session_token: null, isAuthenticated: false });
  },

  loadUser: async () => {
    try {
      const token = await AsyncStorage.getItem('session_token');
      if (token) {
        // Verify token with backend
        const res = await fetch(`${BACKEND_URL}/api/auth/me`, {
          headers: { 'Authorization': `Bearer ${token}` },
        });
        if (res.ok) {
          const userData = await res.json();
          set({ user: userData, session_token: token, isAuthenticated: true, isLoading: false });
        } else {
          // Token invalid, clear it
          await AsyncStorage.removeItem('session_token');
          set({ isLoading: false });
        }
      } else {
        set({ isLoading: false });
      }
    } catch (error) {
      console.error('Failed to load user:', error);
      set({ isLoading: false });
    }
  },

  updateUser: (user: User) => {
    set({ user });
  },
}));
