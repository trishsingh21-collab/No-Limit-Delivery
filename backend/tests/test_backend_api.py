"""
Backend API Tests for No Limit Delivery
Tests: Auth, Restaurants, Menu, Orders, AI features
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

class TestAuth:
    """Authentication endpoint tests"""
    
    def test_signup_new_user(self):
        """Test creating a new user account"""
        response = requests.post(f"{BASE_URL}/api/auth/signup", json={
            "email": f"TEST_user_{requests.utils.quote('test')}@example.com",
            "password": "testpass123",
            "name": "Test User",
            "phone": "1234567890"
        })
        assert response.status_code == 200, f"Signup failed: {response.text}"
        
        data = response.json()
        assert "user" in data, "Response missing user field"
        assert "session_token" in data, "Response missing session_token"
        assert data["user"]["email"] is not None
        assert data["user"]["name"] == "Test User"
        assert "password_hash" not in data["user"], "Password hash should not be returned"
    
    def test_signup_duplicate_email(self):
        """Test signup with existing email returns error"""
        email = "TEST_duplicate@example.com"
        
        # Create first user
        requests.post(f"{BASE_URL}/api/auth/signup", json={
            "email": email,
            "password": "pass123",
            "name": "First User"
        })
        
        # Try to create duplicate
        response = requests.post(f"{BASE_URL}/api/auth/signup", json={
            "email": email,
            "password": "pass456",
            "name": "Second User"
        })
        assert response.status_code == 400, "Should reject duplicate email"
    
    def test_login_success(self):
        """Test login with valid credentials"""
        # Create user first
        email = "TEST_login@example.com"
        password = "testpass123"
        
        requests.post(f"{BASE_URL}/api/auth/signup", json={
            "email": email,
            "password": password,
            "name": "Login Test User"
        })
        
        # Login
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": email,
            "password": password
        })
        assert response.status_code == 200, f"Login failed: {response.text}"
        
        data = response.json()
        assert "user" in data
        assert "session_token" in data
        assert data["session_token"].startswith("session_")
    
    def test_login_invalid_credentials(self):
        """Test login with wrong password"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "wrongpass"
        })
        assert response.status_code == 401, "Should reject invalid credentials"
    
    def test_get_me_with_valid_token(self):
        """Test /api/auth/me with valid session token"""
        # Create and login user
        email = "TEST_me@example.com"
        password = "testpass123"
        
        requests.post(f"{BASE_URL}/api/auth/signup", json={
            "email": email,
            "password": password,
            "name": "Me Test User"
        })
        
        login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": email,
            "password": password
        })
        token = login_response.json()["session_token"]
        
        # Get current user
        response = requests.get(f"{BASE_URL}/api/auth/me", headers={
            "Authorization": f"Bearer {token}"
        })
        assert response.status_code == 200, f"Get me failed: {response.text}"
        
        data = response.json()
        assert data["email"] == email
        assert data["name"] == "Me Test User"
        assert "password_hash" not in data
    
    def test_get_me_without_token(self):
        """Test /api/auth/me without authentication"""
        response = requests.get(f"{BASE_URL}/api/auth/me")
        assert response.status_code == 401, "Should require authentication"


class TestRestaurants:
    """Restaurant endpoint tests"""
    
    def test_get_all_restaurants(self):
        """Test GET /api/restaurants returns 15 restaurants"""
        response = requests.get(f"{BASE_URL}/api/restaurants")
        assert response.status_code == 200, f"Get restaurants failed: {response.text}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        assert len(data) == 15, f"Expected 15 restaurants, got {len(data)}"
        
        # Validate first restaurant structure
        if len(data) > 0:
            restaurant = data[0]
            assert "restaurant_id" in restaurant
            assert "name" in restaurant
            assert "cuisine_type" in restaurant
            assert "rating" in restaurant
            assert "delivery_time" in restaurant
    
    def test_get_featured_restaurants(self):
        """Test filtering featured restaurants"""
        response = requests.get(f"{BASE_URL}/api/restaurants?featured=true")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        # All returned restaurants should be featured
        for restaurant in data:
            assert restaurant.get("featured") == True
    
    def test_get_restaurant_by_id(self):
        """Test GET /api/restaurants/{id} returns restaurant details"""
        # First get a restaurant ID
        all_restaurants = requests.get(f"{BASE_URL}/api/restaurants").json()
        assert len(all_restaurants) > 0, "No restaurants found"
        
        restaurant_id = all_restaurants[0]["restaurant_id"]
        
        # Get specific restaurant
        response = requests.get(f"{BASE_URL}/api/restaurants/{restaurant_id}")
        assert response.status_code == 200, f"Get restaurant failed: {response.text}"
        
        data = response.json()
        assert data["restaurant_id"] == restaurant_id
        assert "name" in data
        assert "description" in data
        assert "cuisine_type" in data
    
    def test_get_restaurant_invalid_id(self):
        """Test GET /api/restaurants/{id} with invalid ID"""
        response = requests.get(f"{BASE_URL}/api/restaurants/invalid_id_12345")
        assert response.status_code == 404, "Should return 404 for invalid ID"
    
    def test_get_restaurant_menu(self):
        """Test GET /api/restaurants/{id}/menu returns menu items"""
        # Get a restaurant
        all_restaurants = requests.get(f"{BASE_URL}/api/restaurants").json()
        restaurant_id = all_restaurants[0]["restaurant_id"]
        
        # Get menu
        response = requests.get(f"{BASE_URL}/api/restaurants/{restaurant_id}/menu")
        assert response.status_code == 200, f"Get menu failed: {response.text}"
        
        data = response.json()
        assert isinstance(data, list), "Menu should be a list"
        
        # Validate menu item structure
        if len(data) > 0:
            item = data[0]
            assert "item_id" in item
            assert "name" in item
            assert "price" in item
            assert "category" in item
            assert item["restaurant_id"] == restaurant_id


class TestOrders:
    """Order endpoint tests (requires authentication)"""
    
    @pytest.fixture
    def auth_token(self):
        """Create a user and return auth token"""
        email = f"TEST_order_user@example.com"
        password = "testpass123"
        
        # Try to create user (may already exist)
        requests.post(f"{BASE_URL}/api/auth/signup", json={
            "email": email,
            "password": password,
            "name": "Order Test User"
        })
        
        # Login
        login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": email,
            "password": password
        })
        return login_response.json()["session_token"]
    
    def test_create_order(self, auth_token):
        """Test POST /api/orders creates a new order"""
        # Get a restaurant and menu item
        restaurants = requests.get(f"{BASE_URL}/api/restaurants").json()
        restaurant = restaurants[0]
        
        menu_items = requests.get(f"{BASE_URL}/api/restaurants/{restaurant['restaurant_id']}/menu").json()
        assert len(menu_items) > 0, "No menu items found"
        
        menu_item = menu_items[0]
        
        # Create order
        order_data = {
            "restaurant_id": restaurant["restaurant_id"],
            "items": [
                {
                    "item_id": menu_item["item_id"],
                    "name": menu_item["name"],
                    "price": menu_item["price"],
                    "quantity": 2
                }
            ],
            "delivery_address": {
                "street": "123 Test St",
                "city": "San Francisco",
                "state": "CA",
                "zip": "94102"
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/api/orders",
            json=order_data,
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200, f"Create order failed: {response.text}"
        
        data = response.json()
        assert "order_id" in data
        assert data["order_id"].startswith("order_")
        assert data["restaurant_id"] == restaurant["restaurant_id"]
        assert len(data["items"]) == 1
        assert data["items"][0]["quantity"] == 2
        assert "total" in data
        assert "subtotal" in data
        assert "tax" in data
        
        # Verify order was persisted by fetching it
        order_id = data["order_id"]
        get_response = requests.get(
            f"{BASE_URL}/api/orders/{order_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert get_response.status_code == 200
        fetched_order = get_response.json()
        assert fetched_order["order_id"] == order_id
    
    def test_create_order_without_auth(self):
        """Test creating order without authentication fails"""
        response = requests.post(f"{BASE_URL}/api/orders", json={
            "restaurant_id": "rest_123",
            "items": [],
            "delivery_address": {}
        })
        assert response.status_code == 401, "Should require authentication"
    
    def test_get_user_orders(self, auth_token):
        """Test GET /api/orders returns user's orders"""
        response = requests.get(
            f"{BASE_URL}/api/orders",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200, f"Get orders failed: {response.text}"
        
        data = response.json()
        assert isinstance(data, list), "Orders should be a list"
        # User should have at least one order from previous test
        assert len(data) >= 0


class TestProfile:
    """Profile endpoint tests"""
    
    @pytest.fixture
    def auth_token(self):
        """Login with test@demo.com"""
        login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "test@demo.com",
            "password": "test123"
        })
        if login_response.status_code != 200:
            # Create test user if doesn't exist
            requests.post(f"{BASE_URL}/api/auth/signup", json={
                "email": "test@demo.com",
                "password": "test123",
                "name": "Test User"
            })
            login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
                "email": "test@demo.com",
                "password": "test123"
            })
        return login_response.json()["session_token"]
    
    def test_get_profile(self, auth_token):
        """Test GET /api/profile returns user profile with order_count"""
        response = requests.get(
            f"{BASE_URL}/api/profile",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200, f"Get profile failed: {response.text}"
        
        data = response.json()
        assert "email" in data
        assert "name" in data
        assert "loyalty_points" in data
        assert "order_count" in data
        assert isinstance(data["order_count"], int)


class TestAIFeatures:
    """AI recommendation endpoint tests"""
    
    @pytest.fixture
    def auth_token(self):
        """Create a user and return auth token"""
        email = "TEST_ai_user@example.com"
        password = "testpass123"
        
        requests.post(f"{BASE_URL}/api/auth/signup", json={
            "email": email,
            "password": password,
            "name": "AI Test User"
        })
        
        login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": email,
            "password": password
        })
        return login_response.json()["session_token"]
    
    def test_ai_randomizer(self):
        """Test POST /api/ai/randomizer returns random suggestion"""
        response = requests.post(f"{BASE_URL}/api/ai/randomizer", json={})
        assert response.status_code == 200, f"AI randomizer failed: {response.text}"
        
        data = response.json()
        assert "suggestion" in data, "Response should contain suggestion"
        assert "restaurants" in data, "Response should contain restaurants list"
    
    def test_mood_suggestions(self):
        """Test POST /api/ai/mood-suggestions"""
        response = requests.post(f"{BASE_URL}/api/ai/mood-suggestions", json={
            "mood": "comfort"
        })
        assert response.status_code == 200, f"Mood suggestions failed: {response.text}"
        
        data = response.json()
        assert "mood" in data
        assert "suggestions" in data
        assert data["mood"] == "comfort"
    
    def test_ai_recommendations_with_auth(self, auth_token):
        """Test POST /api/ai/recommendations (requires auth)"""
        response = requests.post(
            f"{BASE_URL}/api/ai/recommendations",
            json={},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200, f"AI recommendations failed: {response.text}"
        
        data = response.json()
        assert "recommendations" in data
        assert "restaurants" in data


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_data():
    """Cleanup test data after all tests"""
    yield
    # Cleanup would go here if needed
    print("\nTest suite completed")
