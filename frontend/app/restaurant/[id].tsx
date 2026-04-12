import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Image,
  Dimensions,
  ActivityIndicator,
  Alert,
} from 'react-native';
import Animated, { FadeIn, FadeInDown, FadeInUp, SlideInRight } from 'react-native-reanimated';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Typography, Spacing, BorderRadius } from '../../constants/Colors';
import { StaggerItem, BounceInView, SlideInView } from '../../components/animated';
import { api } from '../../utils/api';
import { useCartStore } from '../../store/cartStore';

const { width } = Dimensions.get('window');
const HERO_HEIGHT = 280;

export default function RestaurantDetailScreen() {
  const router = useRouter();
  const { id } = useLocalSearchParams();
  const addItem = useCartStore(state => state.addItem);
  const itemCount = useCartStore(state => state.getItemCount());
  const getTotal = useCartStore(state => state.getTotal);

  const [restaurant, setRestaurant] = useState<any>(null);
  const [menuItems, setMenuItems] = useState<any[]>([]);
  const [reviews, setReviews] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'menu' | 'reviews'>('menu');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  // Available hours (could come from backend in the future)
  const availableHours = {
    weekdays: '10:00 AM - 10:00 PM',
    weekends: '9:00 AM - 11:00 PM',
    isOpen: true,
  };

  useEffect(() => {
    loadRestaurant();
  }, [id]);

  const loadRestaurant = async () => {
    try {
      const [restData, menuData, reviewData] = await Promise.all([
        api.getRestaurant(id as string),
        api.getMenu(id as string),
        api.getReviews(id as string),
      ]);
      setRestaurant(restData);
      setMenuItems(menuData);
      setReviews(reviewData);
      if (restData.menu_categories?.length > 0) {
        setSelectedCategory(restData.menu_categories[0]);
      }
    } catch (error) {
      console.error('Error loading restaurant:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = (item: any) => {
    addItem({
      item_id: item.item_id,
      name: item.name,
      price: item.price,
      quantity: 1,
      restaurant_id: restaurant.restaurant_id,
      restaurant_name: restaurant.name,
      image: item.image,
    });
    Alert.alert('Added to Cart', `${item.name} added to your cart`);
  };

  const filteredItems = selectedCategory
    ? menuItems.filter(item => item.category === selectedCategory)
    : menuItems;

  // Group items by category
  const groupedItems: Record<string, any[]> = {};
  filteredItems.forEach(item => {
    if (!groupedItems[item.category]) {
      groupedItems[item.category] = [];
    }
    groupedItems[item.category].push(item);
  });

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={Colors.sage} />
      </View>
    );
  }

  if (!restaurant) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.errorText}>Restaurant not found</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Hero Image */}
        <View style={styles.heroContainer}>
          <Image
            source={{ uri: restaurant.image }}
            style={styles.heroImage}
            resizeMode="cover"
          />
          <View style={styles.heroOverlay} />

          {/* Floating Buttons */}
          <View style={styles.heroButtons}>
            <TouchableOpacity
              testID="back-button"
              style={styles.heroBtn}
              onPress={() => router.back()}
            >
              <Ionicons name="arrow-back" size={22} color={Colors.charcoal} />
            </TouchableOpacity>
            <View style={styles.heroRightBtns}>
              <TouchableOpacity testID="favorite-button" style={styles.heroBtn}>
                <Ionicons name="heart-outline" size={22} color={Colors.charcoal} />
              </TouchableOpacity>
              <TouchableOpacity testID="share-button" style={styles.heroBtn}>
                <Ionicons name="share-social-outline" size={22} color={Colors.charcoal} />
              </TouchableOpacity>
            </View>
          </View>
        </View>

        {/* Restaurant Info Card (overlapping hero) */}
        <Animated.View entering={FadeInUp.delay(200).duration(500).springify()} style={styles.infoCard}>
          <Text testID="restaurant-name" style={styles.restaurantName}>{restaurant.name}</Text>
          <Text style={styles.restaurantDescription}>{restaurant.description}</Text>

          <View style={styles.metaRow}>
            <View style={styles.metaItem}>
              <Ionicons name="star" size={16} color="#F5A623" />
              <Text style={styles.metaValue}>{restaurant.rating}</Text>
              <Text style={styles.metaLabel}>(120+)</Text>
            </View>
            <View style={styles.metaItem}>
              <Ionicons name="time-outline" size={16} color={Colors.gray} />
              <Text style={styles.metaValue}>{restaurant.delivery_time}</Text>
            </View>
            <View style={styles.metaItem}>
              <Ionicons name="bicycle-outline" size={16} color={Colors.gray} />
              <Text style={styles.metaValue}>R25</Text>
            </View>
          </View>

          {/* Available Hours */}
          <View style={styles.hoursRow}>
            <View style={[styles.openBadge, { backgroundColor: availableHours.isOpen ? '#E8F5E9' : '#FFEBEE' }]}>
              <View style={[styles.openDot, { backgroundColor: availableHours.isOpen ? Colors.sage : Colors.error }]} />
              <Text style={[styles.openText, { color: availableHours.isOpen ? Colors.sage : Colors.error }]}>
                {availableHours.isOpen ? 'Open Now' : 'Closed'}
              </Text>
            </View>
            <Text style={styles.hoursText}>
              Mon-Fri: {availableHours.weekdays} | Sat-Sun: {availableHours.weekends}
            </Text>
          </View>
        </Animated.View>

        {/* Menu / Reviews Tabs */}
        <View style={styles.tabRow}>
          <TouchableOpacity
            testID="menu-tab"
            style={[styles.tab, activeTab === 'menu' && styles.activeTab]}
            onPress={() => setActiveTab('menu')}
          >
            <Text style={[styles.tabText, activeTab === 'menu' && styles.activeTabText]}>
              Menu
            </Text>
          </TouchableOpacity>
          <TouchableOpacity
            testID="reviews-tab"
            style={[styles.tab, activeTab === 'reviews' && styles.activeTab]}
            onPress={() => setActiveTab('reviews')}
          >
            <Text style={[styles.tabText, activeTab === 'reviews' && styles.activeTabText]}>
              Reviews
            </Text>
          </TouchableOpacity>
        </View>

        {activeTab === 'menu' ? (
          <View style={styles.menuSection}>
            {/* Category chips */}
            {restaurant.menu_categories?.length > 0 && (
              <ScrollView
                horizontal
                showsHorizontalScrollIndicator={false}
                style={styles.categoryScroll}
              >
                <TouchableOpacity
                  style={[styles.categoryChip, !selectedCategory && styles.activeCategoryChip]}
                  onPress={() => setSelectedCategory(null)}
                >
                  <Text style={[styles.categoryChipText, !selectedCategory && styles.activeCategoryChipText]}>
                    All
                  </Text>
                </TouchableOpacity>
                {restaurant.menu_categories.map((cat: string) => (
                  <TouchableOpacity
                    key={cat}
                    style={[styles.categoryChip, selectedCategory === cat && styles.activeCategoryChip]}
                    onPress={() => setSelectedCategory(cat)}
                  >
                    <Text style={[styles.categoryChipText, selectedCategory === cat && styles.activeCategoryChipText]}>
                      {cat}
                    </Text>
                  </TouchableOpacity>
                ))}
              </ScrollView>
            )}

            {/* Menu items grouped by category */}
            {Object.entries(groupedItems).map(([category, items]) => (
              <View key={category} style={styles.menuCategory}>
                <Text style={styles.menuCategoryTitle}>{category.toUpperCase()}</Text>
                {items.map((item, idx) => (
                  <StaggerItem key={item.item_id} index={idx} delay={60}>
                    <View style={styles.menuItem}>
                      <View style={styles.menuItemInfo}>
                        <Text testID={`menu-item-${item.item_id}`} style={styles.menuItemName}>
                          {item.name}
                        </Text>
                        <Text style={styles.menuItemDescription} numberOfLines={2}>
                          {item.description}
                        </Text>
                        <View style={styles.menuItemPriceRow}>
                          <Text style={styles.menuItemPrice}>R{item.price.toFixed(2)}</Text>
                        </View>
                      </View>
                      <View style={styles.menuItemRight}>
                        <Image
                          source={{ uri: item.image }}
                          style={styles.menuItemImage}
                          resizeMode="cover"
                        />
                        <TouchableOpacity
                          testID={`add-to-cart-${item.item_id}`}
                          style={styles.addButton}
                          onPress={() => handleAddToCart(item)}
                        >
                          <Ionicons name="add" size={20} color={Colors.white} />
                        </TouchableOpacity>
                      </View>
                    </View>
                  </StaggerItem>
                ))}
              </View>
            ))}

            {filteredItems.length === 0 && (
              <View style={styles.emptyMenu}>
                <Ionicons name="restaurant-outline" size={48} color={Colors.lightGray} />
                <Text style={styles.emptyText}>No menu items available</Text>
              </View>
            )}
          </View>
        ) : (
          <View style={styles.reviewsSection}>
            {reviews.length === 0 ? (
              <View style={styles.emptyMenu}>
                <Ionicons name="chatbubble-outline" size={48} color={Colors.lightGray} />
                <Text style={styles.emptyText}>No reviews yet</Text>
              </View>
            ) : (
              reviews.map((review) => (
                <View key={review.review_id} style={styles.reviewCard}>
                  <View style={styles.reviewHeader}>
                    <View style={styles.reviewAvatar}>
                      <Text style={styles.reviewAvatarText}>
                        {review.user_name?.[0]?.toUpperCase() || 'U'}
                      </Text>
                    </View>
                    <View style={styles.reviewMeta}>
                      <Text style={styles.reviewName}>{review.user_name}</Text>
                      <View style={styles.reviewStars}>
                        {[1, 2, 3, 4, 5].map((star) => (
                          <Ionicons
                            key={star}
                            name={star <= review.rating ? 'star' : 'star-outline'}
                            size={14}
                            color="#F5A623"
                          />
                        ))}
                      </View>
                    </View>
                  </View>
                  <Text style={styles.reviewComment}>{review.comment}</Text>
                </View>
              ))
            )}
          </View>
        )}

        {/* Spacer for floating cart button */}
        <View style={{ height: 100 }} />
      </ScrollView>

      {/* Floating Cart Button */}
      {itemCount > 0 && (
        <BounceInView delay={200}>
          <TouchableOpacity
          testID="view-cart-button"
          style={styles.floatingCart}
          onPress={() => router.push('/cart')}
        >
          <View style={styles.floatingCartContent}>
            <View style={styles.cartCountBadge}>
              <Text style={styles.cartCountText}>{itemCount}</Text>
            </View>
            <Text style={styles.floatingCartText}>View Cart</Text>
            <Text style={styles.floatingCartPrice}>R{getTotal().toFixed(2)}</Text>
          </View>
        </TouchableOpacity>
        </BounceInView>
      )}
    </View>
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
    ...Typography.body,
    color: Colors.textSecondary,
  },
  heroContainer: {
    height: HERO_HEIGHT,
    position: 'relative',
  },
  heroImage: {
    width: '100%',
    height: '100%',
    backgroundColor: Colors.white,
  },
  heroOverlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(0,0,0,0.1)',
  },
  heroButtons: {
    position: 'absolute',
    top: 50,
    left: Spacing.md,
    right: Spacing.md,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  heroBtn: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: 'rgba(255,255,255,0.9)',
    justifyContent: 'center',
    alignItems: 'center',
    marginLeft: Spacing.sm,
  },
  heroRightBtns: {
    flexDirection: 'row',
  },
  infoCard: {
    backgroundColor: Colors.background,
    marginTop: -30,
    marginHorizontal: Spacing.md,
    borderRadius: BorderRadius.xl,
    padding: Spacing.lg,
    elevation: 4,
    shadowColor: Colors.black,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
  },
  restaurantName: {
    fontSize: 24,
    fontWeight: '700',
    color: Colors.textPrimary,
    marginBottom: Spacing.sm,
  },
  restaurantDescription: {
    ...Typography.body,
    color: Colors.textSecondary,
    lineHeight: 22,
    marginBottom: Spacing.md,
  },
  metaRow: {
    flexDirection: 'row',
    alignItems: 'center',
    flexWrap: 'wrap',
    gap: Spacing.lg,
    marginBottom: Spacing.md,
  },
  metaItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  metaValue: {
    ...Typography.body,
    fontWeight: '600',
    color: Colors.textPrimary,
  },
  metaLabel: {
    ...Typography.bodySmall,
    color: Colors.textSecondary,
  },
  hoursRow: {
    flexDirection: 'row',
    alignItems: 'center',
    flexWrap: 'wrap',
    gap: Spacing.sm,
  },
  openBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: Spacing.sm,
    paddingVertical: 4,
    borderRadius: BorderRadius.full,
    gap: 6,
  },
  openDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
  },
  openText: {
    ...Typography.caption,
    fontWeight: '600',
  },
  hoursText: {
    ...Typography.caption,
    color: Colors.textSecondary,
  },
  tabRow: {
    flexDirection: 'row',
    marginTop: Spacing.lg,
    marginHorizontal: Spacing.xl,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  tab: {
    paddingVertical: Spacing.md,
    paddingHorizontal: Spacing.lg,
  },
  activeTab: {
    borderBottomWidth: 3,
    borderBottomColor: Colors.sage,
  },
  tabText: {
    ...Typography.body,
    color: Colors.textSecondary,
  },
  activeTabText: {
    color: Colors.textPrimary,
    fontWeight: '600',
  },
  menuSection: {
    paddingBottom: Spacing.xl,
  },
  categoryScroll: {
    paddingLeft: Spacing.xl,
    paddingVertical: Spacing.md,
  },
  categoryChip: {
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm,
    borderRadius: BorderRadius.full,
    backgroundColor: Colors.white,
    marginRight: Spacing.sm,
  },
  activeCategoryChip: {
    backgroundColor: Colors.sage,
  },
  categoryChipText: {
    ...Typography.bodySmall,
    color: Colors.textSecondary,
  },
  activeCategoryChipText: {
    color: Colors.white,
    fontWeight: '600',
  },
  menuCategory: {
    paddingHorizontal: Spacing.xl,
    marginTop: Spacing.md,
  },
  menuCategoryTitle: {
    fontSize: 14,
    fontWeight: '700',
    color: Colors.textPrimary,
    letterSpacing: 1,
    marginBottom: Spacing.md,
  },
  menuItem: {
    flexDirection: 'row',
    paddingVertical: Spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: Colors.borderLight,
  },
  menuItemInfo: {
    flex: 1,
    paddingRight: Spacing.md,
  },
  menuItemName: {
    ...Typography.body,
    fontWeight: '600',
    color: Colors.textPrimary,
    marginBottom: Spacing.xs,
  },
  menuItemDescription: {
    ...Typography.caption,
    color: Colors.textSecondary,
    lineHeight: 18,
    marginBottom: Spacing.sm,
  },
  menuItemPriceRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.sm,
  },
  menuItemPrice: {
    fontSize: 16,
    fontWeight: '700',
    color: Colors.textPrimary,
  },
  calorieBadge: {
    backgroundColor: Colors.white,
    paddingHorizontal: Spacing.sm,
    paddingVertical: 2,
    borderRadius: BorderRadius.sm,
  },
  calorieText: {
    ...Typography.caption,
    color: Colors.textSecondary,
  },
  menuItemRight: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  menuItemImage: {
    width: 80,
    height: 80,
    borderRadius: BorderRadius.md,
    backgroundColor: Colors.white,
    marginBottom: Spacing.xs,
  },
  addButton: {
    width: 34,
    height: 34,
    borderRadius: 17,
    backgroundColor: Colors.sage,
    justifyContent: 'center',
    alignItems: 'center',
    position: 'absolute',
    bottom: 12,
    right: 0,
    elevation: 2,
    shadowColor: Colors.black,
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.15,
    shadowRadius: 2,
  },
  emptyMenu: {
    alignItems: 'center',
    paddingVertical: Spacing.xxl,
  },
  emptyText: {
    ...Typography.body,
    color: Colors.textSecondary,
    marginTop: Spacing.md,
  },
  reviewsSection: {
    paddingHorizontal: Spacing.xl,
    paddingTop: Spacing.md,
    paddingBottom: Spacing.xl,
  },
  reviewCard: {
    padding: Spacing.md,
    backgroundColor: Colors.white,
    borderRadius: BorderRadius.lg,
    marginBottom: Spacing.md,
  },
  reviewHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: Spacing.sm,
  },
  reviewAvatar: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: Colors.sage,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: Spacing.sm,
  },
  reviewAvatarText: {
    ...Typography.body,
    fontWeight: '600',
    color: Colors.white,
  },
  reviewMeta: {
    flex: 1,
  },
  reviewName: {
    ...Typography.bodySmall,
    fontWeight: '600',
    color: Colors.textPrimary,
  },
  reviewStars: {
    flexDirection: 'row',
    marginTop: 2,
  },
  reviewComment: {
    ...Typography.body,
    color: Colors.textSecondary,
    lineHeight: 22,
  },
  floatingCart: {
    position: 'absolute',
    bottom: Spacing.xl,
    left: Spacing.xl,
    right: Spacing.xl,
    backgroundColor: Colors.sage,
    borderRadius: BorderRadius.lg,
    padding: Spacing.md,
    elevation: 6,
    shadowColor: Colors.black,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
  },
  floatingCartContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  cartCountBadge: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: 'rgba(255,255,255,0.3)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  cartCountText: {
    ...Typography.caption,
    fontWeight: '600',
    color: Colors.white,
  },
  floatingCartText: {
    ...Typography.button,
    color: Colors.white,
  },
  floatingCartPrice: {
    ...Typography.button,
    color: Colors.white,
  },
});
