import { useEffect, useState } from "react";
import { Text, View, ScrollView } from "react-native";

const BASE_URL = "https://vscode-eb228d18-4d59-45e7-8a8d-01322ed7fdd9.preview.emergentagent.com/proxy/8000";

export default function Home() {
  const [restaurants, setRestaurants] = useState<any[]>([]);

  useEffect(() => {
    fetch(`${BASE_URL}/api/restaurants`)
      .then(res => res.json())
      .then(data => {
        setRestaurants(data);
      })
      .catch(err => console.log(err));
  }, []);

  return (
    <ScrollView style={{ padding: 20 }}>
      {restaurants.length === 0 ? (
        <Text>Loading...</Text>
      ) : (
        restaurants.map((r, i) => (
          <View key={i} style={{ marginBottom: 20 }}>
            <Text style={{ fontSize: 18, fontWeight: "bold" }}>
              {r.name}
            </Text>
            <Text>{r.cuisine_type}</Text>
          </View>
        ))
      )}
    </ScrollView>
  );
}