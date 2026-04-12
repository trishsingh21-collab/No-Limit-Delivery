import React, { useEffect, useState, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
} from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Typography, Spacing, BorderRadius } from '../../constants/Colors';
import { api } from '../../utils/api';
import { useAuthStore } from '../../store/authStore';
import Constants from 'expo-constants';
import { io, Socket } from 'socket.io-client';
import { StaggerItem, FadeInView, Pulse, BounceInView } from '../../components/animated';
import Animated, { FadeIn, FadeInDown } from 'react-native-reanimated';

const BACKEND_URL = process.env.EXPO_PUBLIC_BACKEND_URL || '';

const ORDER_STATUSES = [
  { key: 'pending', label: 'Order Placed', icon: 'receipt-outline' as const },
  { key: 'confirmed', label: 'Confirmed', icon: 'checkmark-circle-outline' as const },
  { key: 'preparing', label: 'Preparing', icon: 'restaurant-outline' as const },
  { key: 'ready', label: 'Ready', icon: 'checkmark-done-outline' as const },
  { key: 'picked_up', label: 'On the Way', icon: 'bicycle-outline' as const },
  { key: 'delivered', label: 'Delivered', icon: 'checkmark-done-circle' as const },
];

export default function OrderTrackingScreen() {
  const router = useRouter();
  const { id } = useLocalSearchParams();
  const session_token = useAuthStore(state => state.session_token);
  const [order, setOrder] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const socketRef = useRef<Socket | null>(null);

  useEffect(() => {
    loadOrder();
    connectSocket();

    return () => {
      if (socketRef.current?.connected) {
        socketRef.current.disconnect();
      }
    };
  }, [id]);

  const loadOrder = async () => {
    if (!session_token) return;
    try {
      const data = await api.getOrder(session_token, id as string);
      setOrder(data);
    } catch (error) {
      console.error('Error loading order:', error);
    } finally {
      setLoading(false);
    }
  };

  const connectSocket = () => {
    if (!BACKEND_URL) return;

    socketRef.current = io(BACKEND_URL, {
      path: '/api/socket.io',
      transports: ['websocket', 'polling'],
    });

    socketRef.current.on('connect', () => {
      console.log('Socket connected for order tracking');
      socketRef.current?.emit('join_order_room', { order_id: id });
    });

    socketRef.current.on('order_update', (data: any) => {
      console.log('Order update received:', data);
      setOrder(data);
    });

    socketRef.current.on('disconnect', () => {
      console.log('Socket disconnected');
    });
  };

  const getStatusIndex = (status: string) => {
    return ORDER_STATUSES.findIndex(s => s.key === status);
  };

  const currentStatusIndex = order ? getStatusIndex(order.status) : 0;

  const getEstimatedTime = () => {
    if (!order) return '';
    if (order.status === 'delivered') return 'Delivered!';
    if (order.status === 'cancelled') return 'Cancelled';

    const estimateMinutes = order.status === 'pending' ? 40
      : order.status === 'confirmed' ? 35
      : order.status === 'preparing' ? 25
      : order.status === 'ready' ? 15
      : order.status === 'picked_up' ? 10 : 0;

    return estimateMinutes > 0 ? `~${estimateMinutes} min` : '';
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={Colors.sage} />
      </View>
    );
  }

  if (!order) {
    return (
      <SafeAreaView style={styles.container} edges={['top']}>
        <View style={styles.loadingContainer}>
          <Ionicons name="alert-circle-outline" size={64} color={Colors.lightGray} />
          <Text style={styles.errorText}>Order not found</Text>
          <TouchableOpacity
            style={styles.homeBtn}
            onPress={() => router.push('/(tabs)/home')}
          >
            <Text style={styles.homeBtnText}>Go Home</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity testID="tracking-back-btn" onPress={() => router.back()} style={styles.backBtn}>
          <Ionicons name="arrow-back" size={24} color={Colors.black} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Order Tracking</Text>
        <View style={{ width: 40 }} />
      </View>

      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Status Card */}
        <Animated.View entering={FadeInDown.delay(100).duration(400).springify()} style={styles.statusCard}>
          <View style={styles.statusHeader}>
            <Text style={styles.statusTitle}>
              {order.status === 'delivered' ? 'Order Delivered!' :
               order.status === 'cancelled' ? 'Order Cancelled' :
               'Your order is on its way'}
            </Text>
            {getEstimatedTime() ? (
              <View style={styles.etaBadge}>
                <Ionicons name="time-outline" size={16} color={Colors.sage} />
                <Text style={styles.etaText}>{getEstimatedTime()}</Text>
              </View>
            ) : null}
          </View>

          <Text style={styles.orderId}>Order #{order.order_id.slice(-8).toUpperCase()}</Text>
        </Animated.View>

        {/* Progress Tracker */}
        <View style={styles.progressSection}>
          <Text style={styles.sectionTitle}>Order Progress</Text>
          <View style={styles.timeline}>
            {ORDER_STATUSES.map((status, index) => {
              const isCompleted = index <= currentStatusIndex;
              const isCurrent = index === currentStatusIndex;
              const isLast = index === ORDER_STATUSES.length - 1;

              return (
                <StaggerItem key={status.key} index={index} delay={100}>
                <View style={styles.timelineItem}>
                  <View style={styles.timelineLeft}>
                    {isCurrent ? (
                    <Pulse active={true}>
                    <View
                      style={[
                        styles.timelineDot,
                        isCompleted && styles.timelineDotCompleted,
                        isCurrent && styles.timelineDotCurrent,
                      ]}
                    >
                      <Ionicons
                        name={isCompleted ? 'checkmark' : (status.icon as any)}
                        size={isCurrent ? 18 : 14}
                        color={isCompleted ? Colors.white : Colors.lightGray}
                      />
                    </View>
                    </Pulse>
                    ) : (
                    <View
                      style={[
                        styles.timelineDot,
                        isCompleted && styles.timelineDotCompleted,
                      ]}
                    >
                      <Ionicons
                        name={isCompleted ? 'checkmark' : (status.icon as any)}
                        size={14}
                        color={isCompleted ? Colors.white : Colors.lightGray}
                      />
                    </View>
                    )}
                    {!isLast && (
                      <View
                        style={[
                          styles.timelineLine,
                          isCompleted && index < currentStatusIndex && styles.timelineLineCompleted,
                        ]}
                      />
                    )}
                  </View>
                  <View style={styles.timelineContent}>
                    <Text
                      style={[
                        styles.timelineLabel,
                        isCompleted && styles.timelineLabelCompleted,
                        isCurrent && styles.timelineLabelCurrent,
                      ]}
                    >
                      {status.label}
                    </Text>
                    {isCurrent && (
                      <Text style={styles.timelineSubtext}>In progress...</Text>
                    )}
                  </View>
                </View>
                </StaggerItem>
              );
            })}
          </View>
        </View>

        {/* Order Details */}
        <View style={styles.detailsSection}>
          <Text style={styles.sectionTitle}>Order Details</Text>

          <View style={styles.detailCard}>
            <View style={styles.detailRow}>
              <Ionicons name="restaurant" size={18} color={Colors.sage} />
              <Text style={styles.detailLabel}>{order.restaurant_name}</Text>
            </View>

            {order.items?.map((item: any, index: number) => (
              <View key={index} style={styles.orderItem}>
                <Text style={styles.orderItemName}>
                  {item.quantity}x {item.name}
                </Text>
                <Text style={styles.orderItemPrice}>
                  ${(item.price * item.quantity).toFixed(2)}
                </Text>
              </View>
            ))}

            <View style={styles.divider} />

            <View style={styles.totalRow}>
              <Text style={styles.totalLabel}>Total</Text>
              <Text style={styles.totalValue}>R{order.total?.toFixed(2)}</Text>
            </View>
          </View>

          {/* Delivery Address */}
          {order.delivery_address && (
            <View style={styles.addressCard}>
              <Ionicons name="location" size={20} color={Colors.sage} />
              <View style={styles.addressInfo}>
                <Text style={styles.addressTitle}>Delivery Address</Text>
                <Text style={styles.addressText}>
                  {order.delivery_address.street}
                  {order.delivery_address.city ? `, ${order.delivery_address.city}` : ''}
                  {order.delivery_address.zip ? ` ${order.delivery_address.zip}` : ''}
                </Text>
              </View>
            </View>
          )}
        </View>

        <View style={{ height: Spacing.xxl * 2 }} />
      </ScrollView>

      {/* Bottom Button */}
      <View style={styles.footer}>
        {order.status === 'delivered' ? (
          <TouchableOpacity
            testID="order-again-btn"
            style={styles.orderAgainBtn}
            onPress={() => router.push(`/restaurant/${order.restaurant_id}`)}
          >
            <Ionicons name="refresh" size={20} color={Colors.white} />
            <Text style={styles.orderAgainText}>Order Again</Text>
          </TouchableOpacity>
        ) : (
          <TouchableOpacity
            testID="back-to-home-btn"
            style={[styles.orderAgainBtn, { backgroundColor: Colors.charcoal }]}
            onPress={() => router.push('/(tabs)/home')}
          >
            <Ionicons name="home" size={20} color={Colors.white} />
            <Text style={styles.orderAgainText}>Back to Home</Text>
          </TouchableOpacity>
        )}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: Colors.background,
  },
  errorText: {
    ...Typography.h4,
    color: Colors.textSecondary,
    marginTop: Spacing.md,
  },
  homeBtn: {
    backgroundColor: Colors.sage,
    paddingVertical: Spacing.md,
    paddingHorizontal: Spacing.xl,
    borderRadius: BorderRadius.lg,
    marginTop: Spacing.lg,
  },
  homeBtnText: {
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
    color: Colors.textPrimary,
  },
  statusCard: {
    margin: Spacing.xl,
    padding: Spacing.lg,
    backgroundColor: Colors.sagePale,
    borderRadius: BorderRadius.xl,
  },
  statusHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: Spacing.sm,
  },
  statusTitle: {
    ...Typography.h4,
    color: Colors.sageDark,
    flex: 1,
  },
  etaBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.background,
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.xs,
    borderRadius: BorderRadius.full,
    gap: 4,
  },
  etaText: {
    ...Typography.bodySmall,
    fontWeight: '600',
    color: Colors.sage,
  },
  orderId: {
    ...Typography.caption,
    color: Colors.textSecondary,
  },
  progressSection: {
    paddingHorizontal: Spacing.xl,
    marginBottom: Spacing.lg,
  },
  sectionTitle: {
    ...Typography.h4,
    fontSize: 18,
    color: Colors.textPrimary,
    marginBottom: Spacing.md,
  },
  timeline: {
    paddingLeft: Spacing.sm,
  },
  timelineItem: {
    flexDirection: 'row',
    minHeight: 60,
  },
  timelineLeft: {
    alignItems: 'center',
    width: 40,
  },
  timelineDot: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: Colors.surface,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: Colors.border,
  },
  timelineDotCompleted: {
    backgroundColor: Colors.sage,
    borderColor: Colors.sage,
  },
  timelineDotCurrent: {
    width: 36,
    height: 36,
    borderRadius: 18,
    borderWidth: 3,
    borderColor: Colors.sage,
    backgroundColor: Colors.sage,
    elevation: 2,
    shadowColor: Colors.sage,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
  },
  timelineLine: {
    width: 2,
    flex: 1,
    backgroundColor: Colors.border,
    marginVertical: 4,
  },
  timelineLineCompleted: {
    backgroundColor: Colors.sage,
  },
  timelineContent: {
    flex: 1,
    paddingLeft: Spacing.md,
    paddingTop: 6,
  },
  timelineLabel: {
    ...Typography.body,
    color: Colors.textSecondary,
  },
  timelineLabelCompleted: {
    color: Colors.sage,
    fontWeight: '600',
  },
  timelineLabelCurrent: {
    color: Colors.textPrimary,
    fontWeight: '700',
  },
  timelineSubtext: {
    ...Typography.caption,
    color: Colors.sage,
    marginTop: 2,
  },
  detailsSection: {
    paddingHorizontal: Spacing.xl,
  },
  detailCard: {
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.lg,
    padding: Spacing.md,
    marginBottom: Spacing.md,
  },
  detailRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.sm,
    marginBottom: Spacing.md,
  },
  detailLabel: {
    ...Typography.body,
    fontWeight: '600',
    color: Colors.textPrimary,
  },
  orderItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: Spacing.sm,
  },
  orderItemName: {
    ...Typography.bodySmall,
    color: Colors.textSecondary,
    flex: 1,
  },
  orderItemPrice: {
    ...Typography.bodySmall,
    color: Colors.textPrimary,
  },
  divider: {
    height: 1,
    backgroundColor: Colors.border,
    marginVertical: Spacing.sm,
  },
  totalRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  totalLabel: {
    ...Typography.body,
    fontWeight: '700',
    color: Colors.textPrimary,
  },
  totalValue: {
    fontSize: 18,
    fontWeight: '700',
    color: Colors.sage,
  },
  addressCard: {
    flexDirection: 'row',
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.lg,
    padding: Spacing.md,
    gap: Spacing.md,
  },
  addressInfo: {
    flex: 1,
  },
  addressTitle: {
    ...Typography.bodySmall,
    fontWeight: '600',
    color: Colors.textPrimary,
    marginBottom: 2,
  },
  addressText: {
    ...Typography.bodySmall,
    color: Colors.textSecondary,
  },
  footer: {
    padding: Spacing.xl,
    borderTopWidth: 1,
    borderTopColor: Colors.border,
  },
  orderAgainBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: Colors.sage,
    paddingVertical: Spacing.md,
    borderRadius: BorderRadius.lg,
    gap: Spacing.sm,
  },
  orderAgainText: {
    ...Typography.button,
    color: Colors.white,
  },
});
