import React, { useState, useRef } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ActivityIndicator } from 'react-native';
import { WebView } from 'react-native-webview';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Typography, Spacing, BorderRadius } from '../constants/Colors';

interface MapPickerProps {
  onLocationSelect: (location: { lat: number; lng: number; address: string }) => void;
  initialLat?: number;
  initialLng?: number;
  label?: string;
}

// Witbank/Emalahleni center coordinates
const DEFAULT_LAT = -25.8744;
const DEFAULT_LNG = 29.2339;

export default function MapPicker({ onLocationSelect, initialLat, initialLng, label = 'Select Location' }: MapPickerProps) {
  const [loading, setLoading] = useState(true);
  const [selectedAddress, setSelectedAddress] = useState('');
  const webViewRef = useRef<WebView>(null);

  const lat = initialLat || DEFAULT_LAT;
  const lng = initialLng || DEFAULT_LNG;

  const mapHtml = `
    <!DOCTYPE html>
    <html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
      <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
      <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
      <style>
        html, body, #map { height: 100%; margin: 0; padding: 0; }
        .pin-label {
          background: rgba(135,169,107,0.95);
          color: white;
          padding: 6px 12px;
          border-radius: 8px;
          font-size: 13px;
          font-weight: 500;
          border: none;
          box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }
      </style>
    </head>
    <body>
      <div id="map"></div>
      <script>
        var map = L.map('map').setView([${lat}, ${lng}], 14);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '© OpenStreetMap',
          maxZoom: 19
        }).addTo(map);

        var marker = null;
        var greenIcon = L.divIcon({
          className: '',
          html: '<div style="width:24px;height:24px;background:#87A96B;border-radius:50%;border:3px solid white;box-shadow:0 2px 6px rgba(0,0,0,0.3);"></div>',
          iconSize: [24, 24],
          iconAnchor: [12, 12]
        });

        function reverseGeocode(lat, lng) {
          fetch('https://nominatim.openstreetmap.org/reverse?format=json&lat=' + lat + '&lon=' + lng + '&zoom=18&addressdetails=1')
            .then(function(r) { return r.json(); })
            .then(function(data) {
              var addr = data.display_name || (lat.toFixed(4) + ', ' + lng.toFixed(4));
              window.ReactNativeWebView.postMessage(JSON.stringify({
                lat: lat, lng: lng, address: addr, action: 'location_selected'
              }));
              if (marker) {
                marker.bindPopup('<div class="pin-label">' + addr.substring(0, 60) + '</div>').openPopup();
              }
            })
            .catch(function() {
              window.ReactNativeWebView.postMessage(JSON.stringify({
                lat: lat, lng: lng, address: lat.toFixed(4) + ', ' + lng.toFixed(4), action: 'location_selected'
              }));
            });
        }

        map.on('click', function(e) {
          if (marker) map.removeLayer(marker);
          marker = L.marker(e.latlng, { icon: greenIcon, draggable: true }).addTo(map);
          reverseGeocode(e.latlng.lat, e.latlng.lng);
          
          marker.on('dragend', function(ev) {
            var pos = ev.target.getLatLng();
            reverseGeocode(pos.lat, pos.lng);
          });
        });
      </script>
    </body>
    </html>
  `;

  const handleMessage = (event: any) => {
    try {
      const data = JSON.parse(event.nativeEvent.data);
      if (data.action === 'location_selected') {
        setSelectedAddress(data.address);
        onLocationSelect({ lat: data.lat, lng: data.lng, address: data.address });
      }
    } catch (e) {}
  };

  return (
    <View style={styles.container}>
      <Text style={styles.label}>{label}</Text>
      <View style={styles.mapContainer}>
        {loading && (
          <View style={styles.loader}>
            <ActivityIndicator size="small" color={Colors.sage} />
            <Text style={styles.loaderText}>Loading map...</Text>
          </View>
        )}
        <WebView
          ref={webViewRef}
          source={{ html: mapHtml }}
          style={styles.map}
          onLoadEnd={() => setLoading(false)}
          onMessage={handleMessage}
          javaScriptEnabled={true}
          domStorageEnabled={true}
          scrollEnabled={false}
        />
        <View style={styles.mapHint}>
          <Ionicons name="finger-print" size={14} color={Colors.sage} />
          <Text style={styles.hintText}>Tap map to drop pin</Text>
        </View>
      </View>
      {selectedAddress ? (
        <View style={styles.addressRow}>
          <Ionicons name="location" size={16} color={Colors.sage} />
          <Text style={styles.addressText} numberOfLines={2}>{selectedAddress}</Text>
        </View>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { marginBottom: Spacing.md },
  label: { ...Typography.bodySmall, fontWeight: '600', color: Colors.textPrimary, marginBottom: Spacing.sm },
  mapContainer: { height: 200, borderRadius: BorderRadius.xl, overflow: 'hidden', borderWidth: 1, borderColor: Colors.border, position: 'relative' },
  map: { flex: 1 },
  loader: { ...StyleSheet.absoluteFillObject, justifyContent: 'center', alignItems: 'center', backgroundColor: Colors.surfaceAlt, zIndex: 1 },
  loaderText: { ...Typography.caption, color: Colors.textSecondary, marginTop: 4 },
  mapHint: { position: 'absolute', bottom: 8, left: 8, flexDirection: 'row', alignItems: 'center', backgroundColor: 'rgba(255,255,255,0.9)', paddingHorizontal: 8, paddingVertical: 4, borderRadius: 8, gap: 4 },
  hintText: { ...Typography.caption, color: Colors.sage },
  addressRow: { flexDirection: 'row', alignItems: 'flex-start', marginTop: Spacing.sm, padding: Spacing.sm, backgroundColor: Colors.sagePale, borderRadius: BorderRadius.md, gap: Spacing.sm },
  addressText: { ...Typography.bodySmall, color: Colors.textPrimary, flex: 1 },
});
