import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Linking } from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Typography, Spacing, BorderRadius } from '../constants/Colors';

const FAQ_ITEMS = [
  { q: 'How do I track my order?', a: 'After placing an order, go to the Orders tab and tap on your active order. You\'ll see real-time tracking with estimated delivery time.' },
  { q: 'How do I earn loyalty points?', a: 'You earn 1 point for every R1 spent. Additional points from reviews (10 pts), referrals (50 pts), and birthday bonuses (100 pts).' },
  { q: 'Can I cancel my order?', a: 'You can cancel within 2 minutes of placing. After the restaurant starts preparing, cancellation may not be possible.' },
  { q: 'How do delivery fees work?', a: 'Standard delivery fee is R25 depending on distance. Free delivery is available as a loyalty reward.' },
  { q: 'Is my payment information secure?', a: 'Yes! We use Stripe for all payments. Your card details are never stored on our servers.' },
  { q: 'How do promo codes work?', a: 'Enter your promo code at checkout. Discounts are applied to your subtotal before tax and delivery fees.' },
];

export default function HelpScreen() {
  const router = useRouter();
  const [expandedFaq, setExpandedFaq] = useState<number | null>(null);

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backBtn}>
          <Ionicons name="arrow-back" size={24} color={Colors.black} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Help & Support</Text>
        <View style={{ width: 40 }} />
      </View>

      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Contact Options */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Contact Us</Text>
          <View style={styles.contactGrid}>
            <TouchableOpacity style={styles.contactCard} onPress={() => Linking.openURL('mailto:support@nolimitdelivery.com')}>
              <View style={[styles.contactIcon, { backgroundColor: '#E8F5E9' }]}>
                <Ionicons name="mail" size={24} color={Colors.sage} />
              </View>
              <Text style={styles.contactTitle}>Email</Text>
              <Text style={styles.contactDesc}>Get a response within 24h</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.contactCard} onPress={() => Linking.openURL('tel:+18001234567')}>
              <View style={[styles.contactIcon, { backgroundColor: '#E3F2FD' }]}>
                <Ionicons name="call" size={24} color="#1976D2" />
              </View>
              <Text style={styles.contactTitle}>Phone</Text>
              <Text style={styles.contactDesc}>Mon-Sun, 9am-10pm</Text>
            </TouchableOpacity>
          </View>
          <TouchableOpacity style={styles.chatButton}>
            <Ionicons name="chatbubbles" size={22} color={Colors.white} />
            <Text style={styles.chatButtonText}>Live Chat</Text>
          </TouchableOpacity>
        </View>

        {/* FAQ */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Frequently Asked Questions</Text>
          {FAQ_ITEMS.map((faq, index) => (
            <TouchableOpacity
              key={index}
              style={styles.faqItem}
              onPress={() => setExpandedFaq(expandedFaq === index ? null : index)}
              activeOpacity={0.7}
            >
              <View style={styles.faqHeader}>
                <Text style={styles.faqQuestion}>{faq.q}</Text>
                <Ionicons
                  name={expandedFaq === index ? 'chevron-up' : 'chevron-down'}
                  size={20}
                  color={Colors.gray}
                />
              </View>
              {expandedFaq === index && (
                <Text style={styles.faqAnswer}>{faq.a}</Text>
              )}
            </TouchableOpacity>
          ))}
        </View>

        {/* App Info */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>About</Text>
          <View style={styles.aboutCard}>
            <View style={styles.aboutRow}>
              <Text style={styles.aboutLabel}>App Version</Text>
              <Text style={styles.aboutValue}>1.0.0</Text>
            </View>
            <View style={styles.aboutRow}>
              <Text style={styles.aboutLabel}>Terms of Service</Text>
              <Ionicons name="chevron-forward" size={18} color={Colors.gray} />
            </View>
            <View style={styles.aboutRow}>
              <Text style={styles.aboutLabel}>Privacy Policy</Text>
              <Ionicons name="chevron-forward" size={18} color={Colors.gray} />
            </View>
            <View style={[styles.aboutRow, { borderBottomWidth: 0 }]}>
              <Text style={styles.aboutLabel}>Licenses</Text>
              <Ionicons name="chevron-forward" size={18} color={Colors.gray} />
            </View>
          </View>
        </View>

        <Text style={styles.footer}>Made with care by No Limit Delivery</Text>
        <View style={{ height: Spacing.xxl }} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.white },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: Spacing.xl, paddingVertical: Spacing.md, borderBottomWidth: 1, borderBottomColor: Colors.border },
  backBtn: { padding: Spacing.sm },
  headerTitle: { ...Typography.h4, color: Colors.black },
  section: { paddingHorizontal: Spacing.xl, marginTop: Spacing.lg },
  sectionTitle: { ...Typography.h4, fontSize: 18, color: Colors.black, marginBottom: Spacing.md },
  contactGrid: { flexDirection: 'row', gap: Spacing.md, marginBottom: Spacing.md },
  contactCard: { flex: 1, backgroundColor: Colors.paleGray, borderRadius: BorderRadius.xl, padding: Spacing.md, alignItems: 'center' },
  contactIcon: { width: 48, height: 48, borderRadius: 24, justifyContent: 'center', alignItems: 'center', marginBottom: Spacing.sm },
  contactTitle: { ...Typography.body, fontWeight: '600', color: Colors.black },
  contactDesc: { ...Typography.caption, color: Colors.textSecondary, marginTop: 2 },
  chatButton: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', backgroundColor: Colors.sage, paddingVertical: Spacing.md, borderRadius: BorderRadius.lg, gap: Spacing.sm },
  chatButtonText: { ...Typography.button, color: Colors.white },
  faqItem: { borderBottomWidth: 1, borderBottomColor: Colors.borderLight, paddingVertical: Spacing.md },
  faqHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  faqQuestion: { ...Typography.body, fontWeight: '600', color: Colors.black, flex: 1, paddingRight: Spacing.md },
  faqAnswer: { ...Typography.body, color: Colors.textSecondary, marginTop: Spacing.sm, lineHeight: 22 },
  aboutCard: { backgroundColor: Colors.paleGray, borderRadius: BorderRadius.xl, overflow: 'hidden' },
  aboutRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', padding: Spacing.md, borderBottomWidth: 1, borderBottomColor: Colors.border },
  aboutLabel: { ...Typography.body, color: Colors.black },
  aboutValue: { ...Typography.body, color: Colors.textSecondary },
  footer: { ...Typography.caption, color: Colors.lightGray, textAlign: 'center', marginTop: Spacing.xl },
});
