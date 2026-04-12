import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Image,
  Dimensions,
  RefreshControl,
  ActivityIndicator,
} from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Typography, Spacing, BorderRadius } from '../../constants/Colors';
import { api } from '../../utils/api';
import { useAuthStore } from '../../store/authStore';
import { useCartStore } from '../../store/cartStore';

const { width } = Dimensions.get('window');
const CARD_WIDTH = width - Spacing.xl * 2;

export default function HomeScreen() {
  const router = useRouter();
  const user = useAuthStore(state => state.user);
  const itemCount = useCartStore(state => state.getItemCount());
  const [featuredRestaurants, setFeaturedRestaurants] = useState<any[]>([]);
  const [allRestaurants, setAllRestaurants] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  
  const categories = [
    { name: 'Pizza', icon: 'pizza', cuisine: 'Italian' },
    { name: 'Burgers', icon: 'fast-food', cuisine: 'American' },
    { name: 'Sushi', icon: 'fish', cuisine: 'Japanese' },
    { name: 'Healthy', icon: 'leaf', cuisine: 'Healthy' },
    { name: 'Desserts', icon: 'ice-cream', cuisine: 'Desserts' },
    { name: 'Chinese', icon: 'restaurant', cuisine: 'Chinese' },
  ];
  
  const loadData = async () => {
    try {
      const [featured, all] = await Promise.all([
        api.getRestaurants({ featured: true }),
        api.getRestaurants({}),
      ]);
      setFeaturedRestaurants(featured);
      setAllRestaurants(all);
    } catch (error) {
      console.error('Error loading restaurants:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };
  
  useEffect(() => {
    loadData();
  }, []);
  
  const onRefresh = () => {
    setRefreshing(true);
    loadData();
  };
  
  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size=\"large\" color={Colors.sage} />
      </View>
    );
  }
  
  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <ScrollView
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={Colors.sage} />
        }
      >
        {/* Header */}
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>Hello, {user?.name || 'Guest'}!</Text>
            <Text style={styles.subtitle}>What would you like to eat today?</Text>
          </View>
          <TouchableOpacity
            style={styles.cartButton}
            onPress={() => router.push('/cart')}
          >
            <Ionicons name=\"cart\" size={24} color={Colors.black} />
            {itemCount > 0 && (
              <View style={styles.cartBadge}>
                <Text style={styles.cartBadgeText}>{itemCount}</Text>
              </View>
            )}
          </TouchableOpacity>
        </View>
        
        {/* AI Features */}
        <View style={styles.aiSection}>
          <TouchableOpacity
            style={styles.aiCard}
            onPress={() => router.push('/search?tab=randomizer')}
          >
            <Ionicons name=\"dice\" size={24} color={Colors.sage} />
            <Text style={styles.aiCardText}>What should I eat?</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.aiCard}
            onPress={() => router.push('/search?tab=mood')}
          >
            <Ionicons name=\"happy\" size={24} color={Colors.sage} />
            <Text style={styles.aiCardText}>Mood-based</Text>
          </TouchableOpacity>
        </View>
        
        {/* Categories */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Categories</Text>
          <ScrollView
            horizontal
            showsHorizontalScrollIndicator={false}
            style={styles.categoriesScroll}
          >
            {categories.map((category, index) => (
              <TouchableOpacity
                key={index}
                style={styles.categoryCard}
                onPress={() => router.push(`/search?cuisine=${category.cuisine}`)}
              >
                <View style={styles.categoryIcon}>
                  <Ionicons name={category.icon as any} size={28} color={Colors.sage} />
                </View>
                <Text style={styles.categoryName}>{category.name}</Text>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </View>
        
        {/* Featured Restaurants */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Featured</Text>
            <TouchableOpacity onPress={() => router.push('/search')}>
              <Text style={styles.seeAll}>See All</Text>
            </TouchableOpacity>
          </View>
          <ScrollView
            horizontal
            showsHorizontalScrollIndicator={false}
            style={styles.featuredScroll}
          >
            {featuredRestaurants.map((restaurant) => (
              <TouchableOpacity
                key={restaurant.restaurant_id}
                style={styles.featuredCard}
                onPress={() => router.push(`/restaurant/${restaurant.restaurant_id}`)}
              >
                <Image
                  source={{ uri: restaurant.image }}
                  style={styles.featuredImage}
                  resizeMode=\"cover\"
                />
                <View style={styles.featuredInfo}>
                  <Text style={styles.restaurantName}>{restaurant.name}</Text>
                  <View style={styles.restaurantMeta}>
                    <Ionicons name=\"star\" size={14} color={Colors.sage} />
                    <Text style={styles.rating}>{restaurant.rating}</Text>
                    <Text style={styles.metaDivider}>•</Text>
                    <Text style={styles.deliveryTime}>{restaurant.delivery_time}</Text>
                    <Text style={styles.metaDivider}>•</Text>
                    <Text style={styles.priceRange}>{restaurant.price_range}</Text>
                  </View>
                  <Text style={styles.cuisine}>{restaurant.cuisine_type}</Text>
                </View>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </View>
        
        {/* All Restaurants */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>All Restaurants</Text>
          <View style={styles.restaurantList}>
            {allRestaurants.slice(0, 10).map((restaurant) => (
              <TouchableOpacity
                key={restaurant.restaurant_id}
                style={styles.restaurantCard}
                onPress={() => router.push(`/restaurant/${restaurant.restaurant_id}`)}
              >
                <Image
                  source={{ uri: restaurant.image }}
                  style={styles.restaurantImage}
                  resizeMode=\"cover\"
                />
                <View style={styles.restaurantInfo}>
                  <Text style={styles.restaurantNameSmall}>{restaurant.name}</Text>
                  <Text style={styles.description} numberOfLines={2}>
                    {restaurant.description}
                  </Text>
                  <View style={styles.restaurantMeta}>
                    <Ionicons name=\"star\" size={14} color={Colors.sage} />
                    <Text style={styles.rating}>{restaurant.rating}</Text>
                    <Text style={styles.metaDivider}>•</Text>
                    <Text style={styles.deliveryTime}>{restaurant.delivery_time}</Text>
                    <Text style={styles.metaDivider}>•</Text>
                    <Text style={styles.priceRange}>{restaurant.price_range}</Text>
                  </View>
                </View>
              </TouchableOpacity>
            ))}
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.white,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: Colors.white,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: Spacing.xl,
    paddingTop: Spacing.md,
    paddingBottom: Spacing.lg,
  },
  greeting: {
    ...Typography.h3,
    color: Colors.black,
  },
  subtitle: {
    ...Typography.bodySmall,
    color: Colors.textSecondary,
    marginTop: Spacing.xs,
  },
  cartButton: {
    position: 'relative',
    padding: Spacing.sm,
  },
  cartBadge: {
    position: 'absolute',
    top: 4,
    right: 4,
    backgroundColor: Colors.sage,
    borderRadius: 10,
    minWidth: 18,
    height: 18,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 4,
  },
  cartBadgeText: {
    color: Colors.white,
    fontSize: 10,
    fontWeight: '600',
  },
  aiSection: {
    flexDirection: 'row',
    paddingHorizontal: Spacing.xl,
    gap: Spacing.md,
    marginBottom: Spacing.lg,
  },
  aiCard: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: Colors.sagePale,
    padding: Spacing.md,
    borderRadius: BorderRadius.lg,
    gap: Spacing.sm,
  },
  aiCardText: {
    ...Typography.bodySmall,
    color: Colors.sageDark,
    fontWeight: '600',
  },
  section: {
    marginBottom: Spacing.lg,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: Spacing.xl,
    marginBottom: Spacing.md,
  },
  sectionTitle: {
    ...Typography.h4,
    color: Colors.black,
    paddingHorizontal: Spacing.xl,
    marginBottom: Spacing.md,
  },
  seeAll: {
    ...Typography.bodySmall,
    color: Colors.sage,
    fontWeight: '600',
  },
  categoriesScroll: {
    paddingLeft: Spacing.xl,
  },
  categoryCard: {
    alignItems: 'center',
    marginRight: Spacing.md,
    width: 80,
  },
  categoryIcon: {
    width: 64,
    height: 64,
    borderRadius: BorderRadius.full,
    backgroundColor: Colors.sagePale,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: Spacing.xs,
  },
  categoryName: {
    ...Typography.caption,
    color: Colors.textSecondary,
    textAlign: 'center',
  },
  featuredScroll: {
    paddingLeft: Spacing.xl,
  },
  featuredCard: {
    width: CARD_WIDTH * 0.7,
    marginRight: Spacing.md,
    backgroundColor: Colors.white,
    borderRadius: BorderRadius.lg,
    overflow: 'hidden',
    elevation: 2,
    shadowColor: Colors.black,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  featuredImage: {
    width: '100%',
    height: 160,
    backgroundColor: Colors.paleGray,
  },
  featuredInfo: {
    padding: Spacing.md,
  },
  restaurantName: {
    ...Typography.h4,
    fontSize: 18,
    color: Colors.black,
    marginBottom: Spacing.xs,
  },
  restaurantMeta: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: Spacing.xs,
  },
  rating: {
    ...Typography.bodySmall,
    color: Colors.textSecondary,
    marginLeft: 4,
  },
  metaDivider: {
    ...Typography.bodySmall,
    color: Colors.lightGray,
    marginHorizontal: 6,
  },
  deliveryTime: {
    ...Typography.bodySmall,
    color: Colors.textSecondary,
  },
  priceRange: {
    ...Typography.bodySmall,
    color: Colors.textSecondary,
  },
  cuisine: {
    ...Typography.caption,
    color: Colors.sage,
  },
  restaurantList: {
    paddingHorizontal: Spacing.xl,
  },
  restaurantCard: {
    flexDirection: 'row',
    backgroundColor: Colors.white,
    borderRadius: BorderRadius.lg,
    marginBottom: Spacing.md,
    overflow: 'hidden',
    elevation: 1,
    shadowColor: Colors.black,
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
  },
  restaurantImage: {
    width: 100,
    height: 100,
    backgroundColor: Colors.paleGray,
  },
  restaurantInfo: {
    flex: 1,
    padding: Spacing.md,
  },
  restaurantNameSmall: {
    ...Typography.body,
    fontWeight: '600',
    color: Colors.black,
    marginBottom: Spacing.xs,
  },
  description: {
    ...Typography.caption,
    color: Colors.textSecondary,
    marginBottom: Spacing.xs,
  },
});
