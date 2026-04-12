import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Typography, Spacing, BorderRadius } from '../constants/Colors';
import { useAuthStore } from '../store/authStore';
import { format } from 'date-fns';

export default function MyReviewsScreen() {
  const router = useRouter();
  const session_token = useAuthStore(state => state.session_token);
  const [reviews, setReviews] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadReviews();
  }, []);

  const loadReviews = async () => {
    // For now, show empty state since we need user-specific reviews endpoint
    setLoading(false);
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backBtn}>
          <Ionicons name="arrow-back" size={24} color={Colors.black} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>My Reviews</Text>
        <View style={{ width: 40 }} />
      </View>

      <ScrollView showsVerticalScrollIndicator={false}>
        {loading ? (
          <ActivityIndicator size="large" color={Colors.sage} style={{ marginTop: Spacing.xxl }} />
        ) : reviews.length === 0 ? (
          <View style={styles.empty}>
            <View style={styles.emptyIcon}>
              <Ionicons name="star-outline" size={48} color={Colors.lightGray} />
            </View>
            <Text style={styles.emptyTitle}>No reviews yet</Text>
            <Text style={styles.emptyDesc}>
              After ordering, you can rate and review restaurants to help others find great food!
            </Text>
            <TouchableOpacity style={styles.browseBtn} onPress={() => router.push('/(tabs)/home' as any)}>
              <Text style={styles.browseBtnText}>Browse Restaurants</Text>
            </TouchableOpacity>

            {/* How reviews work */}
            <View style={styles.infoCard}>
              <Text style={styles.infoTitle}>How Reviews Work</Text>
              {[
                { icon: 'cart', text: 'Place an order from any restaurant' },
                { icon: 'star', text: 'Rate your experience (1-5 stars)' },
                { icon: 'chatbubble', text: 'Write a review to help others' },
                { icon: 'gift', text: 'Earn 10 loyalty points per review' },
              ].map((item, i) => (
                <View key={i} style={styles.infoRow}>
                  <View style={styles.infoIcon}>
                    <Ionicons name={item.icon as any} size={18} color={Colors.sage} />
                  </View>
                  <Text style={styles.infoText}>{item.text}</Text>
                </View>
              ))}
            </View>
          </View>
        ) : (
          <View style={styles.reviewsList}>
            {reviews.map((review: any) => (
              <View key={review.review_id} style={styles.reviewCard}>
                <View style={styles.reviewHeader}>
                  <Text style={styles.restaurantName}>{review.restaurant_name}</Text>
                  <View style={styles.stars}>
                    {[1,2,3,4,5].map(s => (
                      <Ionicons key={s} name={s <= review.rating ? 'star' : 'star-outline'} size={16} color="#F5A623" />
                    ))}
                  </View>
                </View>
                <Text style={styles.reviewText}>{review.comment}</Text>
                <Text style={styles.reviewDate}>{format(new Date(review.created_at), 'MMM d, yyyy')}</Text>
              </View>
            ))}
          </View>
        )}
        <View style={{ height: Spacing.xxl }} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: Spacing.xl, paddingVertical: Spacing.md, borderBottomWidth: 1, borderBottomColor: Colors.border },
  backBtn: { padding: Spacing.sm },
  headerTitle: { ...Typography.h4, color: Colors.black },
  empty: { alignItems: 'center', paddingHorizontal: Spacing.xl, paddingTop: Spacing.xxl },
  emptyIcon: { width: 100, height: 100, borderRadius: 50, backgroundColor: Colors.paleGray, justifyContent: 'center', alignItems: 'center', marginBottom: Spacing.lg },
  emptyTitle: { ...Typography.h4, color: Colors.black, marginBottom: Spacing.sm },
  emptyDesc: { ...Typography.body, color: Colors.textSecondary, textAlign: 'center', lineHeight: 22, marginBottom: Spacing.lg },
  browseBtn: { backgroundColor: Colors.sage, paddingVertical: Spacing.md, paddingHorizontal: Spacing.xl, borderRadius: BorderRadius.lg },
  browseBtnText: { ...Typography.button, color: Colors.white },
  infoCard: { marginTop: Spacing.xl, width: '100%', backgroundColor: Colors.paleGray, borderRadius: BorderRadius.xl, padding: Spacing.lg },
  infoTitle: { ...Typography.h4, fontSize: 16, color: Colors.black, marginBottom: Spacing.md },
  infoRow: { flexDirection: 'row', alignItems: 'center', marginBottom: Spacing.md },
  infoIcon: { width: 36, height: 36, borderRadius: 18, backgroundColor: Colors.sagePale, justifyContent: 'center', alignItems: 'center', marginRight: Spacing.md },
  infoText: { ...Typography.bodySmall, color: Colors.textSecondary, flex: 1 },
  reviewsList: { paddingHorizontal: Spacing.xl, paddingTop: Spacing.md },
  reviewCard: { borderBottomWidth: 1, borderBottomColor: Colors.borderLight, paddingVertical: Spacing.md },
  reviewHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: Spacing.sm },
  restaurantName: { ...Typography.body, fontWeight: '600', color: Colors.black },
  stars: { flexDirection: 'row' },
  reviewText: { ...Typography.body, color: Colors.textSecondary, lineHeight: 22, marginBottom: Spacing.sm },
  reviewDate: { ...Typography.caption, color: Colors.lightGray },
});
