import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Typography, Spacing, BorderRadius } from '../constants/Colors';
import { useAuthStore } from '../store/authStore';
import { api } from '../utils/api';

const TIERS = [
  { name: 'Bronze', min: 0, max: 99, icon: 'medal-outline', color: '#CD7F32', emoji: '🥉' },
  { name: 'Silver', min: 100, max: 499, icon: 'medal-outline', color: '#C0C0C0', emoji: '🥈' },
  { name: 'Gold', min: 500, max: 999, icon: 'trophy-outline', color: '#FFD700', emoji: '🥇' },
  { name: 'Platinum', min: 1000, max: Infinity, icon: 'diamond-outline', color: '#E5E4E2', emoji: '💎' },
];

const REWARDS = [
  { id: 'r1', name: 'Free Delivery', description: 'Free delivery on your next order', points: 50, icon: 'bicycle' },
  { id: 'r2', name: '10% Off', description: '10% discount on any order', points: 100, icon: 'pricetag' },
  { id: 'r3', name: '20% Off', description: '20% discount on any order', points: 200, icon: 'pricetags' },
  { id: 'r4', name: 'Free Dessert', description: 'Free dessert with any order', points: 75, icon: 'ice-cream' },
  { id: 'r5', name: 'R50 Credit', description: 'R50 off your next order', points: 150, icon: 'cash' },
  { id: 'r6', name: 'VIP Access', description: 'Early access to new restaurants', points: 300, icon: 'star' },
];

export default function RewardsScreen() {
  const router = useRouter();
  const { session_token, user, updateUser } = useAuthStore();
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [redeemingId, setRedeemingId] = useState<string | null>(null);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    if (!session_token) return;
    try {
      const data = await api.getProfile(session_token);
      setProfile(data);
    } catch (error) {
      console.error('Error loading profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const points = profile?.loyalty_points || 0;

  const getCurrentTier = () => {
    for (let i = TIERS.length - 1; i >= 0; i--) {
      if (points >= TIERS[i].min) return TIERS[i];
    }
    return TIERS[0];
  };

  const getNextTier = () => {
    const currentIndex = TIERS.findIndex(t => t.name === getCurrentTier().name);
    return currentIndex < TIERS.length - 1 ? TIERS[currentIndex + 1] : null;
  };

  const currentTier = getCurrentTier();
  const nextTier = getNextTier();

  const progressToNext = nextTier
    ? ((points - currentTier.min) / (nextTier.min - currentTier.min)) * 100
    : 100;

  const handleRedeem = (reward: typeof REWARDS[0]) => {
    if (points < reward.points) {
      Alert.alert('Not Enough Points', `You need ${reward.points - points} more points to redeem this reward.`);
      return;
    }
    Alert.alert(
      'Redeem Reward',
      `Redeem ${reward.name} for ${reward.points} points?`,
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Redeem',
          onPress: () => {
            setRedeemingId(reward.id);
            setTimeout(() => {
              Alert.alert('Reward Redeemed!', `${reward.name} has been added to your account. Use it on your next order!`);
              setRedeemingId(null);
            }, 1000);
          },
        },
      ]
    );
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
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity testID="rewards-back-btn" onPress={() => router.back()} style={styles.backBtn}>
          <Ionicons name="arrow-back" size={24} color={Colors.black} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Loyalty Rewards</Text>
        <View style={{ width: 40 }} />
      </View>

      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Points & Tier Card */}
        <View style={styles.tierCard}>
          <View style={styles.tierTop}>
            <Text style={styles.tierEmoji}>{currentTier.emoji}</Text>
            <View style={styles.tierInfo}>
              <Text style={styles.tierName}>{currentTier.name} Member</Text>
              <Text style={styles.pointsValue}>{points.toLocaleString()} pts</Text>
            </View>
          </View>

          {nextTier && (
            <View style={styles.progressSection}>
              <View style={styles.progressBar}>
                <View style={[styles.progressFill, { width: `${Math.min(progressToNext, 100)}%` }]} />
              </View>
              <Text style={styles.progressText}>
                {nextTier.min - points} pts to {nextTier.name}
              </Text>
            </View>
          )}

          {!nextTier && (
            <Text style={styles.maxTierText}>You've reached the highest tier!</Text>
          )}
        </View>

        {/* All Tiers */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Membership Tiers</Text>
          <View style={styles.tiersGrid}>
            {TIERS.map((tier) => {
              const isActive = tier.name === currentTier.name;
              return (
                <View
                  key={tier.name}
                  style={[styles.tierBadge, isActive && styles.tierBadgeActive]}
                >
                  <Text style={styles.tierBadgeEmoji}>{tier.emoji}</Text>
                  <Text style={[styles.tierBadgeName, isActive && styles.tierBadgeNameActive]}>
                    {tier.name}
                  </Text>
                  <Text style={styles.tierBadgeRange}>
                    {tier.max === Infinity ? `${tier.min}+` : `${tier.min}-${tier.max}`}
                  </Text>
                  {isActive && (
                    <View style={styles.currentBadge}>
                      <Text style={styles.currentBadgeText}>Current</Text>
                    </View>
                  )}
                </View>
              );
            })}
          </View>
        </View>

        {/* Available Rewards */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Available Rewards</Text>
          <View style={styles.rewardsList}>
            {REWARDS.map((reward) => {
              const canRedeem = points >= reward.points;
              const isRedeeming = redeemingId === reward.id;
              return (
                <View key={reward.id} style={styles.rewardCard}>
                  <View style={[styles.rewardIcon, { backgroundColor: canRedeem ? Colors.sagePale : Colors.paleGray }]}>
                    <Ionicons
                      name={reward.icon as any}
                      size={24}
                      color={canRedeem ? Colors.sage : Colors.lightGray}
                    />
                  </View>
                  <View style={styles.rewardInfo}>
                    <Text style={styles.rewardName}>{reward.name}</Text>
                    <Text style={styles.rewardDescription}>{reward.description}</Text>
                    <Text style={[styles.rewardPoints, { color: canRedeem ? Colors.sage : Colors.textSecondary }]}>
                      {reward.points} points
                    </Text>
                  </View>
                  <TouchableOpacity
                    testID={`redeem-${reward.id}`}
                    style={[styles.redeemBtn, !canRedeem && styles.redeemBtnDisabled]}
                    onPress={() => handleRedeem(reward)}
                    disabled={isRedeeming}
                  >
                    {isRedeeming ? (
                      <ActivityIndicator size="small" color={Colors.white} />
                    ) : (
                      <Text style={[styles.redeemBtnText, !canRedeem && styles.redeemBtnTextDisabled]}>
                        Redeem
                      </Text>
                    )}
                  </TouchableOpacity>
                </View>
              );
            })}
          </View>
        </View>

        {/* How to Earn */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>How to Earn Points</Text>
          <View style={styles.earnList}>
            {[
              { icon: 'cart', text: 'Earn 1 point for every R1 spent', highlight: '1 pt / R1' },
              { icon: 'star', text: 'Leave a review and earn 10 points', highlight: '+10 pts' },
              { icon: 'people', text: 'Refer a friend and earn 50 points', highlight: '+50 pts' },
              { icon: 'gift', text: 'Birthday bonus - 100 points', highlight: '+100 pts' },
            ].map((item, index) => (
              <View key={index} style={styles.earnItem}>
                <View style={styles.earnIcon}>
                  <Ionicons name={item.icon as any} size={20} color={Colors.sage} />
                </View>
                <Text style={styles.earnText}>{item.text}</Text>
                <View style={styles.earnHighlight}>
                  <Text style={styles.earnHighlightText}>{item.highlight}</Text>
                </View>
              </View>
            ))}
          </View>
        </View>

        <View style={{ height: Spacing.xxl * 2 }} />
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
  tierCard: {
    margin: Spacing.xl,
    padding: Spacing.lg,
    backgroundColor: Colors.sagePale,
    borderRadius: BorderRadius.xl,
  },
  tierTop: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: Spacing.md,
  },
  tierEmoji: {
    fontSize: 48,
    marginRight: Spacing.md,
  },
  tierInfo: {
    flex: 1,
  },
  tierName: {
    ...Typography.h4,
    color: Colors.sageDark,
  },
  pointsValue: {
    fontSize: 28,
    fontWeight: '700',
    color: Colors.sage,
    marginTop: 2,
  },
  progressSection: {
    marginTop: Spacing.sm,
  },
  progressBar: {
    height: 8,
    backgroundColor: 'rgba(255,255,255,0.5)',
    borderRadius: 4,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: Colors.sage,
    borderRadius: 4,
  },
  progressText: {
    ...Typography.caption,
    color: Colors.sageDark,
    marginTop: Spacing.xs,
    textAlign: 'right',
  },
  maxTierText: {
    ...Typography.bodySmall,
    color: Colors.sageDark,
    fontWeight: '600',
    marginTop: Spacing.sm,
  },
  section: {
    paddingHorizontal: Spacing.xl,
    marginBottom: Spacing.lg,
  },
  sectionTitle: {
    ...Typography.h4,
    fontSize: 18,
    color: Colors.black,
    marginBottom: Spacing.md,
  },
  tiersGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: Spacing.sm,
  },
  tierBadge: {
    width: '48%',
    backgroundColor: Colors.paleGray,
    borderRadius: BorderRadius.lg,
    padding: Spacing.md,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: 'transparent',
  },
  tierBadgeActive: {
    borderColor: Colors.sage,
    backgroundColor: Colors.sagePale,
  },
  tierBadgeEmoji: {
    fontSize: 32,
    marginBottom: Spacing.xs,
  },
  tierBadgeName: {
    ...Typography.body,
    fontWeight: '600',
    color: Colors.textSecondary,
  },
  tierBadgeNameActive: {
    color: Colors.sage,
  },
  tierBadgeRange: {
    ...Typography.caption,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  currentBadge: {
    backgroundColor: Colors.sage,
    paddingHorizontal: Spacing.sm,
    paddingVertical: 2,
    borderRadius: BorderRadius.full,
    marginTop: Spacing.xs,
  },
  currentBadgeText: {
    ...Typography.caption,
    color: Colors.white,
    fontWeight: '600',
  },
  rewardsList: {
    gap: Spacing.md,
  },
  rewardCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.white,
    borderRadius: BorderRadius.lg,
    padding: Spacing.md,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  rewardIcon: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: Spacing.md,
  },
  rewardInfo: {
    flex: 1,
  },
  rewardName: {
    ...Typography.body,
    fontWeight: '600',
    color: Colors.black,
  },
  rewardDescription: {
    ...Typography.caption,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  rewardPoints: {
    ...Typography.caption,
    fontWeight: '600',
    marginTop: 4,
  },
  redeemBtn: {
    backgroundColor: Colors.sage,
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm,
    borderRadius: BorderRadius.lg,
    minWidth: 80,
    alignItems: 'center',
  },
  redeemBtnDisabled: {
    backgroundColor: Colors.paleGray,
  },
  redeemBtnText: {
    ...Typography.bodySmall,
    fontWeight: '600',
    color: Colors.white,
  },
  redeemBtnTextDisabled: {
    color: Colors.textSecondary,
  },
  earnList: {
    gap: Spacing.md,
  },
  earnItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: Spacing.md,
    backgroundColor: Colors.paleGray,
    borderRadius: BorderRadius.lg,
  },
  earnIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: Colors.sagePale,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: Spacing.md,
  },
  earnText: {
    ...Typography.bodySmall,
    color: Colors.textSecondary,
    flex: 1,
  },
  earnHighlight: {
    backgroundColor: Colors.sagePale,
    paddingHorizontal: Spacing.sm,
    paddingVertical: 4,
    borderRadius: BorderRadius.sm,
  },
  earnHighlightText: {
    ...Typography.caption,
    fontWeight: '600',
    color: Colors.sage,
  },
});
