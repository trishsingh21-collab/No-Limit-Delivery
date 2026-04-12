import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Switch } from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Typography, Spacing, BorderRadius } from '../constants/Colors';

export default function NotificationsScreen() {
  const router = useRouter();
  const [settings, setSettings] = useState({
    orderUpdates: true,
    promotions: true,
    newRestaurants: false,
    rewards: true,
    emailNotifs: false,
    smsNotifs: true,
  });

  const toggle = (key: keyof typeof settings) => {
    setSettings({ ...settings, [key]: !settings[key] });
  };

  const sections = [
    {
      title: 'Order Notifications',
      items: [
        { key: 'orderUpdates' as const, icon: 'receipt', title: 'Order Updates', desc: 'Get notified about order status changes' },
        { key: 'smsNotifs' as const, icon: 'chatbubble', title: 'SMS Updates', desc: 'Receive text messages for delivery' },
      ],
    },
    {
      title: 'Marketing',
      items: [
        { key: 'promotions' as const, icon: 'pricetag', title: 'Promotions & Deals', desc: 'Special offers and discounts' },
        { key: 'newRestaurants' as const, icon: 'restaurant', title: 'New Restaurants', desc: 'When new restaurants open near you' },
        { key: 'rewards' as const, icon: 'gift', title: 'Rewards Updates', desc: 'Points earned and reward availability' },
        { key: 'emailNotifs' as const, icon: 'mail', title: 'Email Newsletter', desc: 'Weekly food recommendations' },
      ],
    },
  ];

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backBtn}>
          <Ionicons name="arrow-back" size={24} color={Colors.black} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Notifications</Text>
        <View style={{ width: 40 }} />
      </View>

      <ScrollView showsVerticalScrollIndicator={false}>
        {sections.map((section, sIdx) => (
          <View key={sIdx} style={styles.section}>
            <Text style={styles.sectionTitle}>{section.title}</Text>
            <View style={styles.card}>
              {section.items.map((item, iIdx) => (
                <View key={item.key} style={[styles.row, iIdx < section.items.length - 1 && styles.rowBorder]}>
                  <View style={styles.iconWrap}>
                    <Ionicons name={item.icon as any} size={20} color={Colors.sage} />
                  </View>
                  <View style={styles.rowInfo}>
                    <Text style={styles.rowTitle}>{item.title}</Text>
                    <Text style={styles.rowDesc}>{item.desc}</Text>
                  </View>
                  <Switch
                    value={settings[item.key]}
                    onValueChange={() => toggle(item.key)}
                    trackColor={{ false: Colors.lightGray, true: Colors.sageLight }}
                    thumbColor={settings[item.key] ? Colors.sage : Colors.gray}
                  />
                </View>
              ))}
            </View>
          </View>
        ))}
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
  section: { paddingHorizontal: Spacing.xl, marginTop: Spacing.lg },
  sectionTitle: { ...Typography.bodySmall, fontWeight: '600', color: Colors.textSecondary, textTransform: 'uppercase', letterSpacing: 1, marginBottom: Spacing.sm },
  card: { backgroundColor: Colors.background, borderRadius: BorderRadius.xl, borderWidth: 1, borderColor: Colors.border, overflow: 'hidden' },
  row: { flexDirection: 'row', alignItems: 'center', padding: Spacing.md },
  rowBorder: { borderBottomWidth: 1, borderBottomColor: Colors.borderLight },
  iconWrap: { width: 40, height: 40, borderRadius: 12, backgroundColor: Colors.sagePale, justifyContent: 'center', alignItems: 'center', marginRight: Spacing.md },
  rowInfo: { flex: 1, marginRight: Spacing.md },
  rowTitle: { ...Typography.body, fontWeight: '600', color: Colors.black },
  rowDesc: { ...Typography.caption, color: Colors.textSecondary, marginTop: 2 },
});
