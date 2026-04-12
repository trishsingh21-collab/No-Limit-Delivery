import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, TextInput, Alert, KeyboardAvoidingView, Platform } from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Typography, Spacing, BorderRadius } from '../constants/Colors';
import { useAuthStore } from '../store/authStore';

const SAMPLE_ADDRESSES = [
  { id: '1', label: 'Home', street: '123 Main St', city: 'San Francisco', zip: '94105', isDefault: true },
  { id: '2', label: 'Work', street: '456 Market St', city: 'San Francisco', zip: '94103', isDefault: false },
];

export default function AddressesScreen() {
  const router = useRouter();
  const [addresses, setAddresses] = useState(SAMPLE_ADDRESSES);
  const [showForm, setShowForm] = useState(false);
  const [newAddress, setNewAddress] = useState({ label: '', street: '', city: '', zip: '' });

  const handleAdd = () => {
    if (!newAddress.street || !newAddress.city || !newAddress.zip) {
      Alert.alert('Error', 'Please fill in all fields');
      return;
    }
    setAddresses([...addresses, { ...newAddress, id: Date.now().toString(), isDefault: false }]);
    setNewAddress({ label: '', street: '', city: '', zip: '' });
    setShowForm(false);
  };

  const handleDelete = (id: string) => {
    Alert.alert('Delete Address', 'Are you sure?', [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Delete', style: 'destructive', onPress: () => setAddresses(addresses.filter(a => a.id !== id)) },
    ]);
  };

  const handleSetDefault = (id: string) => {
    setAddresses(addresses.map(a => ({ ...a, isDefault: a.id === id })));
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backBtn}>
          <Ionicons name="arrow-back" size={24} color={Colors.black} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Delivery Addresses</Text>
        <TouchableOpacity onPress={() => setShowForm(!showForm)}>
          <Ionicons name={showForm ? "close" : "add"} size={24} color={Colors.sage} />
        </TouchableOpacity>
      </View>

      <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : 'height'} style={{ flex: 1 }}>
        <ScrollView showsVerticalScrollIndicator={false}>
          {showForm && (
            <View style={styles.formCard}>
              <Text style={styles.formTitle}>Add New Address</Text>
              <TextInput style={styles.input} placeholder="Label (Home, Work...)" placeholderTextColor={Colors.gray} value={newAddress.label} onChangeText={t => setNewAddress({...newAddress, label: t})} />
              <TextInput style={styles.input} placeholder="Street address" placeholderTextColor={Colors.gray} value={newAddress.street} onChangeText={t => setNewAddress({...newAddress, street: t})} />
              <View style={styles.row}>
                <TextInput style={[styles.input, { flex: 1 }]} placeholder="City" placeholderTextColor={Colors.gray} value={newAddress.city} onChangeText={t => setNewAddress({...newAddress, city: t})} />
                <TextInput style={[styles.input, { flex: 0.5, marginLeft: Spacing.sm }]} placeholder="ZIP" placeholderTextColor={Colors.gray} value={newAddress.zip} onChangeText={t => setNewAddress({...newAddress, zip: t})} keyboardType="number-pad" />
              </View>
              <TouchableOpacity style={styles.saveBtn} onPress={handleAdd}>
                <Text style={styles.saveBtnText}>Save Address</Text>
              </TouchableOpacity>
            </View>
          )}

          {addresses.map(addr => (
            <View key={addr.id} style={styles.addressCard}>
              <View style={styles.addressLeft}>
                <View style={styles.addressIcon}>
                  <Ionicons name={addr.label === 'Home' ? 'home' : addr.label === 'Work' ? 'briefcase' : 'location'} size={20} color={Colors.sage} />
                </View>
                <View style={styles.addressInfo}>
                  <View style={styles.labelRow}>
                    <Text style={styles.addressLabel}>{addr.label || 'Address'}</Text>
                    {addr.isDefault && <View style={styles.defaultBadge}><Text style={styles.defaultText}>Default</Text></View>}
                  </View>
                  <Text style={styles.addressText}>{addr.street}</Text>
                  <Text style={styles.addressCity}>{addr.city}, {addr.zip}</Text>
                </View>
              </View>
              <View style={styles.addressActions}>
                {!addr.isDefault && (
                  <TouchableOpacity onPress={() => handleSetDefault(addr.id)} style={styles.actionBtn}>
                    <Ionicons name="checkmark-circle-outline" size={20} color={Colors.sage} />
                  </TouchableOpacity>
                )}
                <TouchableOpacity onPress={() => handleDelete(addr.id)} style={styles.actionBtn}>
                  <Ionicons name="trash-outline" size={20} color={Colors.error} />
                </TouchableOpacity>
              </View>
            </View>
          ))}

          {addresses.length === 0 && (
            <View style={styles.empty}><Ionicons name="location-outline" size={64} color={Colors.lightGray} /><Text style={styles.emptyText}>No saved addresses</Text></View>
          )}
          <View style={{ height: Spacing.xxl }} />
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.white },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: Spacing.xl, paddingVertical: Spacing.md, borderBottomWidth: 1, borderBottomColor: Colors.border },
  backBtn: { padding: Spacing.sm },
  headerTitle: { ...Typography.h4, color: Colors.black },
  formCard: { margin: Spacing.xl, padding: Spacing.lg, backgroundColor: Colors.paleGray, borderRadius: BorderRadius.xl },
  formTitle: { ...Typography.h4, fontSize: 18, color: Colors.black, marginBottom: Spacing.md },
  input: { borderWidth: 1, borderColor: Colors.border, borderRadius: BorderRadius.lg, paddingHorizontal: Spacing.md, paddingVertical: Spacing.md, ...Typography.body, color: Colors.black, backgroundColor: Colors.white, marginBottom: Spacing.sm },
  row: { flexDirection: 'row' },
  saveBtn: { backgroundColor: Colors.sage, paddingVertical: Spacing.md, borderRadius: BorderRadius.lg, alignItems: 'center', marginTop: Spacing.sm },
  saveBtnText: { ...Typography.button, color: Colors.white },
  addressCard: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingVertical: Spacing.md, paddingHorizontal: Spacing.xl, borderBottomWidth: 1, borderBottomColor: Colors.borderLight },
  addressLeft: { flexDirection: 'row', alignItems: 'center', flex: 1 },
  addressIcon: { width: 44, height: 44, borderRadius: 22, backgroundColor: Colors.sagePale, justifyContent: 'center', alignItems: 'center', marginRight: Spacing.md },
  addressInfo: { flex: 1 },
  labelRow: { flexDirection: 'row', alignItems: 'center', gap: Spacing.sm, marginBottom: 2 },
  addressLabel: { ...Typography.body, fontWeight: '600', color: Colors.black },
  defaultBadge: { backgroundColor: Colors.sage, paddingHorizontal: 8, paddingVertical: 2, borderRadius: BorderRadius.full },
  defaultText: { ...Typography.caption, color: Colors.white, fontWeight: '600' },
  addressText: { ...Typography.bodySmall, color: Colors.textSecondary },
  addressCity: { ...Typography.caption, color: Colors.textSecondary },
  addressActions: { flexDirection: 'row', gap: Spacing.sm },
  actionBtn: { padding: Spacing.sm },
  empty: { alignItems: 'center', paddingVertical: Spacing.xxl * 2 },
  emptyText: { ...Typography.body, color: Colors.textSecondary, marginTop: Spacing.md },
});
