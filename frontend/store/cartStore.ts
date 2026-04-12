import { create } from 'zustand';

interface CartItem {
  item_id: string;
  name: string;
  price: number;
  quantity: number;
  special_instructions?: string;
  restaurant_id: string;
  restaurant_name: string;
  image?: string;
}

interface CartState {
  items: CartItem[];
  restaurant_id: string | null;
  restaurant_name: string | null;
  addItem: (item: CartItem) => void;
  removeItem: (item_id: string) => void;
  updateQuantity: (item_id: string, quantity: number) => void;
  clearCart: () => void;
  getTotal: () => number;
  getItemCount: () => number;
}

export const useCartStore = create<CartState>((set, get) => ({
  items: [],
  restaurant_id: null,
  restaurant_name: null,
  
  addItem: (item: CartItem) => {
    const state = get();
    
    // Check if adding from different restaurant
    if (state.restaurant_id && state.restaurant_id !== item.restaurant_id) {
      // Clear cart when switching restaurants
      set({
        items: [item],
        restaurant_id: item.restaurant_id,
        restaurant_name: item.restaurant_name,
      });
      return;
    }
    
    // Check if item already in cart
    const existingItem = state.items.find(i => i.item_id === item.item_id);
    
    if (existingItem) {
      set({
        items: state.items.map(i =>
          i.item_id === item.item_id
            ? { ...i, quantity: i.quantity + item.quantity }
            : i
        ),
      });
    } else {
      set({
        items: [...state.items, item],
        restaurant_id: item.restaurant_id,
        restaurant_name: item.restaurant_name,
      });
    }
  },
  
  removeItem: (item_id: string) => {
    const state = get();
    const newItems = state.items.filter(i => i.item_id !== item_id);
    
    set({
      items: newItems,
      restaurant_id: newItems.length > 0 ? state.restaurant_id : null,
      restaurant_name: newItems.length > 0 ? state.restaurant_name : null,
    });
  },
  
  updateQuantity: (item_id: string, quantity: number) => {
    if (quantity <= 0) {
      get().removeItem(item_id);
      return;
    }
    
    set({
      items: get().items.map(i =>
        i.item_id === item_id ? { ...i, quantity } : i
      ),
    });
  },
  
  clearCart: () => {
    set({ items: [], restaurant_id: null, restaurant_name: null });
  },
  
  getTotal: () => {
    return get().items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  },
  
  getItemCount: () => {
    return get().items.reduce((sum, item) => sum + item.quantity, 0);
  },
}));
