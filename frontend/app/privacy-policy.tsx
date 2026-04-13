import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Typography, Spacing, BorderRadius } from '../constants/Colors';

export default function PrivacyPolicyScreen() {
  const router = useRouter();

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backBtn}>
          <Ionicons name="arrow-back" size={24} color={Colors.textPrimary} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Privacy Policy</Text>
        <View style={{ width: 40 }} />
      </View>

      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        <Text style={styles.lastUpdated}>Last updated: April 2026</Text>

        <Text style={styles.sectionTitle}>1. Introduction</Text>
        <Text style={styles.body}>
          No Limit Delivery ("we", "our", "us") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, and safeguard your personal information when you use our mobile application and delivery services in Emalahleni, Mpumalanga, South Africa.
        </Text>

        <Text style={styles.sectionTitle}>2. Information We Collect</Text>
        <Text style={styles.body}>
          We collect the following information to provide our delivery services:{'\n\n'}
          - <Text style={styles.bold}>Account Information:</Text> Name, email address, phone number, and password when you register.{'\n'}
          - <Text style={styles.bold}>Delivery Addresses:</Text> Pickup and delivery addresses you provide for orders.{'\n'}
          - <Text style={styles.bold}>Order Information:</Text> Items ordered, payment method selected, order notes, and allergy information you provide.{'\n'}
          - <Text style={styles.bold}>Payment Information:</Text> Payment processing is handled securely by PayFast. We do not store your card details.{'\n'}
          - <Text style={styles.bold}>Location Data:</Text> With your permission, we use your location to show nearby providers and enable delivery tracking.
        </Text>

        <Text style={styles.sectionTitle}>3. How We Use Your Information</Text>
        <Text style={styles.body}>
          We use your information to:{'\n\n'}
          - Process and deliver your orders{'\n'}
          - Communicate order updates and delivery status{'\n'}
          - Improve our app and services{'\n'}
          - Send promotional offers (with your consent){'\n'}
          - Comply with legal obligations
        </Text>

        <Text style={styles.sectionTitle}>4. Payment Security</Text>
        <Text style={styles.body}>
          All online payments are processed securely through PayFast, a PCI-DSS compliant payment gateway registered in South Africa. We never store or have access to your full card details. Cash on delivery and EFT payment options are also available.
        </Text>

        <Text style={styles.sectionTitle}>5. Data Sharing</Text>
        <Text style={styles.body}>
          We share your information only with:{'\n\n'}
          - <Text style={styles.bold}>Delivery Partners:</Text> Your name, address, and order details to complete deliveries.{'\n'}
          - <Text style={styles.bold}>Restaurant/Service Partners:</Text> Order details and allergy information to prepare your order.{'\n'}
          - <Text style={styles.bold}>Payment Processors:</Text> PayFast for secure payment processing.{'\n\n'}
          We do not sell your personal information to third parties.
        </Text>

        <Text style={styles.sectionTitle}>6. Data Protection (POPIA)</Text>
        <Text style={styles.body}>
          We comply with the Protection of Personal Information Act (POPIA) of South Africa. You have the right to:{'\n\n'}
          - Access your personal information{'\n'}
          - Correct inaccurate information{'\n'}
          - Request deletion of your data{'\n'}
          - Object to processing of your data{'\n'}
          - Lodge a complaint with the Information Regulator
        </Text>

        <Text style={styles.sectionTitle}>7. Data Retention</Text>
        <Text style={styles.body}>
          We retain your personal information for as long as your account is active or as needed to provide services. Order history is retained for 12 months for record-keeping purposes.
        </Text>

        <Text style={styles.sectionTitle}>8. Children's Privacy</Text>
        <Text style={styles.body}>
          Our services are not directed to children under 18. We do not knowingly collect personal information from children.
        </Text>

        <Text style={styles.sectionTitle}>9. Changes to This Policy</Text>
        <Text style={styles.body}>
          We may update this Privacy Policy from time to time. We will notify you of any changes by posting the new policy on this page.
        </Text>

        <Text style={styles.sectionTitle}>10. Contact Us</Text>
        <Text style={styles.body}>
          If you have any questions about this Privacy Policy or your personal data, please contact us at:{'\n\n'}
          Email: trishsingh21@gmail.com{'\n'}
          Location: Emalahleni, Mpumalanga, South Africa
        </Text>

        <View style={{ height: 60 }} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: Spacing.xl, paddingVertical: Spacing.md, borderBottomWidth: 1, borderBottomColor: Colors.border },
  backBtn: { padding: Spacing.sm },
  headerTitle: { ...Typography.h4, color: Colors.textPrimary },
  content: { flex: 1, paddingHorizontal: Spacing.xl },
  lastUpdated: { ...Typography.caption, color: Colors.textSecondary, marginTop: Spacing.lg, marginBottom: Spacing.lg },
  sectionTitle: { ...Typography.h4, fontSize: 17, color: Colors.textPrimary, marginTop: Spacing.lg, marginBottom: Spacing.sm },
  body: { ...Typography.body, color: Colors.textSecondary, lineHeight: 22 },
  bold: { fontWeight: '600', color: Colors.textPrimary },
});
