import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  ActivityIndicator,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Typography, Spacing, BorderRadius } from '../constants/Colors';
import { useCartStore } from '../store/cartStore';
import { useAuthStore } from '../store/authStore';
import { api } from '../utils/api';

export default function CheckoutScreen() {
  const router = useRouter();
  const { items, restaurant_id, restaurant_name, getTotal, clearCart } = useCartStore();
  const session_token = useAuthStore(state => state.session_token);

  const [address, setAddress] = useState({
    street: '',
    city: '',
    zip: '',
    instructions: '',
  });
  const [loading, setLoading] = useState(false);

  const subtotal = getTotal();
  const deliveryFee = 3.99;
  const tax = subtotal * 0.08;
  const total = subtotal + deliveryFee + tax;

  const handlePlaceOrder = async () => {
    if (!address.street || !address.city || !address.zip) {
      Alert.alert('Missing Information', 'Please fill in your delivery address');
      return;
    }

    if (!session_token) {
      Alert.alert('Login Required', 'Please login to place an order');
      return;
    }

    setLoading(true);
    try {
      const orderData = {
        restaurant_id: restaurant_id,
        items: items.map(item => ({
          item_id: item.item_id,
          name: item.name,
          price: item.price,
          quantity: item.quantity,
        })),
        delivery_address: {
          street: address.street,
          city: address.city,
          zip: address.zip,
          instructions: address.instructions,
        },
      };

      const order = await api.createOrder(session_token, orderData);
      clearCart();
      router.replace(`/order-tracking/${order.order_id}`);
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
          <TouchableOpacity
            style={styles.browseBtn}
            onPress={() => router.push('/(tabs)/home')}
          >
            <Text style={styles.browseBtnText}>Browse Restaurants</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={{ flex: 1 }}
      >
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity testID="checkout-back-btn" onPress={() => router.back()} style={styles.backBtn}>
            <Ionicons name="arrow-back" size={24} color={Colors.black} />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Checkout</Text>
          <View style={{ width: 40 }} />
        </View>

        <ScrollView showsVerticalScrollIndicator={false}>
          {/* Order from */}
          <View style={styles.section}>
            <View style={styles.restaurantBanner}>
              <Ionicons name="restaurant" size={20} color={Colors.sage} />
              <Text style={styles.restaurantName}>{restaurant_name}</Text>
            </View>
          </View>

          {/* Delivery Address */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Delivery Address</Text>
            <View style={styles.inputGroup}>
              <View style={styles.inputRow}>
                <Ionicons name="location-outline" size={20} color={Colors.gray} />
                <TextInput
                  testID="address-street-input"
                  style={styles.input}
                  placeholder="Street address"
                  placeholderTextColor={Colors.gray}
                  value={address.street}
                  onChangeText={(text) => setAddress({ ...address, street: text })}
                />
              </View>
              <View style={styles.rowInputs}>
                <View style={[styles.inputRow, { flex: 1 }]}>
                  <TextInput
                    testID="address-city-input"
                    style={styles.input}
                    placeholder="City"
                    placeholderTextColor={Colors.gray}
                    value={address.city}
                    onChangeText={(text) => setAddress({ ...address, city: text })}
                  />
                </View>
                <View style={[styles.inputRow, { flex: 0.5, marginLeft: Spacing.sm }]}>
                  <TextInput
                    testID="address-zip-input"
                    style={styles.input}
                    placeholder="ZIP"
                    placeholderTextColor={Colors.gray}
                    value={address.zip}
                    onChangeText={(text) => setAddress({ ...address, zip: text })}
                    keyboardType="number-pad"
                  />
                </View>
              </View>
              <View style={styles.inputRow}>
                <Ionicons name="chatbubble-outline" size={20} color={Colors.gray} />
                <TextInput
                  testID="address-instructions-input"
                  style={styles.input}
                  placeholder="Delivery instructions (optional)"
                  placeholderTextColor={Colors.gray}
                  value={address.instructions}
                  onChangeText={(text) => setAddress({ ...address, instructions: text })}
                />
              </View>
            </View>
          </View>

          {/* Payment Method */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Payment Method</Text>
            <TouchableOpacity testID="payment-method-card" style={styles.paymentCard}>
              <View style={styles.paymentLeft}>
                <Ionicons name="card-outline" size={24} color={Colors.sage} />
                <View style={styles.paymentInfo}>
                  <Text style={styles.paymentTitle}>Credit/Debit Card</Text>
                  <Text style={styles.paymentSub}>Pay on delivery</Text>
                </View>
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
                  <Text style={styles.summaryItemName}>
                    {item.quantity}x {item.name}
                  </Text>
                  <Text style={styles.summaryItemPrice}>
                    ${(item.price * item.quantity).toFixed(2)}
                  </Text>
                </View>
              ))}

              <View style={styles.divider} />

              <View style={styles.summaryRow}>
                <Text style={styles.summaryLabel}>Subtotal</Text>
                <Text style={styles.summaryValue}>${subtotal.toFixed(2)}</Text>
              </View>
              <View style={styles.summaryRow}>
                <Text style={styles.summaryLabel}>Delivery Fee</Text>
                <Text style={styles.summaryValue}>${deliveryFee.toFixed(2)}</Text>
              </View>
              <View style={styles.summaryRow}>
                <Text style={styles.summaryLabel}>Tax</Text>
                <Text style={styles.summaryValue}>${tax.toFixed(2)}</Text>
              </View>

              <View style={[styles.divider, { marginTop: Spacing.sm }]} />

              <View style={styles.totalRow}>
                <Text style={styles.totalLabel}>Total</Text>
                <Text style={styles.totalValue}>${total.toFixed(2)}</Text>
              </View>
            </View>
          </View>

          <View style={{ height: 100 }} />
        </ScrollView>

        {/* Place Order Button */}
        <View style={styles.footer}>
          <TouchableOpacity
            testID="place-order-button"
            style={styles.placeOrderBtn}
            onPress={handlePlaceOrder}
            disabled={loading}
          >
            {loading ? (
              <ActivityIndicator color={Colors.white} />
            ) : (
              <Text style={styles.placeOrderText}>
                Place Order  •  ${total.toFixed(2)}
              </Text>
            )}
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.white,
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  emptyText: {
    ...Typography.h4,
    color: Colors.textSecondary,
    marginTop: Spacing.md,
    marginBottom: Spacing.lg,
  },
  browseBtn: {
    backgroundColor: Colors.sage,
    paddingVertical: Spacing.md,
    paddingHorizontal: Spacing.xl,
    borderRadius: BorderRadius.lg,
  },
  browseBtnText: {
    ...Typography.button,
    color: Colors.white,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: Spacing.xl,
    paddingVertical: Spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  backBtn: {
    padding: Spacing.sm,
  },
  headerTitle: {
    ...Typography.h4,
    color: Colors.black,
  },
  section: {
    paddingHorizontal: Spacing.xl,
    marginTop: Spacing.lg,
  },
  sectionTitle: {
    ...Typography.h4,
    fontSize: 18,
    color: Colors.black,
    marginBottom: Spacing.md,
  },
  restaurantBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.sagePale,
    padding: Spacing.md,
    borderRadius: BorderRadius.lg,
    gap: Spacing.sm,
  },
  restaurantName: {
    ...Typography.body,
    fontWeight: '600',
    color: Colors.sageDark,
  },
  inputGroup: {
    gap: Spacing.sm,
  },
  inputRow: {
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: Colors.border,
    borderRadius: BorderRadius.lg,
    paddingHorizontal: Spacing.md,
    backgroundColor: Colors.white,
  },
  rowInputs: {
    flexDirection: 'row',
  },
  input: {
    flex: 1,
    ...Typography.body,
    paddingVertical: Spacing.md,
    color: Colors.black,
    marginLeft: Spacing.sm,
  },
  paymentCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: Spacing.md,
    borderWidth: 1,
    borderColor: Colors.sage,
    borderRadius: BorderRadius.lg,
    backgroundColor: '#F8FBF8',
  },
  paymentLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.md,
  },
  paymentInfo: {},
  paymentTitle: {
    ...Typography.body,
    fontWeight: '600',
    color: Colors.black,
  },
  paymentSub: {
    ...Typography.caption,
    color: Colors.textSecondary,
  },
  summaryCard: {
    backgroundColor: Colors.paleGray,
    borderRadius: BorderRadius.lg,
    padding: Spacing.md,
  },
  summaryItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: Spacing.sm,
  },
  summaryItemName: {
    ...Typography.body,
    color: Colors.black,
    flex: 1,
  },
  summaryItemPrice: {
    ...Typography.body,
    color: Colors.black,
  },
  divider: {
    height: 1,
    backgroundColor: Colors.border,
    marginVertical: Spacing.sm,
  },
  summaryRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: Spacing.xs,
  },
  summaryLabel: {
    ...Typography.body,
    color: Colors.textSecondary,
  },
  summaryValue: {
    ...Typography.body,
    color: Colors.black,
  },
  totalRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: Spacing.sm,
  },
  totalLabel: {
    ...Typography.body,
    fontWeight: '700',
    color: Colors.black,
  },
  totalValue: {
    fontSize: 20,
    fontWeight: '700',
    color: Colors.sage,
  },
  footer: {
    padding: Spacing.xl,
    borderTopWidth: 1,
    borderTopColor: Colors.border,
  },
  placeOrderBtn: {
    backgroundColor: Colors.sage,
    paddingVertical: Spacing.md,
    borderRadius: BorderRadius.lg,
    alignItems: 'center',
  },
  placeOrderText: {
    ...Typography.button,
    color: Colors.white,
    fontSize: 17,
  },
});
