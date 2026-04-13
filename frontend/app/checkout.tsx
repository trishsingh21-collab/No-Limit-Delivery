import React, { useState, useMemo } from 'react';
import {
  View, Text, StyleSheet, ScrollView, TouchableOpacity,
  TextInput, ActivityIndicator, Alert, KeyboardAvoidingView, Platform,
  Linking,
} from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Typography, Spacing, BorderRadius } from '../constants/Colors';
import { useCartStore, DELIVERY_FEE, TAX_RATE } from '../store/cartStore';
import { useAuthStore } from '../store/authStore';
import { api } from '../utils/api';
import MapPicker from '../components/MapPicker';

type PaymentMethod = 'payfast' | 'cash' | 'eft';

const PAYMENT_METHODS: { key: PaymentMethod; icon: string; title: string; subtitle: string }[] = [
  { key: 'payfast', icon: 'card-outline', title: 'Pay Online (PayFast)', subtitle: 'Visa, Mastercard, SnapScan, EFT' },
  { key: 'cash', icon: 'cash-outline', title: 'Cash on Delivery', subtitle: 'Pay when your order arrives' },
  { key: 'eft', icon: 'swap-horizontal-outline', title: 'Manual EFT', subtitle: 'Transfer directly to our bank' },
];

const EFT_DETAILS = {
  bank: 'FNB (First National Bank)',
  accountName: 'No Limit Delivery (Pty) Ltd',
  accountNumber: '62875432190',
  branchCode: '250655',
  reference: 'Your order number',
};

const ALLERGY_OPTIONS = [
  'Nuts', 'Dairy', 'Gluten', 'Shellfish', 'Eggs', 'Soy', 'Sesame', 'Fish',
];

export default function CheckoutScreen() {
  const router = useRouter();
  const { items, getTotal, clearCart, getItemsByRestaurant, getRestaurants, getDeliveryFeeTotal, getGrandTotal } = useCartStore();
  const session_token = useAuthStore(state => state.session_token);

  const [pickupAddress, setPickupAddress] = useState({ street: '', city: '', zip: '', lat: 0, lng: 0 });
  const [deliveryAddress, setDeliveryAddress] = useState({ street: '', city: '', zip: '', instructions: '', lat: 0, lng: 0 });
  const [loading, setLoading] = useState(false);
  const [showPickupMap, setShowPickupMap] = useState(false);
  const [showDeliveryMap, setShowDeliveryMap] = useState(false);

  // Payment
  const [selectedPayment, setSelectedPayment] = useState<PaymentMethod>('payfast');

  // Notes & Allergies
  const [orderNotes, setOrderNotes] = useState('');
  const [selectedAllergies, setSelectedAllergies] = useState<string[]>([]);
  const [customAllergy, setCustomAllergy] = useState('');

  // Tip
  const [selectedTip, setSelectedTip] = useState<number>(0);
  const tipOptions = [0, 10, 15, 20, 30];

  // Promo Code
  const [promoCode, setPromoCode] = useState('');
  const [promoApplied, setPromoApplied] = useState(false);
  const [promoDiscount, setPromoDiscount] = useState(0);

  const grouped = getItemsByRestaurant();
  const restaurantIds = getRestaurants();
  const subtotal = getTotal();
  const deliveryFees = getDeliveryFeeTotal();
  const vat = subtotal * TAX_RATE;
  const total = getGrandTotal() + selectedTip - promoDiscount;

  const hasParcelOrLaundry = useMemo(() => {
    return items.some(item =>
      item.restaurant_name.toLowerCase().includes('parcel') ||
      item.restaurant_name.toLowerCase().includes('laundry')
    );
  }, [items]);

  // Estimated delivery time
  const estimatedTime = useMemo(() => {
    const hasFoodItems = items.some(i =>
      !i.restaurant_name.toLowerCase().includes('parcel') &&
      !i.restaurant_name.toLowerCase().includes('laundry') &&
      !i.restaurant_name.toLowerCase().includes('flower')
    );
    if (hasParcelOrLaundry) return '1-3 hours';
    if (hasFoodItems) return '30-50 min';
    return '2-4 hours';
  }, [items, hasParcelOrLaundry]);

  const toggleAllergy = (allergy: string) => {
    setSelectedAllergies(prev =>
      prev.includes(allergy) ? prev.filter(a => a !== allergy) : [...prev, allergy]
    );
  };

  const handleApplyPromo = () => {
    if (promoCode.toUpperCase() === 'NOLIMIT40') {
      const discount = subtotal * 0.4;
      setPromoDiscount(discount);
      setPromoApplied(true);
      Alert.alert('Promo Applied!', `R${discount.toFixed(2)} discount applied`);
    } else if (promoCode.trim()) {
      Alert.alert('Invalid Code', 'This promo code is not valid');
    }
  };

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
        payment_method: selectedPayment,
        order_notes: orderNotes,
        allergies: [...selectedAllergies, ...(customAllergy ? [customAllergy] : [])],
        tip: selectedTip,
        promo_code: promoApplied ? promoCode : undefined,
      };

      const order = await api.createOrder(session_token, orderData);

      // If PayFast selected, redirect to PayFast checkout
      if (selectedPayment === 'payfast') {
        try {
          const pfResponse = await api.createPayFastPayment(session_token, order.order_id);
          const { payfast_url, payment_data } = pfResponse;

          // Build the PayFast form URL with query params
          const params = new URLSearchParams();
          Object.entries(payment_data).forEach(([key, value]) => {
            params.append(key, String(value));
          });

          const fullUrl = `${payfast_url}?${params.toString()}`;
          clearCart();

          // Open PayFast in browser
          const canOpen = await Linking.canOpenURL(fullUrl);
          if (canOpen) {
            await Linking.openURL(fullUrl);
          } else {
            Alert.alert(
              'Payment',
              'Opening PayFast checkout...',
              [{ text: 'OK', onPress: () => Linking.openURL(fullUrl) }]
            );
          }
        } catch (pfError: any) {
          // PayFast failed but order was created - fallback to tracking
          Alert.alert(
            'Payment Issue',
            'Order created but payment redirect failed. You can pay from your order history.',
            [{ text: 'OK', onPress: () => router.replace(`/order-tracking/${order.order_id}` as any) }]
          );
        }
        return;
      }

      // Cash or EFT - go directly to tracking
      clearCart();
      if (selectedPayment === 'eft') {
        Alert.alert(
          'Order Placed - EFT Payment',
          `Please transfer R${total.toFixed(2)} to:\n\nBank: ${EFT_DETAILS.bank}\nAccount: ${EFT_DETAILS.accountNumber}\nBranch: ${EFT_DETAILS.branchCode}\nRef: ${order.order_id}\n\nYour order will be processed once payment is confirmed.`,
          [{ text: 'OK', onPress: () => router.replace(`/order-tracking/${order.order_id}` as any) }]
        );
      } else {
        router.replace(`/order-tracking/${order.order_id}` as any);
      }
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

        <ScrollView showsVerticalScrollIndicator={false} keyboardShouldPersistTaps="handled">
          {/* Estimated Delivery */}
          <View style={styles.estimateBar}>
            <Ionicons name="time-outline" size={18} color={Colors.sage} />
            <Text style={styles.estimateText}>Estimated delivery: <Text style={{ fontWeight: '700' }}>{estimatedTime}</Text></Text>
          </View>

          {/* Order from */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Order From</Text>
            {Object.entries(grouped).map(([restId, restItems]) => (
              <View key={restId} style={styles.restaurantBanner}>
                <Ionicons name="storefront-outline" size={20} color={Colors.sage} />
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

              <TouchableOpacity style={styles.mapToggle} onPress={() => setShowPickupMap(!showPickupMap)}>
                <Ionicons name="map" size={18} color={Colors.sage} />
                <Text style={styles.mapToggleText}>{showPickupMap ? 'Hide Map' : 'Select on Map'}</Text>
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

            <TouchableOpacity style={styles.mapToggle} onPress={() => setShowDeliveryMap(!showDeliveryMap)}>
              <Ionicons name="map" size={18} color={Colors.sage} />
              <Text style={styles.mapToggleText}>{showDeliveryMap ? 'Hide Map' : 'Select on Map'}</Text>
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
                <TextInput style={styles.input} placeholder="Delivery instructions (gate code, landmark...)"
                  placeholderTextColor={Colors.gray} value={deliveryAddress.instructions}
                  onChangeText={(t) => setDeliveryAddress({ ...deliveryAddress, instructions: t })} />
              </View>
            </View>
          </View>

          {/* Special Notes & Allergies */}
          <View style={styles.section}>
            <View style={styles.sectionTitleRow}>
              <Ionicons name="alert-circle-outline" size={20} color={Colors.sage} />
              <Text style={styles.sectionTitle}>Notes & Allergies</Text>
            </View>
            <Text style={styles.sectionSubtitle}>Let the restaurant know about any special requirements</Text>

            <View style={[styles.inputRow, { marginBottom: Spacing.md }]}>
              <Ionicons name="create-outline" size={20} color={Colors.gray} />
              <TextInput
                style={[styles.input, { minHeight: 60 }]}
                placeholder="Special instructions, exclusions, dietary needs..."
                placeholderTextColor={Colors.gray}
                value={orderNotes}
                onChangeText={setOrderNotes}
                multiline
                textAlignVertical="top"
              />
            </View>

            <Text style={styles.allergyLabel}>Common Allergies</Text>
            <View style={styles.allergyGrid}>
              {ALLERGY_OPTIONS.map((allergy) => (
                <TouchableOpacity
                  key={allergy}
                  style={[
                    styles.allergyChip,
                    selectedAllergies.includes(allergy) && styles.allergyChipActive,
                  ]}
                  onPress={() => toggleAllergy(allergy)}
                >
                  <Text style={[
                    styles.allergyChipText,
                    selectedAllergies.includes(allergy) && styles.allergyChipTextActive,
                  ]}>
                    {allergy}
                  </Text>
                  {selectedAllergies.includes(allergy) && (
                    <Ionicons name="close-circle" size={16} color={Colors.white} />
                  )}
                </TouchableOpacity>
              ))}
            </View>

            <View style={[styles.inputRow, { marginTop: Spacing.sm }]}>
              <Ionicons name="add-circle-outline" size={20} color={Colors.gray} />
              <TextInput
                style={styles.input}
                placeholder="Other allergy (type here)"
                placeholderTextColor={Colors.gray}
                value={customAllergy}
                onChangeText={setCustomAllergy}
              />
            </View>
          </View>

          {/* Payment Method */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Payment Method</Text>
            {PAYMENT_METHODS.map((method) => (
              <TouchableOpacity
                key={method.key}
                testID={`payment-${method.key}`}
                style={[
                  styles.paymentCard,
                  selectedPayment === method.key && styles.paymentCardActive,
                ]}
                onPress={() => setSelectedPayment(method.key)}
              >
                <View style={styles.paymentLeft}>
                  <View style={[
                    styles.paymentIconBox,
                    selectedPayment === method.key && styles.paymentIconBoxActive,
                  ]}>
                    <Ionicons
                      name={method.icon as any}
                      size={22}
                      color={selectedPayment === method.key ? Colors.white : Colors.sage}
                    />
                  </View>
                  <View>
                    <Text style={styles.paymentTitle}>{method.title}</Text>
                    <Text style={styles.paymentSub}>{method.subtitle}</Text>
                  </View>
                </View>
                <View style={[
                  styles.radioOuter,
                  selectedPayment === method.key && styles.radioOuterActive,
                ]}>
                  {selectedPayment === method.key && <View style={styles.radioInner} />}
                </View>
              </TouchableOpacity>
            ))}

            {/* EFT Bank Details */}
            {selectedPayment === 'eft' && (
              <View style={styles.eftDetails}>
                <Text style={styles.eftTitle}>Bank Transfer Details</Text>
                <View style={styles.eftRow}>
                  <Text style={styles.eftLabel}>Bank</Text>
                  <Text style={styles.eftValue}>{EFT_DETAILS.bank}</Text>
                </View>
                <View style={styles.eftRow}>
                  <Text style={styles.eftLabel}>Account Name</Text>
                  <Text style={styles.eftValue}>{EFT_DETAILS.accountName}</Text>
                </View>
                <View style={styles.eftRow}>
                  <Text style={styles.eftLabel}>Account No.</Text>
                  <Text style={styles.eftValue}>{EFT_DETAILS.accountNumber}</Text>
                </View>
                <View style={styles.eftRow}>
                  <Text style={styles.eftLabel}>Branch Code</Text>
                  <Text style={styles.eftValue}>{EFT_DETAILS.branchCode}</Text>
                </View>
                <View style={styles.eftRow}>
                  <Text style={styles.eftLabel}>Reference</Text>
                  <Text style={[styles.eftValue, { color: Colors.sage }]}>Your order number</Text>
                </View>
                <Text style={styles.eftNote}>Your order will be processed once payment is confirmed</Text>
              </View>
            )}
          </View>

          {/* Tip Your Driver */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Tip Your Driver</Text>
            <Text style={styles.sectionSubtitle}>100% of the tip goes to your driver</Text>
            <View style={styles.tipRow}>
              {tipOptions.map((tip) => (
                <TouchableOpacity
                  key={tip}
                  style={[styles.tipBtn, selectedTip === tip && styles.tipBtnActive]}
                  onPress={() => setSelectedTip(tip)}
                >
                  <Text style={[styles.tipBtnText, selectedTip === tip && styles.tipBtnTextActive]}>
                    {tip === 0 ? 'None' : `R${tip}`}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>

          {/* Promo Code */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Promo Code</Text>
            <View style={styles.promoRow}>
              <View style={[styles.inputRow, { flex: 1, marginBottom: 0 }]}>
                <Ionicons name="pricetag-outline" size={20} color={Colors.gray} />
                <TextInput
                  style={styles.input}
                  placeholder="Enter promo code"
                  placeholderTextColor={Colors.gray}
                  value={promoCode}
                  onChangeText={setPromoCode}
                  autoCapitalize="characters"
                  editable={!promoApplied}
                />
              </View>
              <TouchableOpacity
                style={[styles.promoApplyBtn, promoApplied && styles.promoAppliedBtn]}
                onPress={promoApplied ? () => { setPromoApplied(false); setPromoDiscount(0); setPromoCode(''); } : handleApplyPromo}
              >
                <Text style={styles.promoApplyText}>{promoApplied ? 'Remove' : 'Apply'}</Text>
              </TouchableOpacity>
            </View>
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
              {selectedTip > 0 && (
                <View style={styles.summaryRow}>
                  <Text style={styles.summaryLabel}>Driver Tip</Text>
                  <Text style={styles.summaryValue}>R{selectedTip.toFixed(2)}</Text>
                </View>
              )}
              {promoDiscount > 0 && (
                <View style={styles.summaryRow}>
                  <Text style={[styles.summaryLabel, { color: Colors.sage }]}>Promo Discount</Text>
                  <Text style={[styles.summaryValue, { color: Colors.sage }]}>-R{promoDiscount.toFixed(2)}</Text>
                </View>
              )}
              <View style={[styles.divider, { marginTop: Spacing.sm }]} />
              <View style={styles.totalRow}>
                <Text style={styles.totalLabel}>Total</Text>
                <Text style={styles.totalValue}>R{total.toFixed(2)}</Text>
              </View>
            </View>
          </View>

          {/* Selected allergies summary */}
          {(selectedAllergies.length > 0 || customAllergy) && (
            <View style={[styles.section, { marginBottom: Spacing.sm }]}>
              <View style={styles.allergySummary}>
                <Ionicons name="warning-outline" size={16} color="#E65100" />
                <Text style={styles.allergySummaryText}>
                  Allergies noted: {[...selectedAllergies, ...(customAllergy ? [customAllergy] : [])].join(', ')}
                </Text>
              </View>
            </View>
          )}

          <View style={{ height: 120 }} />
        </ScrollView>

        <View style={styles.footer}>
          <TouchableOpacity testID="place-order-button" style={styles.placeOrderBtn}
            onPress={handlePlaceOrder} disabled={loading}>
            {loading ? <ActivityIndicator color={Colors.white} /> : (
              <View style={styles.placeOrderContent}>
                <Ionicons name={
                  selectedPayment === 'cash' ? 'cash-outline' :
                  selectedPayment === 'eft' ? 'swap-horizontal-outline' : 'card-outline'
                } size={20} color={Colors.white} />
                <Text style={styles.placeOrderText}>
                  {selectedPayment === 'cash' ? 'Place Order (Cash)' :
                   selectedPayment === 'eft' ? 'Place Order (EFT)' :
                   'Pay with PayFast'}
                </Text>
                <Text style={styles.placeOrderPrice}>R{total.toFixed(2)}</Text>
              </View>
            )}
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

  estimateBar: { flexDirection: 'row', alignItems: 'center', marginHorizontal: Spacing.xl, marginTop: Spacing.md, padding: Spacing.md, backgroundColor: Colors.sagePale, borderRadius: BorderRadius.lg, gap: Spacing.sm },
  estimateText: { ...Typography.bodySmall, color: Colors.sageDark },

  section: { paddingHorizontal: Spacing.xl, marginTop: Spacing.lg },
  sectionTitleRow: { flexDirection: 'row', alignItems: 'center', gap: Spacing.sm, marginBottom: 4 },
  sectionTitle: { ...Typography.h4, fontSize: 18, color: Colors.textPrimary, marginBottom: Spacing.sm },
  sectionSubtitle: { ...Typography.bodySmall, color: Colors.textSecondary, marginBottom: Spacing.md },
  restaurantBanner: { flexDirection: 'row', alignItems: 'center', backgroundColor: Colors.white, padding: Spacing.md, borderRadius: BorderRadius.lg, gap: Spacing.sm, marginBottom: Spacing.xs, borderWidth: 1, borderColor: Colors.border },
  restaurantName: { ...Typography.body, fontWeight: '600', color: Colors.textPrimary, flex: 1 },
  itemCount: { ...Typography.caption, color: Colors.sage, fontWeight: '600', backgroundColor: Colors.sagePale, paddingHorizontal: 8, paddingVertical: 2, borderRadius: 10 },

  mapToggle: { flexDirection: 'row', alignItems: 'center', gap: 6, paddingVertical: Spacing.sm, paddingHorizontal: Spacing.md, backgroundColor: Colors.sagePale, borderRadius: BorderRadius.lg, alignSelf: 'flex-start', marginBottom: Spacing.md },
  mapToggleText: { ...Typography.bodySmall, color: Colors.sage, fontWeight: '600' },
  inputGroup: { gap: Spacing.sm },
  inputRow: { flexDirection: 'row', alignItems: 'center', borderWidth: 1, borderColor: Colors.border, borderRadius: BorderRadius.lg, paddingHorizontal: Spacing.md, backgroundColor: Colors.white },
  rowInputs: { flexDirection: 'row' },
  input: { flex: 1, ...Typography.body, paddingVertical: Spacing.md, color: Colors.textPrimary, marginLeft: Spacing.sm },

  // Notes & Allergies
  allergyLabel: { ...Typography.bodySmall, fontWeight: '600', color: Colors.textPrimary, marginBottom: Spacing.sm },
  allergyGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: Spacing.sm },
  allergyChip: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 14, paddingVertical: 8, borderRadius: 20, backgroundColor: Colors.white, borderWidth: 1, borderColor: Colors.border, gap: 4 },
  allergyChipActive: { backgroundColor: '#E65100', borderColor: '#E65100' },
  allergyChipText: { ...Typography.bodySmall, color: Colors.textSecondary },
  allergyChipTextActive: { color: Colors.white, fontWeight: '600' },

  allergySummary: { flexDirection: 'row', alignItems: 'center', padding: Spacing.md, backgroundColor: '#FFF3E0', borderRadius: BorderRadius.lg, gap: Spacing.sm },
  allergySummaryText: { ...Typography.bodySmall, color: '#E65100', flex: 1 },

  // Payment
  paymentCard: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', padding: Spacing.md, borderWidth: 1, borderColor: Colors.border, borderRadius: BorderRadius.lg, backgroundColor: Colors.white, marginBottom: Spacing.sm },
  paymentCardActive: { borderColor: Colors.sage, backgroundColor: Colors.sagePale },
  paymentLeft: { flexDirection: 'row', alignItems: 'center', gap: Spacing.md },
  paymentIconBox: { width: 44, height: 44, borderRadius: 12, backgroundColor: Colors.sagePale, justifyContent: 'center', alignItems: 'center' },
  paymentIconBoxActive: { backgroundColor: Colors.sage },
  paymentTitle: { ...Typography.body, fontWeight: '600', color: Colors.textPrimary },
  paymentSub: { ...Typography.caption, color: Colors.textSecondary },
  radioOuter: { width: 22, height: 22, borderRadius: 11, borderWidth: 2, borderColor: Colors.border, justifyContent: 'center', alignItems: 'center' },
  radioOuterActive: { borderColor: Colors.sage },
  radioInner: { width: 12, height: 12, borderRadius: 6, backgroundColor: Colors.sage },

  // EFT Details
  eftDetails: { backgroundColor: Colors.white, borderRadius: BorderRadius.lg, padding: Spacing.md, borderWidth: 1, borderColor: Colors.border, marginTop: Spacing.xs },
  eftTitle: { ...Typography.body, fontWeight: '700', color: Colors.textPrimary, marginBottom: Spacing.sm },
  eftRow: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: Spacing.xs },
  eftLabel: { ...Typography.bodySmall, color: Colors.textSecondary },
  eftValue: { ...Typography.bodySmall, fontWeight: '600', color: Colors.textPrimary },
  eftNote: { ...Typography.caption, color: Colors.textSecondary, marginTop: Spacing.sm, fontStyle: 'italic' },

  // Tips
  tipRow: { flexDirection: 'row', gap: Spacing.sm },
  tipBtn: { flex: 1, paddingVertical: 12, borderRadius: BorderRadius.lg, backgroundColor: Colors.white, alignItems: 'center', borderWidth: 1, borderColor: Colors.border },
  tipBtnActive: { backgroundColor: Colors.sage, borderColor: Colors.sage },
  tipBtnText: { ...Typography.bodySmall, fontWeight: '600', color: Colors.textSecondary },
  tipBtnTextActive: { color: Colors.white },

  // Promo
  promoRow: { flexDirection: 'row', gap: Spacing.sm, alignItems: 'center' },
  promoApplyBtn: { backgroundColor: Colors.sage, paddingVertical: Spacing.md, paddingHorizontal: Spacing.lg, borderRadius: BorderRadius.lg },
  promoAppliedBtn: { backgroundColor: Colors.error },
  promoApplyText: { ...Typography.bodySmall, fontWeight: '600', color: Colors.white },

  // Order Summary
  summaryCard: { backgroundColor: Colors.white, borderRadius: BorderRadius.lg, padding: Spacing.md, borderWidth: 1, borderColor: Colors.border },
  summaryItem: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: Spacing.sm },
  summaryItemName: { ...Typography.bodySmall, color: Colors.textPrimary, flex: 1 },
  summaryItemPrice: { ...Typography.bodySmall, color: Colors.textPrimary, fontWeight: '600' },
  divider: { height: 1, backgroundColor: Colors.border, marginVertical: Spacing.sm },
  summaryRow: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: Spacing.xs },
  summaryLabel: { ...Typography.body, color: Colors.textSecondary },
  summaryValue: { ...Typography.body, color: Colors.textPrimary },
  totalRow: { flexDirection: 'row', justifyContent: 'space-between', marginTop: Spacing.sm },
  totalLabel: { ...Typography.body, fontWeight: '700', color: Colors.textPrimary },
  totalValue: { fontSize: 22, fontWeight: '700', color: Colors.sage },

  // Footer
  footer: { padding: Spacing.xl, borderTopWidth: 1, borderTopColor: Colors.border, backgroundColor: Colors.background },
  placeOrderBtn: { backgroundColor: Colors.sage, paddingVertical: 16, borderRadius: BorderRadius.lg, alignItems: 'center' },
  placeOrderContent: { flexDirection: 'row', alignItems: 'center', gap: Spacing.sm },
  placeOrderText: { ...Typography.button, color: Colors.white, fontSize: 16 },
  placeOrderPrice: { ...Typography.button, color: 'rgba(255,255,255,0.8)', fontSize: 16 },
});
