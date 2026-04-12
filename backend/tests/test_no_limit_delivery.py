"""
Backend API Tests for No Limit Delivery - Multi-Service Platform
Tests: Auth, Services, Restaurants (with service_type filtering), Menu (ZAR prices), Orders (R25 delivery, 15% VAT)
"""
import pytest
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

# Load frontend .env to get EXPO_PUBLIC_BACKEND_URL
frontend_env = Path(__file__).parent.parent.parent / 'frontend' / '.env'
load_dotenv(frontend_env)

BASE_URL = os.environ.get('EXPO_PUBLIC_BACKEND_URL', '').rstrip('/')
if not BASE_URL:
    raise ValueError("EXPO_PUBLIC_BACKEND_URL not found in environment")

print(f"\n🔗 Testing against: {BASE_URL}")


class TestAuth:
    """Authentication tests"""
    
    def test_login_with_test_credentials(self):
        """Test login with test@demo.com / test123"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "test@demo.com",
            "password": "test123"
        })
        assert response.status_code == 200, f"Login failed: {response.text}"
        
        data = response.json()
        assert "user" in data
        assert "session_token" in data
        assert data["user"]["email"] == "test@demo.com"
        assert data["session_token"].startswith("session_")
        print(f"✓ Login successful for test@demo.com")


class TestServices:
    """Service categories tests"""
    
    def test_get_services_returns_4_categories(self):
        """Test GET /api/services returns 4 service categories"""
        response = requests.get(f"{BASE_URL}/api/services")
        assert response.status_code == 200, f"Get services failed: {response.text}"
        
        data = response.json()
        assert isinstance(data, list), "Services should be a list"
        assert len(data) == 4, f"Expected 4 services, got {len(data)}"
        
        # Verify service types
        service_types = [s["type"] for s in data]
        assert "food" in service_types
        assert "laundry" in service_types
        assert "parcel" in service_types
        assert "florist" in service_types
        
        print(f"✓ Found 4 service categories: {', '.join(service_types)}")


class TestRestaurants:
    """Restaurant and provider tests"""
    
    def test_get_restaurants_returns_8_providers(self):
        """Test GET /api/restaurants returns 8 providers"""
        response = requests.get(f"{BASE_URL}/api/restaurants")
        assert response.status_code == 200, f"Get restaurants failed: {response.text}"
        
        data = response.json()
        assert isinstance(data, list), "Restaurants should be a list"
        assert len(data) == 8, f"Expected 8 providers, got {len(data)}"
        
        # Verify all have service_type field
        for provider in data:
            assert "service_type" in provider, f"Provider {provider['name']} missing service_type"
            assert provider["service_type"] in ["food", "laundry", "parcel", "florist"]
        
        print(f"✓ Found 8 providers with service_type field")
    
    def test_filter_by_service_type_food(self):
        """Test GET /api/restaurants?service_type=food returns only food restaurants"""
        response = requests.get(f"{BASE_URL}/api/restaurants?service_type=food")
        assert response.status_code == 200, f"Filter failed: {response.text}"
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 5, f"Expected 5 food restaurants, got {len(data)}"
        
        # Verify all are food type
        for restaurant in data:
            assert restaurant["service_type"] == "food", f"{restaurant['name']} is not food type"
        
        # Verify South African restaurants
        names = [r["name"] for r in data]
        assert "Pedro's Chicken" in names
        assert "Mochachos" in names
        assert "The Grill House" in names
        assert "Shawarma Express" in names
        assert "Mr T's Durban Curries" in names
        
        print(f"✓ Food filter returns 5 SA restaurants: {', '.join(names)}")
    
    def test_filter_by_service_type_laundry(self):
        """Test GET /api/restaurants?service_type=laundry returns laundry service"""
        response = requests.get(f"{BASE_URL}/api/restaurants?service_type=laundry")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1, f"Expected 1 laundry service, got {len(data)}"
        assert data[0]["service_type"] == "laundry"
        
        print(f"✓ Laundry filter returns: {data[0]['name']}")
    
    def test_filter_by_service_type_parcel(self):
        """Test GET /api/restaurants?service_type=parcel returns parcel service"""
        response = requests.get(f"{BASE_URL}/api/restaurants?service_type=parcel")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1, f"Expected 1 parcel service, got {len(data)}"
        assert data[0]["service_type"] == "parcel"
        
        print(f"✓ Parcel filter returns: {data[0]['name']}")
    
    def test_filter_by_service_type_florist(self):
        """Test GET /api/restaurants?service_type=florist returns florist service"""
        response = requests.get(f"{BASE_URL}/api/restaurants?service_type=florist")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1, f"Expected 1 florist service, got {len(data)}"
        assert data[0]["service_type"] == "florist"
        
        print(f"✓ Florist filter returns: {data[0]['name']}")
    
    def test_restaurant_has_zar_price_range(self):
        """Test restaurants have ZAR price ranges (R prefix)"""
        response = requests.get(f"{BASE_URL}/api/restaurants")
        data = response.json()
        
        for restaurant in data:
            if restaurant["service_type"] == "food":
                assert "price_range" in restaurant
                assert restaurant["price_range"].startswith("R"), f"{restaurant['name']} price_range doesn't start with R"
        
        print(f"✓ All food restaurants have ZAR price ranges (R prefix)")


class TestMenu:
    """Menu and pricing tests"""
    
    def test_get_menu_returns_items_with_zar_prices(self):
        """Test GET /api/restaurants/{id}/menu returns menu items with ZAR prices"""
        # Get Pedro's Chicken
        restaurants = requests.get(f"{BASE_URL}/api/restaurants?service_type=food").json()
        pedros = next((r for r in restaurants if "Pedro" in r["name"]), None)
        assert pedros is not None, "Pedro's Chicken not found"
        
        # Get menu
        response = requests.get(f"{BASE_URL}/api/restaurants/{pedros['restaurant_id']}/menu")
        assert response.status_code == 200, f"Get menu failed: {response.text}"
        
        data = response.json()
        assert isinstance(data, list), "Menu should be a list"
        assert len(data) > 0, "Menu should have items"
        
        # Verify menu items have prices
        for item in data:
            assert "price" in item
            assert isinstance(item["price"], (int, float))
            assert item["price"] > 0
            assert "name" in item
            assert "category" in item
        
        print(f"✓ Pedro's Chicken menu has {len(data)} items with ZAR prices")
        print(f"  Sample: {data[0]['name']} - R{data[0]['price']}")


class TestOrders:
    """Order creation and pricing tests"""
    
    @pytest.fixture
    def auth_token(self):
        """Login with test@demo.com"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "test@demo.com",
            "password": "test123"
        })
        return response.json()["session_token"]
    
    def test_create_order_with_zar_pricing(self, auth_token):
        """Test POST /api/orders creates order with ZAR pricing (R25 delivery, 15% VAT)"""
        # Get a food restaurant and menu item
        restaurants = requests.get(f"{BASE_URL}/api/restaurants?service_type=food").json()
        restaurant = restaurants[0]
        
        menu_items = requests.get(f"{BASE_URL}/api/restaurants/{restaurant['restaurant_id']}/menu").json()
        assert len(menu_items) > 0, "No menu items found"
        
        menu_item = menu_items[0]
        quantity = 2
        
        # Create order
        order_data = {
            "restaurant_id": restaurant["restaurant_id"],
            "items": [
                {
                    "item_id": menu_item["item_id"],
                    "name": menu_item["name"],
                    "price": menu_item["price"],
                    "quantity": quantity
                }
            ],
            "delivery_address": {
                "street": "123 Test St",
                "city": "Witbank",
                "zip": "1035"
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/api/orders",
            json=order_data,
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200, f"Create order failed: {response.text}"
        
        data = response.json()
        
        # Verify order structure
        assert "order_id" in data
        assert "subtotal" in data
        assert "delivery_fee" in data
        assert "tax" in data
        assert "total" in data
        
        # Verify pricing calculations
        expected_subtotal = menu_item["price"] * quantity
        expected_delivery = 25.00  # R25 delivery fee
        expected_tax = expected_subtotal * 0.15  # 15% VAT
        expected_total = expected_subtotal + expected_delivery + expected_tax
        
        assert abs(data["subtotal"] - expected_subtotal) < 0.01, f"Subtotal mismatch: {data['subtotal']} != {expected_subtotal}"
        assert abs(data["delivery_fee"] - expected_delivery) < 0.01, f"Delivery fee should be R25, got R{data['delivery_fee']}"
        assert abs(data["tax"] - expected_tax) < 0.01, f"Tax should be 15%, got {data['tax']}"
        assert abs(data["total"] - expected_total) < 0.01, f"Total mismatch: {data['total']} != {expected_total}"
        
        print(f"✓ Order created with correct ZAR pricing:")
        print(f"  Subtotal: R{data['subtotal']:.2f}")
        print(f"  Delivery: R{data['delivery_fee']:.2f}")
        print(f"  VAT (15%): R{data['tax']:.2f}")
        print(f"  Total: R{data['total']:.2f}")
        
        # Verify order was persisted
        get_response = requests.get(
            f"{BASE_URL}/api/orders/{data['order_id']}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert get_response.status_code == 200
        print(f"✓ Order persisted successfully")


class TestCuisineCategories:
    """Test cuisine categories match requirements"""
    
    def test_categories_match_requirements(self):
        """Test categories include Chicken, Mexican, Grill, Shawarma, Curry, Flowers, Laundry, Parcels"""
        response = requests.get(f"{BASE_URL}/api/restaurants")
        data = response.json()
        
        cuisine_types = [r["cuisine_type"] for r in data]
        
        # Food categories
        assert "Chicken" in cuisine_types
        assert "Mexican Chicken" in cuisine_types
        assert "Grill & BBQ" in cuisine_types
        assert "Shawarma & Grill" in cuisine_types
        assert "Indian & Curry" in cuisine_types
        
        # Service categories
        assert "Florist" in cuisine_types
        assert "Laundry" in cuisine_types
        assert "Parcel Delivery" in cuisine_types
        
        print(f"✓ All required categories present: {', '.join(cuisine_types)}")


@pytest.fixture(scope="session", autouse=True)
def test_summary():
    """Print test summary"""
    yield
    print("\n" + "="*60)
    print("✅ No Limit Delivery Backend Tests Complete")
    print("="*60)
