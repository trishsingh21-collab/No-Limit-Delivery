import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  ScrollView,
  TouchableOpacity,
  Image,
  ActivityIndicator,
} from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Typography, Spacing, BorderRadius } from '../../constants/Colors';
import { api } from '../../utils/api';
import { useAuthStore } from '../../store/authStore';

export default function SearchScreen() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const user = useAuthStore(state => state.user);
  const session_token = useAuthStore(state => state.session_token);
  const [searchQuery, setSearchQuery] = useState('');
  const [restaurants, setRestaurants] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiSuggestion, setAiSuggestion] = useState('');
  const [selectedTab, setSelectedTab] = useState<string>(params.tab as string || 'search');
  
  const cuisines = ['All', 'Italian', 'American', 'Japanese', 'Chinese', 'Healthy', 'Mexican', 'Indian', 'BBQ'];
  const [selectedCuisine, setSelectedCuisine] = useState(params.cuisine as string || 'All');
  
  const moods = [
    { name: 'Comfort', key: 'comfort', icon: 'heart' as const },
    { name: 'Healthy', key: 'healthy', icon: 'leaf' as const },
    { name: 'Quick', key: 'quick', icon: 'flash' as const },
    { name: 'Indulgent', key: 'indulgent', icon: 'ice-cream' as const },
  ];
  
  useEffect(() => {
    searchRestaurants();
  }, [selectedCuisine]);
  
  const searchRestaurants = async () => {
    setLoading(true);
    try {
      const filters: any = {};
      if (selectedCuisine !== 'All') {
        filters.cuisine = selectedCuisine;
      }
      if (searchQuery) {
        filters.search = searchQuery;
      }
      const data = await api.getRestaurants(filters);
      setRestaurants(data);
    } catch (error) {
      console.error('Error searching:', error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleRandomizer = async () => {
    setAiLoading(true);
    try {
      const data = await api.getRandomizer();
      setAiSuggestion(data.suggestion);
      setRestaurants(data.restaurants || []);
    } catch (error) {
      console.error('Error getting randomizer:', error);
    } finally {
      setAiLoading(false);
    }
  };
  
  const handleMoodSuggestion = async (mood: string) => {
    setAiLoading(true);
    try {
      const data = await api.getMoodSuggestions(mood);
      setAiSuggestion(data.suggestions);
      setRestaurants(data.restaurants || []);
    } catch (error) {
      console.error('Error getting mood suggestions:', error);
    } finally {
      setAiLoading(false);
    }
  };
  
  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Search & Discover</Text>
      </View>
      
      {/* Tabs */}
      <View style={styles.tabs}>
        <TouchableOpacity
          style={[styles.tab, selectedTab === 'search' && styles.activeTab]}
          onPress={() => setSelectedTab('search')}
        >
          <Text style={[styles.tabText, selectedTab === 'search' && styles.activeTabText]}>
            Search
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.tab, selectedTab === 'randomizer' && styles.activeTab]}
          onPress={() => {
            setSelectedTab('randomizer');
            handleRandomizer();
          }}
        >
          <Text style={[styles.tabText, selectedTab === 'randomizer' && styles.activeTabText]}>
            Randomizer
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.tab, selectedTab === 'mood' && styles.activeTab]}
          onPress={() => setSelectedTab('mood')}
        >
          <Text style={[styles.tabText, selectedTab === 'mood' && styles.activeTabText]}>
            Mood
          </Text>
        </TouchableOpacity>
      </View>
      
      <ScrollView showsVerticalScrollIndicator={false}>
        {selectedTab === 'search' && (
          <>
            {/* Search Bar */}
            <View style={styles.searchContainer}>
              <Ionicons name="search" size={20} color={Colors.gray} style={styles.searchIcon} />
              <TextInput
                style={styles.searchInput}
                placeholder="Search restaurants or cuisines..."
                placeholderTextColor={Colors.gray}
                value={searchQuery}
                onChangeText={setSearchQuery}
                onSubmitEditing={searchRestaurants}
              />
            </View>
            
            {/* Cuisine Filters */}
            <ScrollView
              horizontal
              showsHorizontalScrollIndicator={false}
              style={styles.filters}
            >
              {cuisines.map((cuisine) => (
                <TouchableOpacity
                  key={cuisine}
                  style={[
                    styles.filterChip,
                    selectedCuisine === cuisine && styles.activeFilterChip,
                  ]}
                  onPress={() => setSelectedCuisine(cuisine)}
                >
                  <Text
                    style={[
                      styles.filterText,
                      selectedCuisine === cuisine && styles.activeFilterText,
                    ]}
                  >
                    {cuisine}
                  </Text>
                </TouchableOpacity>
              ))}
            </ScrollView>
          </>
        )}
        
        {selectedTab === 'randomizer' && (
          <View style={styles.aiSection}>
            <TouchableOpacity
              style={styles.aiButton}
              onPress={handleRandomizer}
              disabled={aiLoading}
            >
              {aiLoading ? (
                <ActivityIndicator color={Colors.white} />
              ) : (
                <>
                  <Ionicons name="dice" size={24} color={Colors.white} />
                  <Text style={styles.aiButtonText}>What should I eat?</Text>
                </>
              )}
            </TouchableOpacity>
            {aiSuggestion && (
              <View style={styles.suggestionCard}>
                <Text style={styles.suggestionText}>{aiSuggestion}</Text>
              </View>
            )}
          </View>
        )}
        
        {selectedTab === 'mood' && (
          <View style={styles.moodSection}>
            <Text style={styles.moodTitle}>How are you feeling?</Text>
            <View style={styles.moodGrid}>
              {moods.map((mood) => (
                <TouchableOpacity
                  key={mood.key}
                  style={styles.moodCard}
                  onPress={() => handleMoodSuggestion(mood.key)}
                  disabled={aiLoading}
                >
                  <Ionicons name={mood.icon} size={32} color={Colors.sage} />
                  <Text style={styles.moodName}>{mood.name}</Text>
                </TouchableOpacity>
              ))}
            </View>
            {aiSuggestion && (
              <View style={styles.suggestionCard}>
                <Text style={styles.suggestionText}>{aiSuggestion}</Text>
              </View>
            )}
          </View>
        )}
        
        {/* Results */}
        {loading ? (
          <ActivityIndicator size="large" color={Colors.sage} style={styles.loader} />
        ) : (
          <View style={styles.results}>
            {restaurants.length === 0 ? (
              <View style={styles.emptyState}>
                <Ionicons name="restaurant-outline" size={64} color={Colors.lightGray} />
                <Text style={styles.emptyText}>No restaurants found</Text>
              </View>
            ) : (
              restaurants.map((restaurant) => (
                <TouchableOpacity
                  key={restaurant.restaurant_id}
                  style={styles.restaurantCard}
                  onPress={() => router.push(`/restaurant/${restaurant.restaurant_id}`)}
                >
                  <Image
                    source={{ uri: restaurant.image }}
                    style={styles.restaurantImage}
                    resizeMode="cover"
                  />
                  <View style={styles.restaurantInfo}>
                    <Text style={styles.restaurantName}>{restaurant.name}</Text>
                    <Text style={styles.description} numberOfLines={2}>
                      {restaurant.description}
                    </Text>
                    <View style={styles.meta}>
                      <Ionicons name="star" size={14} color={Colors.sage} />
                      <Text style={styles.rating}>{restaurant.rating}</Text>
                      <Text style={styles.metaDivider}>•</Text>
                      <Text style={styles.deliveryTime}>{restaurant.delivery_time}</Text>
                      <Text style={styles.metaDivider}>•</Text>
                      <Text style={styles.priceRange}>{restaurant.price_range}</Text>
                    </View>
                  </View>
                </TouchableOpacity>
              ))
            )}
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.white,
  },
  header: {
    paddingHorizontal: Spacing.xl,
    paddingTop: Spacing.md,
    paddingBottom: Spacing.md,
  },
  headerTitle: {
    ...Typography.h3,
    color: Colors.black,
  },
  tabs: {
    flexDirection: 'row',
    paddingHorizontal: Spacing.xl,
    marginBottom: Spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  tab: {
    paddingVertical: Spacing.md,
    paddingHorizontal: Spacing.md,
    marginRight: Spacing.sm,
  },
  activeTab: {
    borderBottomWidth: 2,
    borderBottomColor: Colors.sage,
  },
  tabText: {
    ...Typography.body,
    color: Colors.textSecondary,
  },
  activeTabText: {
    color: Colors.sage,
    fontWeight: '600',
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginHorizontal: Spacing.xl,
    marginBottom: Spacing.md,
    paddingHorizontal: Spacing.md,
    backgroundColor: Colors.paleGray,
    borderRadius: BorderRadius.lg,
  },
  searchIcon: {
    marginRight: Spacing.sm,
  },
  searchInput: {
    flex: 1,
    ...Typography.body,
    paddingVertical: Spacing.md,
    color: Colors.black,
  },
  filters: {
    paddingLeft: Spacing.xl,
    marginBottom: Spacing.lg,
  },
  filterChip: {
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm,
    borderRadius: BorderRadius.full,
    backgroundColor: Colors.paleGray,
    marginRight: Spacing.sm,
  },
  activeFilterChip: {
    backgroundColor: Colors.sage,
  },
  filterText: {
    ...Typography.bodySmall,
    color: Colors.textSecondary,
  },
  activeFilterText: {
    color: Colors.white,
  },
  aiSection: {
    paddingHorizontal: Spacing.xl,
    marginBottom: Spacing.lg,
  },
  aiButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: Colors.sage,
    paddingVertical: Spacing.md,
    borderRadius: BorderRadius.lg,
    gap: Spacing.sm,
  },
  aiButtonText: {
    ...Typography.button,
    color: Colors.white,
  },
  suggestionCard: {
    backgroundColor: Colors.sagePale,
    padding: Spacing.md,
    borderRadius: BorderRadius.lg,
    marginTop: Spacing.md,
  },
  suggestionText: {
    ...Typography.body,
    color: Colors.sageDark,
    lineHeight: 22,
  },
  moodSection: {
    paddingHorizontal: Spacing.xl,
    marginBottom: Spacing.lg,
  },
  moodTitle: {
    ...Typography.h4,
    color: Colors.black,
    marginBottom: Spacing.md,
  },
  moodGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: Spacing.md,
  },
  moodCard: {
    width: '47%',
    alignItems: 'center',
    backgroundColor: Colors.paleGray,
    padding: Spacing.lg,
    borderRadius: BorderRadius.lg,
  },
  moodName: {
    ...Typography.body,
    color: Colors.textPrimary,
    marginTop: Spacing.sm,
  },
  loader: {
    marginTop: Spacing.xxl,
  },
  results: {
    paddingHorizontal: Spacing.xl,
    paddingBottom: Spacing.xxl,
  },
  emptyState: {
    alignItems: 'center',
    paddingVertical: Spacing.xxl,
  },
  emptyText: {
    ...Typography.body,
    color: Colors.textSecondary,
    marginTop: Spacing.md,
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
  restaurantName: {
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
  meta: {
    flexDirection: 'row',
    alignItems: 'center',
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
});
