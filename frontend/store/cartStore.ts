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
  addItem: (item: CartItem) => void;
  removeItem: (item_id: string) => void;
  updateQuantity: (item_id: string, quantity: number) => void;
  clearCart: () => void;
  clearRestaurant: (restaurant_id: string) => void;
  getTotal: () => number;
  getItemCount: () => number;
  getRestaurants: () => string[];
  getItemsByRestaurant: () => Record<string, CartItem[]>;
  getRestaurantTotal: (restaurant_id: string) => number;
  getDeliveryFeeTotal: () => number;
  getGrandTotal: () => number;
}

const DELIVERY_FEE_LOCAL = 30.00;  // Within 5km
const DELIVERY_FEE_FAR = 35.00;   // 5km or more
const DELIVERY_FEE_PER_RESTAURANT = DELIVERY_FEE_LOCAL; // Default to local
const VAT_RATE = 0.15;

export const useCartStore = create<CartState>((set, get) => ({
  items: [],

  addItem: (item: CartItem) => {
    const state = get();
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
      set({ items: [...state.items, item] });
    }
  },

  removeItem: (item_id: string) => {
    set({ items: get().items.filter(i => i.item_id !== item_id) });
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
    set({ items: [] });
  },

  clearRestaurant: (restaurant_id: string) => {
    set({ items: get().items.filter(i => i.restaurant_id !== restaurant_id) });
  },

  getTotal: () => {
    return get().items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  },

  getItemCount: () => {
    return get().items.reduce((sum, item) => sum + item.quantity, 0);
  },

  getRestaurants: () => {
    const restaurantIds = new Set(get().items.map(i => i.restaurant_id));
    return Array.from(restaurantIds);
  },

  getItemsByRestaurant: () => {
    const grouped: Record<string, CartItem[]> = {};
    get().items.forEach(item => {
      if (!grouped[item.restaurant_id]) {
        grouped[item.restaurant_id] = [];
      }
      grouped[item.restaurant_id].push(item);
    });
    return grouped;
  },

  getRestaurantTotal: (restaurant_id: string) => {
    return get().items
      .filter(i => i.restaurant_id === restaurant_id)
      .reduce((sum, item) => sum + item.price * item.quantity, 0);
  },

  getDeliveryFeeTotal: () => {
    return get().getRestaurants().length * DELIVERY_FEE_PER_RESTAURANT;
  },

  getGrandTotal: () => {
    const subtotal = get().getTotal();
    const deliveryFees = get().getDeliveryFeeTotal();
    const vat = subtotal * VAT_RATE;
    return subtotal + deliveryFees + vat;
  },
}));

export const DELIVERY_FEE = DELIVERY_FEE_LOCAL;
export const DELIVERY_FEE_5KM_PLUS = DELIVERY_FEE_FAR;
export const TAX_RATE = VAT_RATE;
