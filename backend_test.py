"""
Backend API Tests for No Limit Delivery - Seed Data Verification
Tests the specific requirements from the review request:
1. GET /api/restaurants returns exactly 13 restaurants
2. Verify specific restaurant names exist and removed ones don't
3. Verify Jazbar has menu items with specific categories
4. Check image uniqueness for menu items
5. GET /api/services returns 5 service types
"""
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

# Load frontend .env to get EXPO_PUBLIC_BACKEND_URL
frontend_env = Path(__file__).parent / 'frontend' / '.env'
load_dotenv(frontend_env)

BASE_URL = os.environ.get('EXPO_PUBLIC_BACKEND_URL', '').rstrip('/')
if not BASE_URL:
    raise ValueError("EXPO_PUBLIC_BACKEND_URL not found in environment")

print(f"\n🔗 Testing against: {BASE_URL}")

def test_auth_login():
    """Test login with test credentials"""
    print("\n=== Testing Authentication ===")
    response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": "test@demo.com",
        "password": "test123"
    })
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code} - {response.text}")
        return None
    
    data = response.json()
    print(f"✅ Login successful for test@demo.com")
    return data.get("session_token")

def test_restaurants_count():
    """Test GET /api/restaurants returns exactly 13 restaurants"""
    print("\n=== Testing Restaurant Count ===")
    response = requests.get(f"{BASE_URL}/api/restaurants")
    
    if response.status_code != 200:
        print(f"❌ Get restaurants failed: {response.status_code} - {response.text}")
        return False, []
    
    data = response.json()
    restaurant_count = len(data)
    
    if restaurant_count == 13:
        print(f"✅ Found exactly 13 restaurants")
        return True, data
    else:
        print(f"❌ Expected 13 restaurants, got {restaurant_count}")
        return False, data

def test_restaurant_names(restaurants):
    """Verify specific restaurant names exist and removed ones don't"""
    print("\n=== Testing Restaurant Names ===")
    
    # Expected restaurants (should exist)
    expected_names = [
        "Pedro's Chicken", "Mochachos", "Shawarma Express", "Vriespot Frozen Foods", 
        "CAFE E", "Kevcor Take-Aways", "#Braai", "Milano's Brunchies", 
        "Jazbar", "Chantelly's Laundry Services", "No Limit Flowers", 
        "No Limit Parcels", "Witmed Pharmacy & Clinic"
    ]
    
    # Restaurants that should NOT exist (removed)
    removed_names = ["Mr T's Durban Curries", "The Grill House"]
    
    # Renamed restaurant (should NOT exist)
    old_name = "Café Estreito"
    
    restaurant_names = [r["name"] for r in restaurants]
    
    print(f"Found restaurants: {', '.join(restaurant_names)}")
    
    # Check expected restaurants exist
    missing_restaurants = []
    for name in expected_names:
        if name in restaurant_names:
            print(f"✅ Found: {name}")
        else:
            print(f"❌ Missing: {name}")
            missing_restaurants.append(name)
    
    # Check removed restaurants don't exist
    found_removed = []
    for name in removed_names:
        if name in restaurant_names:
            print(f"❌ Should be removed but found: {name}")
            found_removed.append(name)
        else:
            print(f"✅ Correctly removed: {name}")
    
    # Check old name doesn't exist
    if old_name in restaurant_names:
        print(f"❌ Old name still exists: {old_name}")
        found_removed.append(old_name)
    else:
        print(f"✅ Old name correctly removed: {old_name}")
    
    # Check CAFE E exists (renamed from Café Estreito)
    if "CAFE E" in restaurant_names:
        print(f"✅ Renamed restaurant exists: CAFE E")
    else:
        print(f"❌ Renamed restaurant missing: CAFE E")
        missing_restaurants.append("CAFE E")
    
    success = len(missing_restaurants) == 0 and len(found_removed) == 0
    return success, missing_restaurants, found_removed

def test_jazbar_menu(restaurants):
    """Test Jazbar has menu items with categories: Curries, Bunny Chows, Weekly Specials"""
    print("\n=== Testing Jazbar Menu ===")
    
    # Find Jazbar
    jazbar = None
    for restaurant in restaurants:
        if restaurant["name"] == "Jazbar":
            jazbar = restaurant
            break
    
    if not jazbar:
        print("❌ Jazbar restaurant not found")
        return False
    
    print(f"✅ Found Jazbar restaurant")
    
    # Get Jazbar menu
    response = requests.get(f"{BASE_URL}/api/restaurants/{jazbar['restaurant_id']}/menu")
    
    if response.status_code != 200:
        print(f"❌ Get Jazbar menu failed: {response.status_code} - {response.text}")
        return False
    
    menu_items = response.json()
    
    if not menu_items:
        print("❌ Jazbar menu is empty")
        return False
    
    print(f"✅ Jazbar has {len(menu_items)} menu items")
    
    # Check categories
    expected_categories = ["Curries", "Bunny Chows", "Weekly Specials"]
    found_categories = list(set([item["category"] for item in menu_items]))
    
    print(f"Found categories: {', '.join(found_categories)}")
    
    missing_categories = []
    for category in expected_categories:
        if category in found_categories:
            print(f"✅ Found category: {category}")
        else:
            print(f"❌ Missing category: {category}")
            missing_categories.append(category)
    
    # Show sample items from each category
    for category in found_categories:
        items_in_category = [item for item in menu_items if item["category"] == category]
        print(f"  {category}: {len(items_in_category)} items")
        if items_in_category:
            print(f"    Sample: {items_in_category[0]['name']} - R{items_in_category[0]['price']}")
    
    success = len(missing_categories) == 0
    return success

def test_image_uniqueness(restaurants):
    """Test that menu items have image URLs (not empty/null)"""
    print("\n=== Testing Image Uniqueness ===")
    
    # Test a few restaurants
    test_restaurants = restaurants[:3]  # Test first 3 restaurants
    
    all_images_valid = True
    
    for restaurant in test_restaurants:
        print(f"\nTesting images for: {restaurant['name']}")
        
        response = requests.get(f"{BASE_URL}/api/restaurants/{restaurant['restaurant_id']}/menu")
        
        if response.status_code != 200:
            print(f"❌ Failed to get menu for {restaurant['name']}")
            all_images_valid = False
            continue
        
        menu_items = response.json()
        
        if not menu_items:
            print(f"⚠️  No menu items for {restaurant['name']}")
            continue
        
        items_with_images = 0
        items_without_images = 0
        unique_images = set()
        
        for item in menu_items:
            if item.get("image") and item["image"].strip():
                items_with_images += 1
                unique_images.add(item["image"])
            else:
                items_without_images += 1
                print(f"  ❌ No image: {item['name']}")
        
        print(f"  Items with images: {items_with_images}")
        print(f"  Items without images: {items_without_images}")
        print(f"  Unique images: {len(unique_images)}")
        
        if items_without_images > 0:
            all_images_valid = False
        else:
            print(f"  ✅ All items have images")
    
    return all_images_valid

def test_services_count():
    """Test GET /api/services returns 5 service types"""
    print("\n=== Testing Services Count ===")
    
    response = requests.get(f"{BASE_URL}/api/services")
    
    if response.status_code != 200:
        print(f"❌ Get services failed: {response.status_code} - {response.text}")
        return False, []
    
    data = response.json()
    service_count = len(data)
    
    expected_types = ["food", "laundry", "parcel", "florist", "pharmacy"]
    found_types = [service["type"] for service in data]
    
    print(f"Found {service_count} services: {', '.join(found_types)}")
    
    if service_count == 5:
        print(f"✅ Found exactly 5 services")
    else:
        print(f"❌ Expected 5 services, got {service_count}")
        return False, data
    
    # Check expected service types
    missing_types = []
    for service_type in expected_types:
        if service_type in found_types:
            print(f"✅ Found service type: {service_type}")
        else:
            print(f"❌ Missing service type: {service_type}")
            missing_types.append(service_type)
    
    success = service_count == 5 and len(missing_types) == 0
    return success, data

def run_all_tests():
    """Run all backend tests"""
    print("🚀 Starting No Limit Delivery Backend Tests")
    print("=" * 60)
    
    # Test authentication
    auth_token = test_auth_login()
    if not auth_token:
        print("❌ Authentication failed - cannot continue with authenticated tests")
    
    # Test restaurant count
    restaurants_success, restaurants = test_restaurants_count()
    
    if not restaurants_success:
        print("❌ Restaurant count test failed")
        return False
    
    # Test restaurant names
    names_success, missing, found_removed = test_restaurant_names(restaurants)
    
    # Test Jazbar menu
    jazbar_success = test_jazbar_menu(restaurants)
    
    # Test image uniqueness
    images_success = test_image_uniqueness(restaurants)
    
    # Test services count
    services_success, services = test_services_count()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    tests = [
        ("Authentication", auth_token is not None),
        ("Restaurant Count (13)", restaurants_success),
        ("Restaurant Names", names_success),
        ("Jazbar Menu Categories", jazbar_success),
        ("Menu Item Images", images_success),
        ("Services Count (5)", services_success)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, success in tests:
        if success:
            print(f"✅ {test_name}")
            passed += 1
        else:
            print(f"❌ {test_name}")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed")
        
        # Detailed failure info
        if not names_success:
            if missing:
                print(f"Missing restaurants: {', '.join(missing)}")
            if found_removed:
                print(f"Should be removed: {', '.join(found_removed)}")
        
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)