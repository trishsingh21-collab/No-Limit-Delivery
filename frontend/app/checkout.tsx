import React, { useState, useMemo } from 'react';
import {
  View, Text, StyleSheet, ScrollView, TouchableOpacity,
  TextInput, ActivityIndicator, Alert, KeyboardAvoidingView, Platform,
} from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Typography, Spacing, BorderRadius } from '../constants/Colors';
import { useCartStore, DELIVERY_FEE, TAX_RATE } from '../store/cartStore';
import { useAuthStore } from '../store/authStore';
import { api } from '../utils/api';
import MapPicker from '../components/MapPicker';

export default function CheckoutScreen() {
  const router = useRouter();
  const { items, getTotal, clearCart, getItemsByRestaurant, getRestaurants, getDeliveryFeeTotal, getGrandTotal } = useCartStore();
  const session_token = useAuthStore(state => state.session_token);

  const [pickupAddress, setPickupAddress] = useState({ street: '', city: '', zip: '', lat: 0, lng: 0 });
  const [deliveryAddress, setDeliveryAddress] = useState({ street: '', city: '', zip: '', instructions: '', lat: 0, lng: 0 });
  const [loading, setLoading] = useState(false);
  const [showPickupMap, setShowPickupMap] = useState(false);
  const [showDeliveryMap, setShowDeliveryMap] = useState(false);

  const grouped = getItemsByRestaurant();
  const restaurantIds = getRestaurants();
  const subtotal = getTotal();
  const deliveryFees = getDeliveryFeeTotal();
  const vat = subtotal * TAX_RATE;
  const total = getGrandTotal();

  // Detect if order includes parcel or laundry (needs pickup address)
  const needsPickup = useMemo(() => {
    return items.some(item => {
      const restItems = Object.entries(grouped).find(([_, rItems]) =>
        rItems.some(ri => ri.item_id === item.item_id)
      );
      return restItems !== undefined;
    });
  }, [items, grouped]);

  // Check if any service is parcel or laundry by checking restaurant names
  const hasParcelOrLaundry = useMemo(() => {
    return items.some(item =>
      item.restaurant_name.toLowerCase().includes('parcel') ||
      item.restaurant_name.toLowerCase().includes('laundry')
    );
  }, [items]);

  const handlePlaceOrder = async () => {
    if (!deliveryAddress.street && !deliveryAddress.lat) {
      Alert.alert('Missing Information', 'Please set your delivery address');
      return;
    }
    if (hasParcelOrLaundry && !pickupAddress.street && !pickupAddress.lat) {
      Alert.alert('Missing Information', 'Please set your pickup address');
      return;
    }
    if (!session_token) {
      Alert.alert('Login Required', 'Please login to place an order');
      return;
    }

    setLoading(true);
    try {
      const firstRestId = restaurantIds[0];
      const orderData = {
        restaurant_id: firstRestId,
        items: items.map(item => ({
          item_id: item.item_id, name: item.name, price: item.price, quantity: item.quantity,
        })),
        delivery_address: {
          street: deliveryAddress.street, city: deliveryAddress.city, zip: deliveryAddress.zip,
          instructions: deliveryAddress.instructions, lat: deliveryAddress.lat, lng: deliveryAddress.lng,
          ...(hasParcelOrLaundry ? {
            pickup_street: pickupAddress.street, pickup_city: pickupAddress.city,
            pickup_zip: pickupAddress.zip, pickup_lat: pickupAddress.lat, pickup_lng: pickupAddress.lng,
          } : {}),
        },
      };

      const order = await api.createOrder(session_token, orderData);
      clearCart();
      router.replace(`/order-tracking/${order.order_id}` as any);
    } catch (error: any) {
      Alert.alert('Order Failed', error.message || 'Could not place order');
    } finally {
      setLoading(false);
    }
  };

  if (items.length === 0) {
    return (
      <SafeAreaView style={styles.container} edges={['top']}>
        <View style={styles.emptyState}>
          <Ionicons name="cart-outline" size={80} color={Colors.lightGray} />
          <Text style={styles.emptyText}>Your cart is empty</Text>
          <TouchableOpacity style={styles.browseBtn} onPress={() => router.push('/(tabs)/home')}>
            <Text style={styles.browseBtnText}>Browse Providers</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : 'height'} style={{ flex: 1 }}>
        <View style={styles.header}>
          <TouchableOpacity testID="checkout-back-btn" onPress={() => router.back()} style={styles.backBtn}>
            <Ionicons name="arrow-back" size={24} color={Colors.textPrimary} />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Checkout</Text>
          <View style={{ width: 40 }} />
        </View>

        <ScrollView showsVerticalScrollIndicator={false}>
          {/* Order from */}
          <View style={styles.section}>
            {Object.entries(grouped).map(([restId, restItems]) => (
              <View key={restId} style={[styles.restaurantBanner, { marginBottom: 8 }]}>
                <Ionicons name="restaurant" size={20} color={Colors.sage} />
                <Text style={styles.restaurantName}>{restItems[0]?.restaurant_name}</Text>
                <Text style={styles.itemCount}>{restItems.length} items</Text>
              </View>
            ))}
          </View>

          {/* Pickup Address (for Parcel & Laundry) */}
          {hasParcelOrLaundry && (
            <View style={styles.section}>
              <View style={styles.sectionTitleRow}>
                <Ionicons name="arrow-up-circle" size={20} color={Colors.sage} />
                <Text style={styles.sectionTitle}>Pickup Address</Text>
              </View>
              <Text style={styles.sectionSubtitle}>Where should we collect from?</Text>

              <TouchableOpacity
                style={styles.mapToggle}
                onPress={() => setShowPickupMap(!showPickupMap)}
              >
                <Ionicons name="map" size={18} color={Colors.sage} />
                <Text style={styles.mapToggleText}>
                  {showPickupMap ? 'Hide Map' : 'Select on Map'}
                </Text>
              </TouchableOpacity>

              {showPickupMap && (
                <MapPicker
                  label="Tap to set pickup location"
                  onLocationSelect={(loc) => setPickupAddress({
                    ...pickupAddress, street: loc.address, lat: loc.lat, lng: loc.lng,
                  })}
                />
              )}

              <View style={styles.inputGroup}>
                <View style={styles.inputRow}>
                  <Ionicons name="location-outline" size={20} color={Colors.gray} />
                  <TextInput style={styles.input} placeholder="Pickup street address"
                    placeholderTextColor={Colors.gray} value={pickupAddress.street}
                    onChangeText={(t) => setPickupAddress({ ...pickupAddress, street: t })} />
                </View>
                <View style={styles.rowInputs}>
                  <View style={[styles.inputRow, { flex: 1 }]}>
                    <TextInput style={styles.input} placeholder="City" placeholderTextColor={Colors.gray}
                      value={pickupAddress.city} onChangeText={(t) => setPickupAddress({ ...pickupAddress, city: t })} />
                  </View>
                  <View style={[styles.inputRow, { flex: 0.5, marginLeft: Spacing.sm }]}>
                    <TextInput style={styles.input} placeholder="ZIP" placeholderTextColor={Colors.gray}
                      value={pickupAddress.zip} onChangeText={(t) => setPickupAddress({ ...pickupAddress, zip: t })} keyboardType="number-pad" />
                  </View>
                </View>
              </View>
            </View>
          )}

          {/* Delivery Address */}
          <View style={styles.section}>
            <View style={styles.sectionTitleRow}>
              <Ionicons name="arrow-down-circle" size={20} color={Colors.sage} />
              <Text style={styles.sectionTitle}>
                {hasParcelOrLaundry ? 'Delivery / Return Address' : 'Delivery Address'}
              </Text>
            </View>
            <Text style={styles.sectionSubtitle}>
              {hasParcelOrLaundry ? 'Where should we deliver to?' : 'Where should we bring your order?'}
            </Text>

            <TouchableOpacity
              style={styles.mapToggle}
              onPress={() => setShowDeliveryMap(!showDeliveryMap)}
            >
              <Ionicons name="map" size={18} color={Colors.sage} />
              <Text style={styles.mapToggleText}>
                {showDeliveryMap ? 'Hide Map' : 'Select on Map'}
              </Text>
            </TouchableOpacity>

            {showDeliveryMap && (
              <MapPicker
                label="Tap to set delivery location"
                onLocationSelect={(loc) => setDeliveryAddress({
                  ...deliveryAddress, street: loc.address, lat: loc.lat, lng: loc.lng,
                })}
              />
            )}

            <View style={styles.inputGroup}>
              <View style={styles.inputRow}>
                <Ionicons name="location-outline" size={20} color={Colors.gray} />
                <TextInput style={styles.input} placeholder="Delivery street address"
                  placeholderTextColor={Colors.gray} value={deliveryAddress.street}
                  onChangeText={(t) => setDeliveryAddress({ ...deliveryAddress, street: t })} />
              </View>
              <View style={styles.rowInputs}>
                <View style={[styles.inputRow, { flex: 1 }]}>
                  <TextInput style={styles.input} placeholder="City" placeholderTextColor={Colors.gray}
                    value={deliveryAddress.city} onChangeText={(t) => setDeliveryAddress({ ...deliveryAddress, city: t })} />
                </View>
                <View style={[styles.inputRow, { flex: 0.5, marginLeft: Spacing.sm }]}>
                  <TextInput style={styles.input} placeholder="ZIP" placeholderTextColor={Colors.gray}
                    value={deliveryAddress.zip} onChangeText={(t) => setDeliveryAddress({ ...deliveryAddress, zip: t })} keyboardType="number-pad" />
                </View>
              </View>
              <View style={styles.inputRow}>
                <Ionicons name="chatbubble-outline" size={20} color={Colors.gray} />
                <TextInput style={styles.input} placeholder="Delivery instructions (optional)"
                  placeholderTextColor={Colors.gray} value={deliveryAddress.instructions}
                  onChangeText={(t) => setDeliveryAddress({ ...deliveryAddress, instructions: t })} />
              </View>
            </View>
          </View>

          {/* Payment Method */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Payment Method</Text>
            <TouchableOpacity testID="payment-method-card" style={styles.paymentCard}>
              <View style={styles.paymentLeft}>
                <Ionicons name="card-outline" size={24} color={Colors.sage} />
                <View><Text style={styles.paymentTitle}>Credit/Debit Card</Text>
                <Text style={styles.paymentSub}>Pay on delivery</Text></View>
              </View>
              <Ionicons name="checkmark-circle" size={24} color={Colors.sage} />
            </TouchableOpacity>
          </View>

          {/* Order Summary */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Order Summary</Text>
            <View style={styles.summaryCard}>
              {items.map((item) => (
                <View key={item.item_id} style={styles.summaryItem}>
                  <Text style={styles.summaryItemName}>{item.quantity}x {item.name}</Text>
                  <Text style={styles.summaryItemPrice}>R{(item.price * item.quantity).toFixed(2)}</Text>
                </View>
              ))}
              <View style={styles.divider} />
              <View style={styles.summaryRow}>
                <Text style={styles.summaryLabel}>Subtotal</Text>
                <Text style={styles.summaryValue}>R{subtotal.toFixed(2)}</Text>
              </View>
              <View style={styles.summaryRow}>
                <Text style={styles.summaryLabel}>Delivery ({restaurantIds.length} x R25)</Text>
                <Text style={styles.summaryValue}>R{deliveryFees.toFixed(2)}</Text>
              </View>
              <View style={styles.summaryRow}>
                <Text style={styles.summaryLabel}>VAT (15%)</Text>
                <Text style={styles.summaryValue}>R{vat.toFixed(2)}</Text>
              </View>
              <View style={[styles.divider, { marginTop: Spacing.sm }]} />
              <View style={styles.totalRow}>
                <Text style={styles.totalLabel}>Total</Text>
                <Text style={styles.totalValue}>R{total.toFixed(2)}</Text>
              </View>
            </View>
          </View>

          <View style={{ height: 100 }} />
        </ScrollView>

        <View style={styles.footer}>
          <TouchableOpacity testID="place-order-button" style={styles.placeOrderBtn}
            onPress={handlePlaceOrder} disabled={loading}>
            {loading ? <ActivityIndicator color={Colors.white} /> :
              <Text style={styles.placeOrderText}>Place Order  •  R{total.toFixed(2)}</Text>}
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  emptyState: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  emptyText: { ...Typography.h4, color: Colors.textSecondary, marginTop: Spacing.md, marginBottom: Spacing.lg },
  browseBtn: { backgroundColor: Colors.sage, paddingVertical: Spacing.md, paddingHorizontal: Spacing.xl, borderRadius: BorderRadius.lg },
  browseBtnText: { ...Typography.button, color: Colors.white },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: Spacing.xl, paddingVertical: Spacing.md, borderBottomWidth: 1, borderBottomColor: Colors.border },
  backBtn: { padding: Spacing.sm },
  headerTitle: { ...Typography.h4, color: Colors.textPrimary },
  section: { paddingHorizontal: Spacing.xl, marginTop: Spacing.lg },
  sectionTitleRow: { flexDirection: 'row', alignItems: 'center', gap: Spacing.sm, marginBottom: 4 },
  sectionTitle: { ...Typography.h4, fontSize: 18, color: Colors.textPrimary },
  sectionSubtitle: { ...Typography.bodySmall, color: Colors.textSecondary, marginBottom: Spacing.md },
  mapToggle: { flexDirection: 'row', alignItems: 'center', gap: 6, paddingVertical: Spacing.sm, paddingHorizontal: Spacing.md, backgroundColor: Colors.sagePale, borderRadius: BorderRadius.lg, alignSelf: 'flex-start', marginBottom: Spacing.md },
  mapToggleText: { ...Typography.bodySmall, color: Colors.sage, fontWeight: '600' },
  restaurantBanner: { flexDirection: 'row', alignItems: 'center', backgroundColor: Colors.sagePale, padding: Spacing.md, borderRadius: BorderRadius.lg, gap: Spacing.sm },
  restaurantName: { ...Typography.body, fontWeight: '600', color: Colors.sageDark, flex: 1 },
  itemCount: { ...Typography.caption, color: Colors.sage, fontWeight: '600' },
  inputGroup: { gap: Spacing.sm },
  inputRow: { flexDirection: 'row', alignItems: 'center', borderWidth: 1, borderColor: Colors.border, borderRadius: BorderRadius.lg, paddingHorizontal: Spacing.md, backgroundColor: Colors.white },
  rowInputs: { flexDirection: 'row' },
  input: { flex: 1, ...Typography.body, paddingVertical: Spacing.md, color: Colors.textPrimary, marginLeft: Spacing.sm },
  paymentCard: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', padding: Spacing.md, borderWidth: 1, borderColor: Colors.sage, borderRadius: BorderRadius.lg, backgroundColor: Colors.white },
  paymentLeft: { flexDirection: 'row', alignItems: 'center', gap: Spacing.md },
  paymentTitle: { ...Typography.body, fontWeight: '600', color: Colors.textPrimary },
  paymentSub: { ...Typography.caption, color: Colors.textSecondary },
  summaryCard: { backgroundColor: Colors.white, borderRadius: BorderRadius.lg, padding: Spacing.md, borderWidth: 1, borderColor: Colors.border },
  summaryItem: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: Spacing.sm },
  summaryItemName: { ...Typography.body, color: Colors.textPrimary, flex: 1 },
  summaryItemPrice: { ...Typography.body, color: Colors.textPrimary },
  divider: { height: 1, backgroundColor: Colors.border, marginVertical: Spacing.sm },
  summaryRow: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: Spacing.xs },
  summaryLabel: { ...Typography.body, color: Colors.textSecondary },
  summaryValue: { ...Typography.body, color: Colors.textPrimary },
  totalRow: { flexDirection: 'row', justifyContent: 'space-between', marginTop: Spacing.sm },
  totalLabel: { ...Typography.body, fontWeight: '700', color: Colors.textPrimary },
  totalValue: { fontSize: 20, fontWeight: '700', color: Colors.sage },
  footer: { padding: Spacing.xl, borderTopWidth: 1, borderTopColor: Colors.border },
  placeOrderBtn: { backgroundColor: Colors.sage, paddingVertical: Spacing.md, borderRadius: BorderRadius.lg, alignItems: 'center' },
  placeOrderText: { ...Typography.button, color: Colors.white, fontSize: 17 },
});
