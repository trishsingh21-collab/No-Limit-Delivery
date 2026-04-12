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

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  session_token: null,
  isAuthenticated: false,
  isLoading: true,
  
  login: async (user: User, token: string) => {
    await AsyncStorage.setItem('session_token', token);
    set({ user, session_token: token, isAuthenticated: true });
  },
  
  logout: async () => {
    await AsyncStorage.removeItem('session_token');
    set({ user: null, session_token: null, isAuthenticated: false });
  },
  
  loadUser: async () => {
    try {
      const token = await AsyncStorage.getItem('session_token');
      if (token) {
        set({ session_token: token, isLoading: false });
        // Will verify with /api/auth/me on app load
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
