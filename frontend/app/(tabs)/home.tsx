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
import Animated, { FadeIn, FadeInDown, FadeInLeft, FadeInRight, FadeInUp, SlideInLeft } from 'react-native-reanimated';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Typography, Spacing, BorderRadius } from '../../constants/Colors';
import { api } from '../../utils/api';
import { useAuthStore } from '../../store/authStore';
import { useCartStore } from '../../store/cartStore';
import { StaggerItem, SlideInView, FadeInView, BounceInView } from '../../components/animated';

const { width } = Dimensions.get('window');

const CATEGORIES = [
  { name: 'Chicken', emoji: '🍗', cuisine: 'Chicken' },
  { name: 'Pizza', emoji: '🍕', cuisine: 'Braai & BBQ' },
  { name: 'Braai', emoji: '🔥', cuisine: 'Braai & BBQ' },
  { name: 'Mexican', emoji: '🌮', cuisine: 'Mexican Chicken' },
  { name: 'Shawarma', emoji: '🌯', cuisine: 'Shawarma & Grill' },
  { name: 'Curry', emoji: '🍛', cuisine: 'Indian & Curry' },
  { name: 'Café', emoji: '☕', cuisine: 'Café & Coffee' },
  { name: 'Brunch', emoji: '🥐', cuisine: 'Café & Brunch' },
  { name: 'Meals', emoji: '🍱', cuisine: 'Home-Style Meals' },
  { name: 'Take-Away', emoji: '🍟', cuisine: 'Take-Away' },
];

const SERVICE_TABS = [
  { key: 'all', label: 'All', emoji: '🏠' },
  { key: 'food', label: 'Food', emoji: '🍔' },
  { key: 'laundry', label: 'Laundry', emoji: '👔' },
  { key: 'parcel', label: 'Parcels', emoji: '📦' },
  { key: 'florist', label: 'Flowers', emoji: '💐' },
  { key: 'pharmacy', label: 'Pharmacy', emoji: '💊' },
];

const getGreeting = () => {
  const hour = new Date().getHours();
  if (hour < 12) return 'Good morning';
  if (hour < 17) return 'Good afternoon';
  return 'Good evening';
};

export default function HomeScreen() {
  const router = useRouter();
  const user = useAuthStore(state => state.user);
  const itemCount = useCartStore(state => state.getItemCount());
  const [featuredRestaurants, setFeaturedRestaurants] = useState<any[]>([]);
  const [allRestaurants, setAllRestaurants] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [activeService, setActiveService] = useState('all');

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

  useEffect(() => { loadData(); }, []);

  const onRefresh = () => { setRefreshing(true); loadData(); };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={Colors.sage} />
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <ScrollView
        showsVerticalScrollIndicator={false}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={Colors.sage} />}
      >
        {/* Header - fade in */}
        <Animated.View entering={FadeIn.duration(300)} style={styles.header}>
          <View style={styles.headerLeft}>
            <Text style={styles.greeting}>{getGreeting()}</Text>
            <Text style={styles.userName}>{user?.name || 'Guest'} 👋</Text>
          </View>
          <TouchableOpacity testID="cart-button" style={styles.cartButton} onPress={() => router.push('/cart')}>
            <Ionicons name="cart-outline" size={26} color={Colors.black} />
            {itemCount > 0 && (
              <BounceInView style={styles.cartBadge}>
                <Text style={styles.cartBadgeText}>{itemCount}</Text>
              </BounceInView>
            )}
          </TouchableOpacity>
        </Animated.View>

        {/* Location */}
        <Animated.View entering={FadeIn.delay(100).duration(300)}>
          <TouchableOpacity style={styles.locationRow}>
            <Ionicons name="location" size={18} color={Colors.sage} />
            <Text style={styles.locationLabel}>Delivering to</Text>
            <Text style={styles.locationValue}>Current Location</Text>
            <Ionicons name="chevron-down" size={16} color={Colors.gray} />
          </TouchableOpacity>
        </Animated.View>

        {/* Search Bar */}
        <Animated.View entering={FadeInDown.delay(150).duration(400).springify()}>
          <TouchableOpacity testID="search-bar" style={styles.searchBar} onPress={() => router.push('/(tabs)/search')}>
            <Ionicons name="search" size={20} color={Colors.gray} />
            <Text style={styles.searchPlaceholder}>Search restaurants, food...</Text>
            <TouchableOpacity style={styles.filterButton}>
              <Ionicons name="options" size={20} color={Colors.white} />
            </TouchableOpacity>
          </TouchableOpacity>
        </Animated.View>

        {/* Service Tabs */}
        <Animated.View entering={FadeIn.delay(180).duration(300)}>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.serviceTabs}>
            {SERVICE_TABS.map((tab) => (
              <TouchableOpacity
                key={tab.key}
                testID={`service-tab-${tab.key}`}
                style={[styles.serviceTab, activeService === tab.key && styles.serviceTabActive]}
                onPress={() => setActiveService(tab.key)}
              >
                <Text style={styles.serviceEmoji}>{tab.emoji}</Text>
                <Text style={[styles.serviceLabel, activeService === tab.key && styles.serviceLabelActive]}>
                  {tab.label}
                </Text>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </Animated.View>

        {/* Promo Banner - slide in from left */}
        <Animated.View entering={SlideInLeft.delay(200).duration(500).springify()}>
          <View style={styles.promoBanner}>
            <View style={styles.promoContent}>
              <Text style={styles.promoLabel}>LIMITED OFFER</Text>
              <Text style={styles.promoTitle}>40% OFF</Text>
              <Text style={styles.promoSubtitle}>On your first order</Text>
              <View style={styles.promoCode}>
                <Text style={styles.promoCodeText}>NOLIMIT40</Text>
              </View>
            </View>
            <View style={styles.promoEmojis}>
              <Text style={styles.promoEmoji1}>🍟</Text>
              <Text style={styles.promoEmoji2}>🍔</Text>
            </View>
          </View>
        </Animated.View>

        {/* AI Features - stagger */}
        <FadeInView delay={300} style={styles.aiSection}>
          <TouchableOpacity testID="ai-randomizer-btn" style={styles.aiCard} onPress={() => router.push('/search?tab=randomizer')}>
            <Ionicons name="dice" size={22} color={Colors.sage} />
            <Text style={styles.aiCardText}>What should I eat?</Text>
          </TouchableOpacity>
          <TouchableOpacity testID="ai-mood-btn" style={styles.aiCard} onPress={() => router.push('/search?tab=mood')}>
            <Ionicons name="happy" size={22} color={Colors.sage} />
            <Text style={styles.aiCardText}>Mood-based</Text>
          </TouchableOpacity>
        </FadeInView>

        {/* Categories - stagger each item */}
        <Animated.View entering={FadeIn.delay(350).duration(300)} style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Categories</Text>
            <TouchableOpacity onPress={() => router.push('/(tabs)/search')}>
              <Text style={styles.seeAll}>See all</Text>
            </TouchableOpacity>
          </View>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.categoriesScroll}>
            {CATEGORIES.map((category, index) => (
              <StaggerItem key={index} index={index} delay={60}>
                <TouchableOpacity
                  testID={`category-${category.name.toLowerCase()}`}
                  style={styles.categoryCard}
                  onPress={() => router.push(`/search?cuisine=${category.cuisine}` as any)}
                >
                  <View style={styles.categoryIcon}>
                    <Text style={styles.categoryEmoji}>{category.emoji}</Text>
                  </View>
                  <Text style={styles.categoryName}>{category.name}</Text>
                </TouchableOpacity>
              </StaggerItem>
            ))}
          </ScrollView>
        </Animated.View>

        {/* Featured Restaurants - stagger cards */}
        <View style={styles.section}>
          <Animated.View entering={FadeIn.delay(400).duration(300)} style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>
              {activeService === 'all' ? 'Featured' : SERVICE_TABS.find(t => t.key === activeService)?.label}
            </Text>
            <TouchableOpacity onPress={() => router.push('/(tabs)/search')}>
              <Text style={styles.seeAll}>See all</Text>
            </TouchableOpacity>
          </Animated.View>
          {featuredRestaurants
            .filter(r => activeService === 'all' || r.service_type === activeService)
            .map((restaurant, index) => (
            <StaggerItem key={restaurant.restaurant_id} index={index} delay={120}>
              <TouchableOpacity
                testID={`restaurant-${restaurant.restaurant_id}`}
                style={styles.featuredCard}
                onPress={() => router.push(`/restaurant/${restaurant.restaurant_id}` as any)}
                activeOpacity={0.9}
              >
                <View style={styles.featuredImageContainer}>
                  <Image source={{ uri: restaurant.image }} style={styles.featuredImage} resizeMode="cover" />
                  {restaurant.featured && (
                    <View style={styles.promoBadge}><Text style={styles.promoBadgeText}>PROMO</Text></View>
                  )}
                </View>
                <View style={styles.featuredInfo}>
                  <View style={styles.featuredNameRow}>
                    <Text style={styles.restaurantName}>{restaurant.name}</Text>
                    <View style={styles.ratingBadge}>
                      <Ionicons name="star" size={14} color={Colors.sage} />
                      <Text style={styles.ratingText}>{restaurant.rating}</Text>
                    </View>
                  </View>
                  <Text style={styles.cuisine}>{restaurant.cuisine_type}</Text>
                  <View style={styles.metaRow}>
                    <Ionicons name="time-outline" size={14} color={Colors.gray} />
                    <Text style={styles.metaText}>{restaurant.delivery_time}</Text>
                    <Ionicons name="bicycle-outline" size={14} color={Colors.gray} style={{ marginLeft: Spacing.md }} />
                    <Text style={styles.metaText}>R25</Text>
                  </View>
                </View>
              </TouchableOpacity>
            </StaggerItem>
          ))}
        </View>

        {/* All Restaurants - stagger */}
        <View style={styles.section}>
          <Animated.View entering={FadeIn.delay(600).duration(300)}>
            <Text style={styles.sectionTitle}>All Providers</Text>
          </Animated.View>
          {allRestaurants
            .filter(r => activeService === 'all' || r.service_type === activeService)
            .map((restaurant, index) => (
            <StaggerItem key={restaurant.restaurant_id} index={index} delay={80}>
              <TouchableOpacity
                style={styles.listCard}
                onPress={() => router.push(`/restaurant/${restaurant.restaurant_id}` as any)}
                activeOpacity={0.9}
              >
                <Image source={{ uri: restaurant.image }} style={styles.listImage} resizeMode="cover" />
                <View style={styles.listInfo}>
                  <Text style={styles.listName}>{restaurant.name}</Text>
                  <Text style={styles.listCuisine} numberOfLines={1}>{restaurant.cuisine_type}</Text>
                  <View style={styles.metaRow}>
                    <Ionicons name="star" size={12} color={Colors.sage} />
                    <Text style={styles.metaTextSmall}>{restaurant.rating}</Text>
                    <Text style={styles.metaDot}>•</Text>
                    <Text style={styles.metaTextSmall}>{restaurant.delivery_time}</Text>
                    <Text style={styles.metaDot}>•</Text>
                    <Text style={styles.metaTextSmall}>{restaurant.price_range}</Text>
                  </View>
                </View>
              </TouchableOpacity>
            </StaggerItem>
          ))}
        </View>

        <View style={{ height: Spacing.xxl }} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  loadingContainer: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: Colors.background },
  header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingHorizontal: Spacing.xl, paddingTop: Spacing.md },
  headerLeft: {},
  greeting: { ...Typography.bodySmall, color: Colors.textSecondary },
  userName: { fontSize: 24, fontWeight: '700', color: Colors.textPrimary, marginTop: 2 },
  cartButton: { position: 'relative', width: 48, height: 48, borderRadius: 24, backgroundColor: Colors.white, justifyContent: 'center', alignItems: 'center' },
  cartBadge: { position: 'absolute', top: 4, right: 4, backgroundColor: Colors.sage, borderRadius: 10, minWidth: 18, height: 18, justifyContent: 'center', alignItems: 'center', paddingHorizontal: 4 },
  cartBadgeText: { color: Colors.white, fontSize: 10, fontWeight: '700' },
  locationRow: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: Spacing.xl, paddingVertical: Spacing.sm, gap: 6 },
  locationLabel: { ...Typography.caption, color: Colors.textSecondary },
  locationValue: { ...Typography.bodySmall, fontWeight: '600', color: Colors.textPrimary },
  searchBar: { flexDirection: 'row', alignItems: 'center', marginHorizontal: Spacing.xl, marginVertical: Spacing.md, paddingLeft: Spacing.md, paddingRight: Spacing.xs, paddingVertical: Spacing.xs, backgroundColor: Colors.white, borderRadius: BorderRadius.lg, height: 52 },
  searchPlaceholder: { flex: 1, ...Typography.body, color: Colors.gray, marginLeft: Spacing.sm },
  filterButton: { width: 40, height: 40, borderRadius: BorderRadius.md, backgroundColor: Colors.sage, justifyContent: 'center', alignItems: 'center' },
  serviceTabs: { paddingLeft: Spacing.xl, marginBottom: Spacing.md },
  serviceTab: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: Spacing.md, paddingVertical: Spacing.sm, borderRadius: BorderRadius.full, backgroundColor: Colors.white, marginRight: Spacing.sm, gap: 6 },
  serviceTabActive: { backgroundColor: Colors.sage },
  serviceEmoji: { fontSize: 18 },
  serviceLabel: { ...Typography.bodySmall, color: Colors.textSecondary, fontWeight: '600' },
  serviceLabelActive: { color: Colors.white },
  promoBanner: { marginHorizontal: Spacing.xl, marginBottom: Spacing.lg, backgroundColor: '#2E8B57', borderRadius: BorderRadius.xl, padding: Spacing.lg, overflow: 'hidden', minHeight: 160 },
  promoContent: { flex: 1, zIndex: 1 },
  promoLabel: { ...Typography.caption, color: 'rgba(255,255,255,0.8)', fontWeight: '600', letterSpacing: 1, marginBottom: Spacing.xs },
  promoTitle: { fontSize: 32, fontWeight: '800', color: Colors.white, marginBottom: Spacing.xs },
  promoSubtitle: { ...Typography.body, color: 'rgba(255,255,255,0.9)', marginBottom: Spacing.md },
  promoCode: { backgroundColor: 'rgba(255,255,255,0.2)', paddingHorizontal: Spacing.md, paddingVertical: Spacing.sm, borderRadius: BorderRadius.md, alignSelf: 'flex-start' },
  promoCodeText: { ...Typography.body, fontWeight: '700', color: Colors.white },
  promoEmojis: { position: 'absolute', right: Spacing.md, top: Spacing.md, bottom: Spacing.md, justifyContent: 'space-between' },
  promoEmoji1: { fontSize: 40, opacity: 0.8 },
  promoEmoji2: { fontSize: 56, opacity: 0.8 },
  aiSection: { flexDirection: 'row', paddingHorizontal: Spacing.xl, gap: Spacing.md, marginBottom: Spacing.lg },
  aiCard: { flex: 1, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', backgroundColor: Colors.sagePale, paddingVertical: 16, paddingHorizontal: Spacing.md, borderRadius: BorderRadius.xl, gap: Spacing.sm, minHeight: 52 },
  aiCardText: { ...Typography.bodySmall, color: Colors.sageDark, fontWeight: '600', lineHeight: 18 },
  section: { marginBottom: Spacing.lg },
  sectionHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingHorizontal: Spacing.xl, marginBottom: Spacing.md },
  sectionTitle: { fontSize: 20, fontWeight: '700', color: Colors.textPrimary, paddingHorizontal: Spacing.xl },
  seeAll: { ...Typography.bodySmall, color: Colors.sage, fontWeight: '600' },
  categoriesScroll: { paddingLeft: Spacing.xl },
  categoryCard: { alignItems: 'center', marginRight: Spacing.md, width: 76 },
  categoryIcon: { width: 64, height: 64, borderRadius: 20, backgroundColor: Colors.white, justifyContent: 'center', alignItems: 'center', marginBottom: Spacing.xs },
  categoryEmoji: { fontSize: 30 },
  categoryName: { ...Typography.caption, color: Colors.textSecondary, textAlign: 'center' },
  featuredCard: { marginHorizontal: Spacing.xl, marginBottom: Spacing.md, backgroundColor: Colors.white, borderRadius: BorderRadius.xl, overflow: 'hidden', borderWidth: 1, borderColor: Colors.border },
  featuredImageContainer: { position: 'relative' },
  featuredImage: { width: '100%', height: 180, backgroundColor: Colors.white },
  promoBadge: { position: 'absolute', top: Spacing.md, left: Spacing.md, backgroundColor: Colors.sage, paddingHorizontal: Spacing.md, paddingVertical: Spacing.xs, borderRadius: BorderRadius.md },
  promoBadgeText: { ...Typography.caption, color: Colors.white, fontWeight: '700' },
  featuredInfo: { padding: Spacing.md },
  featuredNameRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: Spacing.xs },
  restaurantName: { fontSize: 18, fontWeight: '700', color: Colors.textPrimary, flex: 1 },
  ratingBadge: { flexDirection: 'row', alignItems: 'center', backgroundColor: Colors.surfaceAlt, paddingHorizontal: Spacing.sm, paddingVertical: 4, borderRadius: BorderRadius.md, gap: 4 },
  ratingText: { ...Typography.bodySmall, fontWeight: '700', color: Colors.sage },
  cuisine: { ...Typography.bodySmall, color: Colors.textSecondary, marginBottom: Spacing.sm },
  metaRow: { flexDirection: 'row', alignItems: 'center' },
  metaText: { ...Typography.caption, color: Colors.textSecondary, marginLeft: 4 },
  listCard: { flexDirection: 'row', marginHorizontal: Spacing.xl, marginBottom: Spacing.md, backgroundColor: Colors.white, borderRadius: BorderRadius.xl, overflow: 'hidden', borderWidth: 1, borderColor: Colors.border, alignItems: 'stretch' },
  listImage: { width: 110, height: 110, backgroundColor: Colors.surfaceAlt },
  listInfo: { flex: 1, padding: Spacing.md, justifyContent: 'center' },
  listName: { fontSize: 15, fontWeight: '600', color: Colors.textPrimary, marginBottom: 4 },
  listCuisine: { ...Typography.caption, color: Colors.textSecondary, marginBottom: Spacing.sm },
  metaTextSmall: { ...Typography.caption, color: Colors.textSecondary, marginLeft: 4 },
  metaDot: { ...Typography.caption, color: Colors.lightGray, marginHorizontal: 4 },
});
