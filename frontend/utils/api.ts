import { useAuthStore } from '../store/authStore';

const BACKEND_URL = process.env.EXPO_PUBLIC_BACKEND_URL || 'https://no-limit-delivery-production.up.railway.app';

export const api = {
  // Services
  getServices: async () => {
    const res = await fetch(`${BACKEND_URL}/api/services`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
  
  // Auth
  signup: async (email: string, password: string, name: string, phone?: string) => {
    const res = await fetch(`${BACKEND_URL}/api/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, name, phone }),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
  
  login: async (email: string, password: string) => {
    const res = await fetch(`${BACKEND_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
  
  googleSessionExchange: async (session_id: string) => {
    const res = await fetch(`${BACKEND_URL}/api/auth/google/session`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id }),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
  
  getMe: async (token: string) => {
    const res = await fetch(`${BACKEND_URL}/api/auth/me`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
  
  logout: async (token: string) => {
    const res = await fetch(`${BACKEND_URL}/api/auth/logout`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` },
    });
    return res.ok;
  },
  
  // Restaurants
  getRestaurants: async (params?: { cuisine?: string; featured?: boolean; search?: string }) => {
    const query = new URLSearchParams(params as any).toString();
    const res = await fetch(`${BACKEND_URL}/api/restaurants${query ? `?${query}` : ''}`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
  
  getRestaurant: async (id: string) => {
    const res = await fetch(`${BACKEND_URL}/api/restaurants/${id}`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
  
  getMenu: async (restaurantId: string, category?: string) => {
    const query = category ? `?category=${category}` : '';
    const res = await fetch(`${BACKEND_URL}/api/restaurants/${restaurantId}/menu${query}`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
  
  getReviews: async (restaurantId: string) => {
    const res = await fetch(`${BACKEND_URL}/api/restaurants/${restaurantId}/reviews`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
  
  // Orders
  createOrder: async (token: string, orderData: any) => {
    const res = await fetch(`${BACKEND_URL}/api/orders`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(orderData),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  createPayFastPayment: async (token: string, orderId: string) => {
    const res = await fetch(`${BACKEND_URL}/api/payments/payfast/create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ order_id: orderId }),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
  
  getOrders: async (token: string) => {
    const res = await fetch(`${BACKEND_URL}/api/orders`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
  
  getOrder: async (token: string, orderId: string) => {
    const res = await fetch(`${BACKEND_URL}/api/orders/${orderId}`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
  
  // AI Features
  getRecommendations: async (token: string) => {
    const res = await fetch(`${BACKEND_URL}/api/ai/recommendations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({}),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
  
  getRandomizer: async () => {
    const res = await fetch(`${BACKEND_URL}/api/ai/randomizer`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
  
  getMoodSuggestions: async (mood: string) => {
    const res = await fetch(`${BACKEND_URL}/api/ai/mood-suggestions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mood }),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
  
  // Profile
  getProfile: async (token: string) => {
    const res = await fetch(`${BACKEND_URL}/api/profile`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
  
  // Reviews
  createReview: async (token: string, reviewData: any) => {
    const res = await fetch(`${BACKEND_URL}/api/reviews`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(reviewData),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
};
