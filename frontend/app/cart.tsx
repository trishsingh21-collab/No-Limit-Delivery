import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Image,
  Alert,
} from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Typography, Spacing, BorderRadius } from '../constants/Colors';
import { useCartStore, DELIVERY_FEE, TAX_RATE } from '../store/cartStore';
import { useAuthStore } from '../store/authStore';

export default function CartScreen() {
  const router = useRouter();
  const { items, removeItem, updateQuantity, clearCart, clearRestaurant, getTotal, getItemsByRestaurant, getRestaurants, getDeliveryFeeTotal, getGrandTotal } = useCartStore();
  const isAuthenticated = useAuthStore(state => state.isAuthenticated);

  const subtotal = getTotal();
  const deliveryFees = getDeliveryFeeTotal();
  const vat = subtotal * TAX_RATE;
  const total = getGrandTotal();
  const grouped = getItemsByRestaurant();
  const restaurantIds = getRestaurants();

  const handleCheckout = () => {
    if (!isAuthenticated) {
      Alert.alert('Login Required', 'Please login to proceed with checkout', [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Login', onPress: () => router.push('/auth/login') },
      ]);
      return;
    }
    router.push('/checkout');
  };

  if (items.length === 0) {
    return (
      <SafeAreaView style={styles.container} edges={['top']}>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color={Colors.black} />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Cart</Text>
          <View style={{ width: 40 }} />
        </View>
        <View style={styles.emptyCart}>
          <Ionicons name="cart-outline" size={80} color={Colors.lightGray} />
          <Text style={styles.emptyText}>Your cart is empty</Text>
          <TouchableOpacity style={styles.browseButton} onPress={() => router.push('/(tabs)/home')}>
            <Text style={styles.browseButtonText}>Browse Restaurants</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Ionicons name="arrow-back" size={24} color={Colors.black} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Cart</Text>
        <TouchableOpacity onPress={clearCart}>
          <Text style={styles.clearText}>Clear All</Text>
        </TouchableOpacity>
      </View>

      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Multi-restaurant info banner */}
        {restaurantIds.length > 1 && (
          <View style={styles.multiBanner}>
            <Ionicons name="information-circle" size={18} color={Colors.sage} />
            <Text style={styles.multiBannerText}>
              Ordering from {restaurantIds.length} restaurants • R{DELIVERY_FEE.toFixed(0)} delivery each
            </Text>
          </View>
        )}

        {/* Items grouped by restaurant */}
        {Object.entries(grouped).map(([restId, restItems]) => {
          const restName = restItems[0]?.restaurant_name || 'Unknown';
          const restSubtotal = restItems.reduce((s, i) => s + i.price * i.quantity, 0);

          return (
            <View key={restId} style={styles.restaurantGroup}>
              <View style={styles.restaurantHeader}>
                <View style={styles.restaurantHeaderLeft}>
                  <Ionicons name="restaurant" size={18} color={Colors.sage} />
                  <Text style={styles.restaurantName}>{restName}</Text>
                </View>
                <TouchableOpacity onPress={() => clearRestaurant(restId)}>
                  <Text style={styles.removeRestText}>Remove</Text>
                </TouchableOpacity>
              </View>

              {restItems.map((item) => (
                <View key={item.item_id} style={styles.item}>
                  {item.image && (
                    <Image source={{ uri: item.image }} style={styles.itemImage} resizeMode="cover" />
                  )}
                  <View style={styles.itemInfo}>
                    <Text style={styles.itemName} numberOfLines={2}>{item.name}</Text>
                    <Text style={styles.itemPrice}>R{item.price.toFixed(2)}</Text>
                  </View>
                  <View style={styles.quantityControls}>
                    <TouchableOpacity style={styles.quantityButton} onPress={() => updateQuantity(item.item_id, item.quantity - 1)}>
                      <Ionicons name="remove" size={16} color={Colors.sage} />
                    </TouchableOpacity>
                    <Text style={styles.quantity}>{item.quantity}</Text>
                    <TouchableOpacity style={styles.quantityButton} onPress={() => updateQuantity(item.item_id, item.quantity + 1)}>
                      <Ionicons name="add" size={16} color={Colors.sage} />
                    </TouchableOpacity>
                  </View>
                </View>
              ))}

              <View style={styles.restSubtotal}>
                <Text style={styles.restSubtotalLabel}>Subtotal</Text>
                <Text style={styles.restSubtotalValue}>R{restSubtotal.toFixed(2)}</Text>
              </View>
              <View style={styles.restSubtotal}>
                <Text style={styles.restSubtotalLabel}>Delivery Fee</Text>
                <Text style={styles.restSubtotalValue}>R{DELIVERY_FEE.toFixed(2)}</Text>
              </View>
            </View>
          );
        })}

        {/* Order Summary */}
        <View style={styles.summary}>
          <View style={styles.summaryRow}>
            <Text style={styles.summaryLabel}>Subtotal</Text>
            <Text style={styles.summaryValue}>R{subtotal.toFixed(2)}</Text>
          </View>
          <View style={styles.summaryRow}>
            <Text style={styles.summaryLabel}>Delivery ({restaurantIds.length} x R{DELIVERY_FEE.toFixed(0)})</Text>
            <Text style={styles.summaryValue}>R{deliveryFees.toFixed(2)}</Text>
          </View>
          <View style={styles.summaryRow}>
            <Text style={styles.summaryLabel}>VAT (15%)</Text>
            <Text style={styles.summaryValue}>R{vat.toFixed(2)}</Text>
          </View>
          <View style={[styles.summaryRow, styles.totalRow]}>
            <Text style={styles.totalLabel}>Total</Text>
            <Text style={styles.totalValue}>R{total.toFixed(2)}</Text>
          </View>
        </View>
      </ScrollView>

      <View style={styles.footer}>
        <TouchableOpacity style={styles.checkoutButton} onPress={handleCheckout}>
          <Text style={styles.checkoutButtonText}>Proceed to Checkout  •  R{total.toFixed(2)}</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: Spacing.xl, paddingVertical: Spacing.md, borderBottomWidth: 1, borderBottomColor: Colors.border },
  backButton: { padding: Spacing.sm },
  headerTitle: { ...Typography.h4, color: Colors.textPrimary },
  clearText: { ...Typography.body, color: Colors.error },
  emptyCart: { flex: 1, justifyContent: 'center', alignItems: 'center', paddingHorizontal: Spacing.xl },
  emptyText: { ...Typography.h4, color: Colors.textSecondary, marginTop: Spacing.md, marginBottom: Spacing.lg },
  browseButton: { backgroundColor: Colors.sage, paddingVertical: Spacing.md, paddingHorizontal: Spacing.xl, borderRadius: BorderRadius.lg },
  browseButtonText: { ...Typography.button, color: Colors.white },
  multiBanner: { flexDirection: 'row', alignItems: 'center', marginHorizontal: Spacing.xl, marginTop: Spacing.md, padding: Spacing.md, backgroundColor: Colors.sagePale, borderRadius: BorderRadius.lg, gap: Spacing.sm },
  multiBannerText: { ...Typography.bodySmall, color: Colors.sageDark, flex: 1 },
  restaurantGroup: { marginHorizontal: Spacing.xl, marginTop: Spacing.md, borderWidth: 1, borderColor: Colors.border, borderRadius: BorderRadius.xl, overflow: 'hidden' },
  restaurantHeader: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', padding: Spacing.md, backgroundColor: Colors.surface },
  restaurantHeaderLeft: { flexDirection: 'row', alignItems: 'center', gap: Spacing.sm, flex: 1 },
  restaurantName: { ...Typography.body, fontWeight: '600', color: Colors.textPrimary },
  removeRestText: { ...Typography.caption, color: Colors.error },
  item: { flexDirection: 'row', alignItems: 'center', paddingVertical: Spacing.sm, paddingHorizontal: Spacing.md, borderBottomWidth: 1, borderBottomColor: Colors.borderLight },
  itemImage: { width: 50, height: 50, borderRadius: BorderRadius.md, backgroundColor: Colors.surface, marginRight: Spacing.sm },
  itemInfo: { flex: 1 },
  itemName: { ...Typography.bodySmall, color: Colors.textPrimary, marginBottom: 2 },
  itemPrice: { ...Typography.caption, color: Colors.textSecondary },
  quantityControls: { flexDirection: 'row', alignItems: 'center' },
  quantityButton: { width: 28, height: 28, borderRadius: 14, backgroundColor: Colors.sagePale, justifyContent: 'center', alignItems: 'center' },
  quantity: { ...Typography.body, fontWeight: '600', marginHorizontal: Spacing.sm, minWidth: 20, textAlign: 'center' },
  restSubtotal: { flexDirection: 'row', justifyContent: 'space-between', paddingHorizontal: Spacing.md, paddingVertical: Spacing.xs },
  restSubtotalLabel: { ...Typography.caption, color: Colors.textSecondary },
  restSubtotalValue: { ...Typography.caption, color: Colors.textSecondary, fontWeight: '600' },
  summary: { margin: Spacing.xl, padding: Spacing.md, backgroundColor: Colors.surface, borderRadius: BorderRadius.lg },
  summaryRow: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: Spacing.sm },
  summaryLabel: { ...Typography.body, color: Colors.textSecondary },
  summaryValue: { ...Typography.body, color: Colors.textPrimary },
  totalRow: { paddingTop: Spacing.sm, borderTopWidth: 1, borderTopColor: Colors.border, marginTop: Spacing.sm, marginBottom: 0 },
  totalLabel: { ...Typography.body, fontWeight: '700', color: Colors.textPrimary },
  totalValue: { fontSize: 20, fontWeight: '700', color: Colors.sage },
  footer: { padding: Spacing.xl, borderTopWidth: 1, borderTopColor: Colors.border },
  checkoutButton: { backgroundColor: Colors.sage, paddingVertical: Spacing.md, borderRadius: BorderRadius.lg, alignItems: 'center' },
  checkoutButtonText: { ...Typography.button, color: Colors.white },
});
