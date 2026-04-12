import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  RefreshControl,
  ActivityIndicator,
} from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Typography, Spacing, BorderRadius } from '../../constants/Colors';
import { api } from '../../utils/api';
import { useAuthStore } from '../../store/authStore';
import { format } from 'date-fns';

export default function OrdersScreen() {
  const router = useRouter();
  const session_token = useAuthStore(state => state.session_token);
  const [orders, setOrders] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  
  const loadOrders = async () => {
    if (!session_token) return;
    
    try {
      const data = await api.getOrders(session_token);
      setOrders(data);
    } catch (error) {
      console.error('Error loading orders:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };
  
  useEffect(() => {
    loadOrders();
  }, [session_token]);
  
  const onRefresh = () => {
    setRefreshing(true);
    loadOrders();
  };
  
  const getStatusColor = (status: string) => {
    const colors: any = {
      pending: Colors.warning,
      confirmed: Colors.sage,
      preparing: Colors.sage,
      ready: Colors.sage,
      picked_up: Colors.sage,
      delivered: Colors.success,
      cancelled: Colors.error,
    };
    return colors[status] || Colors.gray;
  };
  
  const getStatusIcon = (status: string) => {
    const icons: any = {
      pending: 'time-outline',
      confirmed: 'checkmark-circle-outline',
      preparing: 'restaurant-outline',
      ready: 'checkmark-done-outline',
      picked_up: 'bicycle-outline',
      delivered: 'checkmark-done-circle',
      cancelled: 'close-circle-outline',
    };
    return icons[status] || 'ellipse-outline';
  };
  
  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={Colors.sage} />
      </View>
    );
  }
  
  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>My Orders</Text>
      </View>
      
      <ScrollView
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={Colors.sage} />
        }
      >
        {orders.length === 0 ? (
          <View style={styles.emptyState}>
            <Ionicons name="receipt-outline" size={64} color={Colors.lightGray} />
            <Text style={styles.emptyText}>No orders yet</Text>
            <Text style={styles.emptySubtext}>Start exploring restaurants!</Text>
            <TouchableOpacity
              style={styles.browseButton}
              onPress={() => router.push('/(tabs)/home')}
            >
              <Text style={styles.browseButtonText}>Browse Restaurants</Text>
            </TouchableOpacity>
          </View>
        ) : (
          <View style={styles.ordersList}>
            {orders.map((order) => (
              <TouchableOpacity
                key={order.order_id}
                style={styles.orderCard}
                onPress={() => router.push(`/order-tracking/${order.order_id}`)}
              >
                <View style={styles.orderHeader}>
                  <Text style={styles.restaurantName}>{order.restaurant_name}</Text>
                  <View style={[styles.statusBadge, { backgroundColor: getStatusColor(order.status) + '20' }]}>
                    <Ionicons
                      name={getStatusIcon(order.status) as any}
                      size={14}
                      color={getStatusColor(order.status)}
                    />
                    <Text style={[styles.statusText, { color: getStatusColor(order.status) }]}>
                      {order.status.replace('_', ' ').toUpperCase()}
                    </Text>
                  </View>
                </View>
                
                <View style={styles.orderDetails}>
                  {order.items.slice(0, 2).map((item: any, index: number) => (
                    <Text key={index} style={styles.itemText}>
                      {item.quantity}x {item.name}
                    </Text>
                  ))}
                  {order.items.length > 2 && (
                    <Text style={styles.moreItems}>+{order.items.length - 2} more items</Text>
                  )}
                </View>
                
                <View style={styles.orderFooter}>
                  <Text style={styles.orderDate}>
                    {format(new Date(order.created_at), 'MMM d, yyyy • h:mm a')}
                  </Text>
                  <Text style={styles.orderTotal}>R{order.total.toFixed(2)}</Text>
                </View>
              </TouchableOpacity>
            ))}
          </View>
        )}
      </ScrollView>
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
  header: {
    paddingHorizontal: Spacing.xl,
    paddingTop: Spacing.md,
    paddingBottom: Spacing.md,
  },
  headerTitle: {
    ...Typography.h3,
    color: Colors.textPrimary,
  },
  emptyState: {
    alignItems: 'center',
    paddingVertical: Spacing.xxl * 2,
    paddingHorizontal: Spacing.xl,
  },
  emptyText: {
    ...Typography.h4,
    color: Colors.textPrimary,
    marginTop: Spacing.md,
  },
  emptySubtext: {
    ...Typography.body,
    color: Colors.textSecondary,
    marginTop: Spacing.xs,
  },
  browseButton: {
    backgroundColor: Colors.sage,
    paddingVertical: Spacing.md,
    paddingHorizontal: Spacing.xl,
    borderRadius: BorderRadius.lg,
    marginTop: Spacing.lg,
  },
  browseButtonText: {
    ...Typography.button,
    color: Colors.white,
  },
  ordersList: {
    paddingHorizontal: Spacing.xl,
    paddingBottom: Spacing.xxl,
  },
  orderCard: {
    backgroundColor: Colors.background,
    borderRadius: BorderRadius.lg,
    padding: Spacing.md,
    marginBottom: Spacing.md,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  orderHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: Spacing.sm,
  },
  restaurantName: {
    ...Typography.body,
    fontWeight: '600',
    color: Colors.textPrimary,
    flex: 1,
  },
  statusBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: Spacing.sm,
    paddingVertical: 4,
    borderRadius: BorderRadius.sm,
    gap: 4,
  },
  statusText: {
    ...Typography.caption,
    fontWeight: '600',
  },
  orderDetails: {
    marginBottom: Spacing.sm,
  },
  itemText: {
    ...Typography.bodySmall,
    color: Colors.textSecondary,
    marginBottom: 2,
  },
  moreItems: {
    ...Typography.caption,
    color: Colors.sage,
    marginTop: 2,
  },
  orderFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingTop: Spacing.sm,
    borderTopWidth: 1,
    borderTopColor: Colors.borderLight,
  },
  orderDate: {
    ...Typography.caption,
    color: Colors.textSecondary,
  },
  orderTotal: {
    ...Typography.body,
    fontWeight: '600',
    color: Colors.textPrimary,
  },
});
