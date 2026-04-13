#!/usr/bin/env python3
"""
PayFast Payment Integration Testing for No Limit Delivery App
Tests all PayFast payment flows and related functionality
"""

import requests
import json
import time
import sys
from typing import Dict, Any, Optional

# Backend URL from environment
BACKEND_URL = "https://limitless-eats-1.preview.emergentagent.com/api"

# Test credentials
TEST_EMAIL = "test@demo.com"
TEST_PASSWORD = "test123"

class PayFastTester:
    def __init__(self):
        self.session_token = None
        self.user_data = None
        self.test_order_id = None
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   {details}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
        
    def make_request(self, method: str, endpoint: str, data: Dict = None, headers: Dict = None) -> requests.Response:
        """Make HTTP request with proper error handling"""
        url = f"{BACKEND_URL}{endpoint}"
        default_headers = {"Content-Type": "application/json"}
        
        if headers:
            default_headers.update(headers)
            
        if self.session_token and "Authorization" not in default_headers:
            default_headers["Authorization"] = f"Bearer {self.session_token}"
            
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=default_headers, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=default_headers, timeout=30)
            elif method.upper() == "PATCH":
                response = requests.patch(url, json=data, headers=default_headers, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise
            
    def test_login(self) -> bool:
        """Test 1: Login and get session token"""
        try:
            response = self.make_request("POST", "/auth/login", {
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD
            })
            
            if response.status_code == 200:
                data = response.json()
                self.session_token = data.get("session_token")
                self.user_data = data.get("user")
                
                if self.session_token and self.user_data:
                    self.log_test("Login with test credentials", True, 
                                f"User: {self.user_data.get('name')} ({self.user_data.get('email')})")
                    return True
                else:
                    self.log_test("Login with test credentials", False, "Missing session_token or user data")
                    return False
            else:
                self.log_test("Login with test credentials", False, 
                            f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Login with test credentials", False, f"Exception: {str(e)}")
            return False
            
    def test_create_order_payfast(self) -> bool:
        """Test 2: Create an order with payment_method: 'payfast'"""
        try:
            # First get restaurants to create a valid order
            restaurants_response = self.make_request("GET", "/restaurants")
            if restaurants_response.status_code != 200:
                self.log_test("Create order with PayFast", False, "Failed to get restaurants")
                return False
                
            restaurants = restaurants_response.json()
            if not restaurants:
                self.log_test("Create order with PayFast", False, "No restaurants available")
                return False
                
            # Get first restaurant and its menu
            restaurant = restaurants[0]
            menu_response = self.make_request("GET", f"/restaurants/{restaurant['restaurant_id']}/menu")
            if menu_response.status_code != 200:
                self.log_test("Create order with PayFast", False, "Failed to get menu")
                return False
                
            menu_items = menu_response.json()
            if not menu_items:
                self.log_test("Create order with PayFast", False, "No menu items available")
                return False
                
            # Create order with PayFast payment method
            order_data = {
                "restaurant_id": restaurant["restaurant_id"],
                "items": [
                    {
                        "item_id": menu_items[0]["item_id"],
                        "name": menu_items[0]["name"],
                        "price": menu_items[0]["price"],
                        "quantity": 2,
                        "special_instructions": "Test order for PayFast"
                    }
                ],
                "delivery_address": {
                    "street": "123 Test Street",
                    "city": "Witbank",
                    "postal_code": "1035",
                    "lat": -25.8738,
                    "lng": 29.2321
                },
                "payment_method": "payfast",
                "order_notes": "PayFast payment test order",
                "allergies": [],
                "tip": 10.0,
                "promo_code": None
            }
            
            response = self.make_request("POST", "/orders", order_data)
            
            if response.status_code == 200:
                order = response.json()
                self.test_order_id = order.get("order_id")
                
                if self.test_order_id and order.get("payment_method") == "payfast":
                    self.log_test("Create order with PayFast", True, 
                                f"Order ID: {self.test_order_id}, Total: R{order.get('total', 0):.2f}")
                    return True
                else:
                    self.log_test("Create order with PayFast", False, "Missing order_id or incorrect payment_method")
                    return False
            else:
                self.log_test("Create order with PayFast", False, 
                            f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Create order with PayFast", False, f"Exception: {str(e)}")
            return False
            
    def test_create_payfast_payment(self) -> bool:
        """Test 3: Create PayFast payment via POST /api/payments/payfast/create"""
        if not self.test_order_id:
            self.log_test("Create PayFast payment", False, "No test order available")
            return False
            
        try:
            response = self.make_request("POST", "/payments/payfast/create", {
                "order_id": self.test_order_id
            })
            
            if response.status_code == 200:
                payment_data = response.json()
                
                # Verify required fields
                required_fields = ["payfast_url", "payment_data", "order_id", "sandbox"]
                missing_fields = [field for field in required_fields if field not in payment_data]
                
                if missing_fields:
                    self.log_test("Create PayFast payment", False, f"Missing fields: {missing_fields}")
                    return False
                    
                # Verify payment_data structure
                payment_info = payment_data.get("payment_data", {})
                required_payment_fields = ["merchant_id", "merchant_key", "signature", "amount", "return_url", "cancel_url"]
                missing_payment_fields = [field for field in required_payment_fields if field not in payment_info]
                
                if missing_payment_fields:
                    self.log_test("Create PayFast payment", False, f"Missing payment fields: {missing_payment_fields}")
                    return False
                    
                # Verify sandbox flag
                is_sandbox = payment_data.get("sandbox", False)
                payfast_url = payment_data.get("payfast_url", "")
                
                details = f"URL: {payfast_url}, Sandbox: {is_sandbox}, Amount: R{payment_info.get('amount', 'N/A')}"
                self.log_test("Create PayFast payment", True, details)
                return True
            else:
                self.log_test("Create PayFast payment", False, 
                            f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Create PayFast payment", False, f"Exception: {str(e)}")
            return False
            
    def test_payfast_return_url(self) -> bool:
        """Test 4: Test PayFast return URL"""
        if not self.test_order_id:
            self.log_test("PayFast return URL", False, "No test order available")
            return False
            
        try:
            # Test return URL without authentication (should work)
            url = f"{BACKEND_URL}/payments/payfast/return?order_id={self.test_order_id}"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                content = response.text
                
                # Verify HTML response contains success message
                if "Payment Successful" in content and "html" in content.lower():
                    self.log_test("PayFast return URL", True, "Returns HTML with 'Payment Successful' message")
                    return True
                else:
                    self.log_test("PayFast return URL", False, "HTML doesn't contain expected success message")
                    return False
            else:
                self.log_test("PayFast return URL", False, 
                            f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("PayFast return URL", False, f"Exception: {str(e)}")
            return False
            
    def test_payfast_cancel_url(self) -> bool:
        """Test 5: Test PayFast cancel URL"""
        if not self.test_order_id:
            self.log_test("PayFast cancel URL", False, "No test order available")
            return False
            
        try:
            # Test cancel URL without authentication (should work)
            url = f"{BACKEND_URL}/payments/payfast/cancel?order_id={self.test_order_id}"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                content = response.text
                
                # Verify HTML response contains cancel message
                if "Payment Cancelled" in content and "html" in content.lower():
                    self.log_test("PayFast cancel URL", True, "Returns HTML with 'Payment Cancelled' message")
                    return True
                else:
                    self.log_test("PayFast cancel URL", False, "HTML doesn't contain expected cancel message")
                    return False
            else:
                self.log_test("PayFast cancel URL", False, 
                            f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("PayFast cancel URL", False, f"Exception: {str(e)}")
            return False
            
    def test_order_status_update(self) -> bool:
        """Test 6: Verify order status updates after return URL hit"""
        try:
            # Create a fresh order specifically for this test
            restaurants_response = self.make_request("GET", "/restaurants")
            if restaurants_response.status_code != 200:
                self.log_test("Order status update", False, "Failed to get restaurants")
                return False
                
            restaurants = restaurants_response.json()
            if not restaurants:
                self.log_test("Order status update", False, "No restaurants available")
                return False
                
            restaurant = restaurants[0]
            menu_response = self.make_request("GET", f"/restaurants/{restaurant['restaurant_id']}/menu")
            if menu_response.status_code != 200:
                self.log_test("Order status update", False, "Failed to get menu")
                return False
                
            menu_items = menu_response.json()
            if not menu_items:
                self.log_test("Order status update", False, "No menu items available")
                return False
                
            # Create fresh order for status test
            order_data = {
                "restaurant_id": restaurant["restaurant_id"],
                "items": [
                    {
                        "item_id": menu_items[0]["item_id"],
                        "name": menu_items[0]["name"],
                        "price": menu_items[0]["price"],
                        "quantity": 1,
                        "special_instructions": "Test order for status update"
                    }
                ],
                "delivery_address": {
                    "street": "999 Status Test Street",
                    "city": "Witbank",
                    "postal_code": "1035",
                    "lat": -25.8738,
                    "lng": 29.2321
                },
                "payment_method": "payfast",
                "order_notes": "Status update test order",
                "allergies": [],
                "tip": 0.0,
                "promo_code": None
            }
            
            order_response = self.make_request("POST", "/orders", order_data)
            if order_response.status_code != 200:
                self.log_test("Order status update", False, "Failed to create test order")
                return False
                
            order = order_response.json()
            test_order_id = order.get("order_id")
            
            if not test_order_id:
                self.log_test("Order status update", False, "No order ID from created order")
                return False
            
            # Create PayFast payment to set status to "awaiting_payment"
            payment_response = self.make_request("POST", "/payments/payfast/create", {
                "order_id": test_order_id
            })
            
            if payment_response.status_code != 200:
                self.log_test("Order status update", False, "Failed to create PayFast payment")
                return False
            
            # Now hit the return URL to trigger status update
            return_url = f"{BACKEND_URL}/payments/payfast/return?order_id={test_order_id}"
            requests.get(return_url, timeout=30)
            
            # Wait a moment for the update to process
            time.sleep(1)
            
            # Check order status
            response = self.make_request("GET", f"/orders/{test_order_id}")
            
            if response.status_code == 200:
                updated_order = response.json()
                status = updated_order.get("status")
                payment_status = updated_order.get("payment_status")
                
                if status == "confirmed":
                    self.log_test("Order status update", True, 
                                f"Order status: {status}, Payment status: {payment_status}")
                    return True
                else:
                    self.log_test("Order status update", False, 
                                f"Expected 'confirmed', got '{status}'. Payment status: {payment_status}")
                    return False
            else:
                self.log_test("Order status update", False, 
                            f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Order status update", False, f"Exception: {str(e)}")
            return False
            
    def test_cash_order(self) -> bool:
        """Test 7: Test cash order creation"""
        try:
            # Get restaurants and menu (reuse logic from payfast test)
            restaurants_response = self.make_request("GET", "/restaurants")
            if restaurants_response.status_code != 200:
                self.log_test("Cash order creation", False, "Failed to get restaurants")
                return False
                
            restaurants = restaurants_response.json()
            if not restaurants:
                self.log_test("Cash order creation", False, "No restaurants available")
                return False
                
            restaurant = restaurants[0]
            menu_response = self.make_request("GET", f"/restaurants/{restaurant['restaurant_id']}/menu")
            if menu_response.status_code != 200:
                self.log_test("Cash order creation", False, "Failed to get menu")
                return False
                
            menu_items = menu_response.json()
            if not menu_items:
                self.log_test("Cash order creation", False, "No menu items available")
                return False
                
            # Create cash order
            order_data = {
                "restaurant_id": restaurant["restaurant_id"],
                "items": [
                    {
                        "item_id": menu_items[0]["item_id"],
                        "name": menu_items[0]["name"],
                        "price": menu_items[0]["price"],
                        "quantity": 1,
                        "special_instructions": "Test cash order"
                    }
                ],
                "delivery_address": {
                    "street": "456 Cash Street",
                    "city": "Witbank",
                    "postal_code": "1035",
                    "lat": -25.8738,
                    "lng": 29.2321
                },
                "payment_method": "cash",
                "order_notes": "Cash payment test order",
                "allergies": [],
                "tip": 5.0,
                "promo_code": None
            }
            
            response = self.make_request("POST", "/orders", order_data)
            
            if response.status_code == 200:
                order = response.json()
                order_id = order.get("order_id")
                payment_method = order.get("payment_method")
                
                if order_id and payment_method == "cash":
                    self.log_test("Cash order creation", True, 
                                f"Order ID: {order_id}, Total: R{order.get('total', 0):.2f}")
                    return True
                else:
                    self.log_test("Cash order creation", False, "Missing order_id or incorrect payment_method")
                    return False
            else:
                self.log_test("Cash order creation", False, 
                            f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Cash order creation", False, f"Exception: {str(e)}")
            return False
            
    def test_eft_order(self) -> bool:
        """Test 8: Test EFT order creation"""
        try:
            # Get restaurants and menu (reuse logic)
            restaurants_response = self.make_request("GET", "/restaurants")
            if restaurants_response.status_code != 200:
                self.log_test("EFT order creation", False, "Failed to get restaurants")
                return False
                
            restaurants = restaurants_response.json()
            if not restaurants:
                self.log_test("EFT order creation", False, "No restaurants available")
                return False
                
            restaurant = restaurants[0]
            menu_response = self.make_request("GET", f"/restaurants/{restaurant['restaurant_id']}/menu")
            if menu_response.status_code != 200:
                self.log_test("EFT order creation", False, "Failed to get menu")
                return False
                
            menu_items = menu_response.json()
            if not menu_items:
                self.log_test("EFT order creation", False, "No menu items available")
                return False
                
            # Create EFT order
            order_data = {
                "restaurant_id": restaurant["restaurant_id"],
                "items": [
                    {
                        "item_id": menu_items[0]["item_id"],
                        "name": menu_items[0]["name"],
                        "price": menu_items[0]["price"],
                        "quantity": 1,
                        "special_instructions": "Test EFT order"
                    }
                ],
                "delivery_address": {
                    "street": "789 EFT Avenue",
                    "city": "Witbank",
                    "postal_code": "1035",
                    "lat": -25.8738,
                    "lng": 29.2321
                },
                "payment_method": "eft",
                "order_notes": "EFT payment test order",
                "allergies": [],
                "tip": 7.5,
                "promo_code": None
            }
            
            response = self.make_request("POST", "/orders", order_data)
            
            if response.status_code == 200:
                order = response.json()
                order_id = order.get("order_id")
                payment_method = order.get("payment_method")
                
                if order_id and payment_method == "eft":
                    self.log_test("EFT order creation", True, 
                                f"Order ID: {order_id}, Total: R{order.get('total', 0):.2f}")
                    return True
                else:
                    self.log_test("EFT order creation", False, "Missing order_id or incorrect payment_method")
                    return False
            else:
                self.log_test("EFT order creation", False, 
                            f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("EFT order creation", False, f"Exception: {str(e)}")
            return False
            
    def run_all_tests(self):
        """Run all PayFast integration tests"""
        print("🚀 Starting PayFast Payment Integration Tests")
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Test Credentials: {TEST_EMAIL} / {TEST_PASSWORD}")
        print("=" * 60)
        
        # Test sequence
        tests = [
            self.test_login,
            self.test_create_order_payfast,
            self.test_create_payfast_payment,
            self.test_payfast_return_url,
            self.test_payfast_cancel_url,
            self.test_order_status_update,
            self.test_cash_order,
            self.test_eft_order
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
            except Exception as e:
                print(f"❌ FAIL {test.__name__}: Unexpected error: {str(e)}")
                
        print("=" * 60)
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All PayFast integration tests PASSED!")
            return True
        else:
            print("⚠️  Some tests FAILED. Check details above.")
            return False

def main():
    """Main test runner"""
    tester = PayFastTester()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()