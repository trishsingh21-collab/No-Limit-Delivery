import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Typography, Spacing, BorderRadius } from '../constants/Colors';

const SAMPLE_CARDS = [
  { id: '1', type: 'visa', last4: '4242', expiry: '12/28', isDefault: true },
  { id: '2', type: 'mastercard', last4: '8888', expiry: '06/27', isDefault: false },
];

export default function PaymentMethodsScreen() {
  const router = useRouter();
  const [cards, setCards] = useState(SAMPLE_CARDS);

  const getCardIcon = (type: string) => type === 'visa' ? 'card' : 'card-outline';

  const handleDelete = (id: string) => {
    Alert.alert('Remove Card', 'Are you sure you want to remove this card?', [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Remove', style: 'destructive', onPress: () => setCards(cards.filter(c => c.id !== id)) },
    ]);
  };

  const handleSetDefault = (id: string) => {
    setCards(cards.map(c => ({ ...c, isDefault: c.id === id })));
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backBtn}>
          <Ionicons name="arrow-back" size={24} color={Colors.black} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Payment Methods</Text>
        <View style={{ width: 40 }} />
      </View>

      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={styles.content}>
        {cards.map(card => (
          <View key={card.id} style={[styles.card, card.isDefault && styles.cardDefault]}>
            <View style={styles.cardTop}>
              <View style={styles.cardIconWrap}>
                <Ionicons name={getCardIcon(card.type) as any} size={28} color={card.isDefault ? Colors.sage : Colors.gray} />
              </View>
              <View style={styles.cardInfo}>
                <Text style={styles.cardType}>{card.type.charAt(0).toUpperCase() + card.type.slice(1)}</Text>
                <Text style={styles.cardNumber}>**** **** **** {card.last4}</Text>
                <Text style={styles.cardExpiry}>Expires {card.expiry}</Text>
              </View>
              {card.isDefault && (
                <View style={styles.defaultBadge}>
                  <Text style={styles.defaultText}>Default</Text>
                </View>
              )}
            </View>
            <View style={styles.cardActions}>
              {!card.isDefault && (
                <TouchableOpacity style={styles.setDefaultBtn} onPress={() => handleSetDefault(card.id)}>
                  <Text style={styles.setDefaultText}>Set as Default</Text>
                </TouchableOpacity>
              )}
              <TouchableOpacity onPress={() => handleDelete(card.id)} style={styles.deleteBtn}>
                <Ionicons name="trash-outline" size={18} color={Colors.error} />
                <Text style={styles.deleteText}>Remove</Text>
              </TouchableOpacity>
            </View>
          </View>
        ))}

        <TouchableOpacity style={styles.addCard}>
          <Ionicons name="add-circle-outline" size={24} color={Colors.sage} />
          <Text style={styles.addCardText}>Add New Card</Text>
        </TouchableOpacity>

        {cards.length === 0 && (
          <View style={styles.empty}>
            <Ionicons name="card-outline" size={64} color={Colors.lightGray} />
            <Text style={styles.emptyText}>No payment methods saved</Text>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: Spacing.xl, paddingVertical: Spacing.md, borderBottomWidth: 1, borderBottomColor: Colors.border },
  backBtn: { padding: Spacing.sm },
  headerTitle: { ...Typography.h4, color: Colors.black },
  content: { padding: Spacing.xl },
  card: { backgroundColor: Colors.paleGray, borderRadius: BorderRadius.xl, padding: Spacing.lg, marginBottom: Spacing.md, borderWidth: 1, borderColor: Colors.border },
  cardDefault: { borderColor: Colors.sage, backgroundColor: '#F8FBF8' },
  cardTop: { flexDirection: 'row', alignItems: 'center' },
  cardIconWrap: { width: 48, height: 48, borderRadius: 12, backgroundColor: Colors.background, justifyContent: 'center', alignItems: 'center', marginRight: Spacing.md },
  cardInfo: { flex: 1 },
  cardType: { ...Typography.body, fontWeight: '600', color: Colors.black },
  cardNumber: { ...Typography.bodySmall, color: Colors.textSecondary, marginTop: 2, letterSpacing: 1 },
  cardExpiry: { ...Typography.caption, color: Colors.textSecondary, marginTop: 2 },
  defaultBadge: { backgroundColor: Colors.sage, paddingHorizontal: Spacing.sm, paddingVertical: 4, borderRadius: BorderRadius.full },
  defaultText: { ...Typography.caption, color: Colors.white, fontWeight: '600' },
  cardActions: { flexDirection: 'row', justifyContent: 'space-between', marginTop: Spacing.md, paddingTop: Spacing.md, borderTopWidth: 1, borderTopColor: Colors.border },
  setDefaultBtn: { paddingVertical: Spacing.sm },
  setDefaultText: { ...Typography.bodySmall, color: Colors.sage, fontWeight: '600' },
  deleteBtn: { flexDirection: 'row', alignItems: 'center', gap: 4, paddingVertical: Spacing.sm },
  deleteText: { ...Typography.bodySmall, color: Colors.error },
  addCard: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', paddingVertical: Spacing.lg, borderWidth: 2, borderColor: Colors.border, borderStyle: 'dashed', borderRadius: BorderRadius.xl, gap: Spacing.sm, marginTop: Spacing.md },
  addCardText: { ...Typography.body, color: Colors.sage, fontWeight: '600' },
  empty: { alignItems: 'center', paddingVertical: Spacing.xxl * 2 },
  emptyText: { ...Typography.body, color: Colors.textSecondary, marginTop: Spacing.md },
});
