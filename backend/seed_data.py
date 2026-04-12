"""Seed script for No Limit Delivery - South African multi-service platform"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import uuid
from datetime import datetime, timezone

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["test_database"]

async def seed():
    # Clear existing data
    await db.restaurants.drop()
    await db.menu_items.drop()
    await db.services.drop()
    
    # ==================== SERVICE CATEGORIES ====================
    services = [
        {"service_id": "svc_food", "name": "Food Delivery", "icon": "restaurant", "emoji": "🍔", "type": "food", "description": "Order from your favourite restaurants", "active": True},
        {"service_id": "svc_laundry", "name": "Laundry", "icon": "shirt", "emoji": "👔", "type": "laundry", "description": "Pick up, clean & deliver back", "active": True},
        {"service_id": "svc_parcel", "name": "Parcel Delivery", "icon": "cube", "emoji": "📦", "type": "parcel", "description": "Door-to-door delivery", "active": True},
        {"service_id": "svc_florist", "name": "Florist", "icon": "flower", "emoji": "💐", "type": "florist", "description": "Fresh flowers delivered", "active": True},
    ]
    await db.services.insert_many(services)
    print(f"Seeded {len(services)} services")

    # ==================== PEDRO'S CHICKEN ====================
    pedros_id = f"rest_{uuid.uuid4().hex[:12]}"
    pedros = {
        "restaurant_id": pedros_id,
        "name": "Pedro's Chicken",
        "description": "Flame-grilled peri-peri chicken, burgers, wraps and family meals. The fastest-growing chicken franchise in South Africa!",
        "image": "https://images.unsplash.com/photo-1626645738196-c2a7c87a8f58",
        "cuisine_type": "Chicken",
        "rating": 4.6,
        "delivery_time": "25-35 min",
        "price_range": "R30-R310",
        "location": {"lat": -25.8744, "lng": 29.2339, "address": "Witbank, Emalahleni, South Africa"},
        "featured": True,
        "active": True,
        "service_type": "food",
        "menu_categories": ["Chicken Only", "Chicken Meals", "Family Meals", "Burger Meals", "Wraps", "Single Meals", "Kids Meals", "Sides", "Snacks"],
        "available_hours": {"weekdays": "09:00 - 21:00", "weekends": "09:00 - 22:00", "is_open": True},
    }
    await db.restaurants.insert_one(pedros)
    
    pedros_items = [
        # Chicken Only
        {"name": "1/4 Chicken", "description": "Flame-grilled peri-peri quarter chicken", "price": 29.99, "category": "Chicken Only", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Q-Chicken_500x500.png"},
        {"name": "1/2 Chicken", "description": "Flame-grilled peri-peri half chicken", "price": 59.99, "category": "Chicken Only", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Half-Chicken_500x500-1.png"},
        {"name": "Full Chicken", "description": "Flame-grilled peri-peri full chicken", "price": 119.99, "category": "Chicken Only", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Full-Chicken_500x500.png"},
        {"name": "4 Wings", "description": "4 flame-grilled peri-peri wings", "price": 39.99, "category": "Chicken Only", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/4-Wings_500x500.png"},
        # Chicken Meals
        {"name": "1/4 Chicken & Chips", "description": "Quarter chicken with chips", "price": 44.99, "category": "Chicken Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Q-Chicken-Chips_400x400.png"},
        {"name": "1/4 Chicken, Chips & Roll", "description": "Quarter chicken with chips and Portuguese roll", "price": 49.99, "category": "Chicken Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Q-Chicken-Chips-Roll_500x500.png"},
        {"name": "1/4 Chicken Meal", "description": "Quarter chicken, chips, roll, coleslaw & drink", "price": 59.99, "category": "Chicken Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Q-Chicken-Meal_500x500.png"},
        {"name": "1/2 Chicken & Chips", "description": "Half chicken with chips", "price": 79.99, "category": "Chicken Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Half-Chicken-and-Chips_500x500.png"},
        {"name": "1/2 Chicken Meal", "description": "Half chicken, chips, roll, coleslaw & drink", "price": 89.99, "category": "Chicken Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Half-Chicken-Meal_500x500.png"},
        {"name": "1/4 Chicken Paella", "description": "Quarter chicken with paella rice", "price": 46.99, "category": "Chicken Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Q-Chicken-Paella_500x500.png"},
        {"name": "4 Wings & Chips", "description": "4 wings with chips", "price": 49.99, "category": "Chicken Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/4-Wings-Chips_500x500.png"},
        # Family Meals
        {"name": "Viva Meal", "description": "Full chicken, large chips & 4 rolls", "price": 155.99, "category": "Family Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Viva-Meal_500x500.png"},
        {"name": "Full Meal", "description": "Full chicken, large chips, 4 rolls, large coleslaw & 2L drink", "price": 199.99, "category": "Family Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Full-Meal_500x500.png"},
        {"name": "Mega Meal", "description": "2 full chickens, 2 large chips & 8 rolls", "price": 309.99, "category": "Family Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Mega-Meal_500x500.png"},
        {"name": "Mini Combo", "description": "Full chicken, 8 wings, large chips & 4 rolls", "price": 219.99, "category": "Family Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Mini-Combo_500x500.png"},
        # Burger Meals
        {"name": "Chicken Burger", "description": "Flame-grilled chicken breast burger", "price": 35.99, "category": "Burger Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Chicken-Burger_500x500.png"},
        {"name": "Chicken Burger & Chips", "description": "Chicken burger served with chips", "price": 45.99, "category": "Burger Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Chicken-Burger-Chips_500x500.png"},
        {"name": "Cheese Burger & Chips", "description": "Chicken cheese burger with chips", "price": 49.99, "category": "Burger Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Cheese-Burger-Chips_500x500.png"},
        {"name": "Don Pedro Burger & Chips", "description": "Signature Don Pedro burger with chips", "price": 45.99, "category": "Burger Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Don-Pedro-Chips_500x500.png"},
        {"name": "Double Up & Chips", "description": "Double chicken burger with chips", "price": 79.99, "category": "Burger Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Double-Up-Chips_500x500.png"},
        # Wraps
        {"name": "Slaw Wrap", "description": "Chicken wrap with coleslaw", "price": 36.99, "category": "Wraps", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Slaw-Wrap_500x500.png"},
        {"name": "Chicken Wrap & Chips", "description": "Chicken wrap served with chips", "price": 49.99, "category": "Wraps", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Chicken-Wrap-Chips_500x500-.png"},
        {"name": "Cheesy Jalapeño Wrap", "description": "Spicy cheesy jalapeño chicken wrap", "price": 46.99, "category": "Wraps", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Cheesy-Jalapeno-Wrap_500x500.png"},
        {"name": "Fully Loaded Wrap & Chips", "description": "Fully loaded chicken wrap with chips", "price": 59.99, "category": "Wraps", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Fully-Loaded-Wrap-Chips_500x500.png"},
        # Sides
        {"name": "Regular Chips", "description": "Portion of crispy chips", "price": 17.99, "category": "Sides", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Regular-Chips_500x500.png"},
        {"name": "Large Chips", "description": "Large portion of crispy chips", "price": 27.99, "category": "Sides", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Large-Chips_500x500.png"},
        {"name": "Garlic Roll", "description": "Freshly baked garlic roll", "price": 9.99, "category": "Sides", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Garlic-Roll_500x500.png"},
        {"name": "Loaded Fries", "description": "Chips loaded with toppings", "price": 36.99, "category": "Sides", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Loaded-Fries_500x500.png"},
        {"name": "Pap & Chakalaka", "description": "Traditional pap with chakalaka", "price": 19.99, "category": "Sides", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Pap-Chakalaka_500x500.png"},
        {"name": "Coleslaw Salad", "description": "Fresh coleslaw salad", "price": 17.99, "category": "Sides", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Coleslaw-Salad_500x500.png"},
    ]
    
    for item in pedros_items:
        await db.menu_items.insert_one({
            "item_id": f"item_{uuid.uuid4().hex[:12]}",
            "restaurant_id": pedros_id,
            "available": True,
            "dietary_tags": [],
            **item,
        })
    print(f"Seeded Pedro's Chicken: {len(pedros_items)} items")

    # ==================== MOCHACHOS ====================
    mochachos_id = f"rest_{uuid.uuid4().hex[:12]}"
    mochachos = {
        "restaurant_id": mochachos_id,
        "name": "Mochachos",
        "description": "Mexican-inspired flame-grilled chicken. Famous for dry spiced chicken, oversized burgers, burritos, enchiladas, fajitas & chimichangas. Spicy but Not Hot!",
        "image": "https://images.unsplash.com/photo-1599021277840-9d3f4f383742",
        "cuisine_type": "Mexican Chicken",
        "rating": 4.5,
        "delivery_time": "30-40 min",
        "price_range": "R35-R180",
        "location": {"lat": -25.8744, "lng": 29.2339, "address": "Saveways Crescent Shopping Centre, Witbank, Emalahleni"},
        "featured": True,
        "active": True,
        "service_type": "food",
        "menu_categories": ["Flame Grilled Chicken", "Burgers", "Mexican Specials", "Wraps & Burritos", "Sides & Extras"],
        "available_hours": {"weekdays": "10:00 - 21:00", "weekends": "09:00 - 22:00", "is_open": True},
    }
    await db.restaurants.insert_one(mochachos)
    
    mochachos_items = [
        {"name": "1/4 Flame Grilled Chicken", "description": "Dry spiced flame-grilled chicken, your choice of flavour", "price": 39.99, "category": "Flame Grilled Chicken", "image": "https://images.unsplash.com/photo-1626645738196-c2a7c87a8f58"},
        {"name": "1/2 Flame Grilled Chicken", "description": "Half flame-grilled chicken with your choice of flavour", "price": 69.99, "category": "Flame Grilled Chicken", "image": "https://images.unsplash.com/photo-1626645738196-c2a7c87a8f58"},
        {"name": "Full Flame Grilled Chicken", "description": "Full flame-grilled chicken - Lemon & Herb, Mild, Hot or Dynamite", "price": 129.99, "category": "Flame Grilled Chicken", "image": "https://images.unsplash.com/photo-1626645738196-c2a7c87a8f58"},
        {"name": "8 BBQ Wings & Chips", "description": "8 wings basted in sticky BBQ sauce with beeger chips", "price": 79.99, "category": "Flame Grilled Chicken", "image": "https://images.unsplash.com/photo-1527477396000-e27163b4bbed"},
        {"name": "Chicken Fillet Burger", "description": "Oversized flame-grilled chicken fillet burger", "price": 54.99, "category": "Burgers", "image": "https://images.unsplash.com/photo-1593022754339-f23454332fd8"},
        {"name": "Cheese Chicken Burger", "description": "Chicken fillet burger with melted cheese", "price": 59.99, "category": "Burgers", "image": "https://images.unsplash.com/photo-1593022754339-f23454332fd8"},
        {"name": "Mexican Burger", "description": "Chicken burger with salsa, guacamole & jalapeños", "price": 64.99, "category": "Burgers", "image": "https://images.unsplash.com/photo-1593022754339-f23454332fd8"},
        {"name": "Chicken Enchilada", "description": "Tortilla filled with chicken, covered in salsa & melted cheese", "price": 74.99, "category": "Mexican Specials", "image": "https://images.unsplash.com/photo-1534352956036-cd81e27dd615"},
        {"name": "Chicken Fajitas", "description": "Two tortillas with chicken, sautéed onion & peppers, rice, salad, cheese, sour cream & guacamole", "price": 89.99, "category": "Mexican Specials", "image": "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b"},
        {"name": "Classic Nachos", "description": "Crispy tortilla chips with salsa, melted cheese, sour cream, guacamole & jalapeños", "price": 59.99, "category": "Mexican Specials", "image": "https://images.unsplash.com/photo-1513456852971-30c0b8199d4d"},
        {"name": "Quesadilla", "description": "Toasted tortillas with chicken, onion, green pepper & cheddar cheese", "price": 64.99, "category": "Mexican Specials", "image": "https://images.unsplash.com/photo-1618040996337-56904b7850b9"},
        {"name": "Chicken Burrito", "description": "Large flour tortilla filled with chicken, Mexican rice, beans & salad", "price": 69.99, "category": "Wraps & Burritos", "image": "https://images.unsplash.com/photo-1626700051175-6818013e1d4f"},
        {"name": "Chimichanga", "description": "Deep-fried burrito with chicken, cheese & Mexican rice", "price": 74.99, "category": "Wraps & Burritos", "image": "https://images.unsplash.com/photo-1626700051175-6818013e1d4f"},
        {"name": "Mexican Rice", "description": "Flavourful Mexican-style rice", "price": 24.99, "category": "Sides & Extras", "image": "https://images.unsplash.com/photo-1596560548464-f010549b84d7"},
        {"name": "Beeger Chips", "description": "Large portion of crispy chips", "price": 29.99, "category": "Sides & Extras", "image": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877"},
        {"name": "Corn on the Cob", "description": "Grilled corn on the cob with butter", "price": 19.99, "category": "Sides & Extras", "image": "https://images.unsplash.com/photo-1551754655-cd27e38d2076"},
    ]
    
    for item in mochachos_items:
        await db.menu_items.insert_one({
            "item_id": f"item_{uuid.uuid4().hex[:12]}",
            "restaurant_id": mochachos_id,
            "available": True,
            "dietary_tags": [],
            **item,
        })
    print(f"Seeded Mochachos: {len(mochachos_items)} items")

    # ==================== LAUNDRY SERVICE ====================
    laundry_id = f"rest_{uuid.uuid4().hex[:12]}"
    laundry = {
        "restaurant_id": laundry_id,
        "name": "No Limit Laundry",
        "description": "Professional laundry service. We pick up your dirty clothes, clean them, and deliver them back fresh and folded!",
        "image": "https://images.unsplash.com/photo-1545173168-9f1947eebb7f",
        "cuisine_type": "Laundry",
        "rating": 4.7,
        "delivery_time": "24-48 hrs",
        "price_range": "R15-R80/item",
        "location": {"lat": -25.8744, "lng": 29.2339, "address": "Witbank, Emalahleni"},
        "featured": True,
        "active": True,
        "service_type": "laundry",
        "menu_categories": ["Wash & Fold", "Dry Cleaning", "Ironing", "Special Items"],
        "available_hours": {"weekdays": "07:00 - 18:00", "weekends": "08:00 - 14:00", "is_open": True},
    }
    await db.restaurants.insert_one(laundry)
    
    laundry_items = [
        {"name": "Wash & Fold (per kg)", "description": "Standard wash, dry and fold service", "price": 25.00, "category": "Wash & Fold", "image": "https://images.unsplash.com/photo-1545173168-9f1947eebb7f"},
        {"name": "Shirt / Blouse", "description": "Wash and iron", "price": 20.00, "category": "Wash & Fold", "image": "https://images.unsplash.com/photo-1545173168-9f1947eebb7f"},
        {"name": "Trousers / Jeans", "description": "Wash and iron", "price": 25.00, "category": "Wash & Fold", "image": "https://images.unsplash.com/photo-1545173168-9f1947eebb7f"},
        {"name": "Bedding Set", "description": "Duvet cover, sheet & 2 pillowcases", "price": 80.00, "category": "Wash & Fold", "image": "https://images.unsplash.com/photo-1545173168-9f1947eebb7f"},
        {"name": "Suit (2-piece)", "description": "Professional dry cleaning", "price": 75.00, "category": "Dry Cleaning", "image": "https://images.unsplash.com/photo-1545173168-9f1947eebb7f"},
        {"name": "Dress", "description": "Dry clean and press", "price": 60.00, "category": "Dry Cleaning", "image": "https://images.unsplash.com/photo-1545173168-9f1947eebb7f"},
        {"name": "Jacket / Blazer", "description": "Dry clean and press", "price": 55.00, "category": "Dry Cleaning", "image": "https://images.unsplash.com/photo-1545173168-9f1947eebb7f"},
        {"name": "Ironing Only (per item)", "description": "Professional pressing service", "price": 15.00, "category": "Ironing", "image": "https://images.unsplash.com/photo-1545173168-9f1947eebb7f"},
        {"name": "Curtains (per panel)", "description": "Wash and iron curtain panels", "price": 45.00, "category": "Special Items", "image": "https://images.unsplash.com/photo-1545173168-9f1947eebb7f"},
        {"name": "Duvet / Comforter", "description": "Deep clean large duvets", "price": 70.00, "category": "Special Items", "image": "https://images.unsplash.com/photo-1545173168-9f1947eebb7f"},
    ]
    
    for item in laundry_items:
        await db.menu_items.insert_one({
            "item_id": f"item_{uuid.uuid4().hex[:12]}",
            "restaurant_id": laundry_id,
            "available": True,
            "dietary_tags": [],
            **item,
        })
    print(f"Seeded No Limit Laundry: {len(laundry_items)} items")

    # ==================== FLORIST ====================
    florist_id = f"rest_{uuid.uuid4().hex[:12]}"
    florist = {
        "restaurant_id": florist_id,
        "name": "No Limit Flowers",
        "description": "Beautiful fresh flower arrangements delivered to your door. Perfect for birthdays, anniversaries, or just because!",
        "image": "https://images.unsplash.com/photo-1487530811176-3780de880c2d",
        "cuisine_type": "Florist",
        "rating": 4.8,
        "delivery_time": "2-4 hrs",
        "price_range": "R150-R800",
        "location": {"lat": -25.8744, "lng": 29.2339, "address": "Witbank, Emalahleni"},
        "featured": True,
        "active": True,
        "service_type": "florist",
        "menu_categories": ["Bouquets", "Arrangements", "Roses", "Add-ons"],
        "available_hours": {"weekdays": "08:00 - 17:00", "weekends": "08:00 - 13:00", "is_open": True},
    }
    await db.restaurants.insert_one(florist)
    
    florist_items = [
        {"name": "Mixed Bouquet - Small", "description": "Beautiful mix of seasonal flowers", "price": 150.00, "category": "Bouquets", "image": "https://images.unsplash.com/photo-1487530811176-3780de880c2d"},
        {"name": "Mixed Bouquet - Large", "description": "Grand arrangement of seasonal flowers", "price": 350.00, "category": "Bouquets", "image": "https://images.unsplash.com/photo-1487530811176-3780de880c2d"},
        {"name": "Sunflower Bouquet", "description": "Bright sunflower arrangement", "price": 200.00, "category": "Bouquets", "image": "https://images.unsplash.com/photo-1596438459194-f275f413d6ff"},
        {"name": "Lily Arrangement", "description": "Elegant lily arrangement in vase", "price": 280.00, "category": "Arrangements", "image": "https://images.unsplash.com/photo-1490750967868-88aa4f44baee"},
        {"name": "Romantic Rose Box", "description": "Luxury rose box arrangement", "price": 450.00, "category": "Arrangements", "image": "https://images.unsplash.com/photo-1455659817273-f96807779a8a"},
        {"name": "12 Red Roses", "description": "Classic dozen red roses wrapped", "price": 300.00, "category": "Roses", "image": "https://images.unsplash.com/photo-1455659817273-f96807779a8a"},
        {"name": "24 Red Roses", "description": "Two dozen premium red roses", "price": 550.00, "category": "Roses", "image": "https://images.unsplash.com/photo-1455659817273-f96807779a8a"},
        {"name": "50 Red Roses", "description": "Grand fifty red roses bouquet", "price": 800.00, "category": "Roses", "image": "https://images.unsplash.com/photo-1455659817273-f96807779a8a"},
        {"name": "Chocolate Box", "description": "Premium chocolate box add-on", "price": 120.00, "category": "Add-ons", "image": "https://images.unsplash.com/photo-1549007994-cb92caebd54b"},
        {"name": "Greeting Card", "description": "Personalised greeting card", "price": 25.00, "category": "Add-ons", "image": "https://images.unsplash.com/photo-1549007994-cb92caebd54b"},
        {"name": "Teddy Bear", "description": "Cute plush teddy bear", "price": 150.00, "category": "Add-ons", "image": "https://images.unsplash.com/photo-1549007994-cb92caebd54b"},
    ]
    
    for item in florist_items:
        await db.menu_items.insert_one({
            "item_id": f"item_{uuid.uuid4().hex[:12]}",
            "restaurant_id": florist_id,
            "available": True,
            "dietary_tags": [],
            **item,
        })
    print(f"Seeded No Limit Flowers: {len(florist_items)} items")

    # ==================== PARCEL DELIVERY SERVICE ====================
    parcel_id = f"rest_{uuid.uuid4().hex[:12]}"
    parcel = {
        "restaurant_id": parcel_id,
        "name": "No Limit Parcels",
        "description": "Fast door-to-door parcel pickup and delivery. Same-day delivery available. Price based on distance.",
        "image": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088",
        "cuisine_type": "Parcel Delivery",
        "rating": 4.5,
        "delivery_time": "Same day",
        "price_range": "R50-R250",
        "location": {"lat": -25.8744, "lng": 29.2339, "address": "Witbank, Emalahleni"},
        "featured": False,
        "active": True,
        "service_type": "parcel",
        "menu_categories": ["Standard Delivery", "Express Delivery", "Packaging"],
        "available_hours": {"weekdays": "08:00 - 18:00", "weekends": "09:00 - 14:00", "is_open": True},
    }
    await db.restaurants.insert_one(parcel)
    
    parcel_items = [
        {"name": "Standard Delivery (0-5km)", "description": "Same-day delivery within 5km radius", "price": 50.00, "category": "Standard Delivery", "image": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088"},
        {"name": "Standard Delivery (5-15km)", "description": "Same-day delivery 5-15km radius", "price": 80.00, "category": "Standard Delivery", "image": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088"},
        {"name": "Standard Delivery (15-30km)", "description": "Same-day delivery 15-30km radius", "price": 120.00, "category": "Standard Delivery", "image": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088"},
        {"name": "Standard Delivery (30-50km)", "description": "Next-day delivery 30-50km", "price": 180.00, "category": "Standard Delivery", "image": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088"},
        {"name": "Express Delivery (0-5km)", "description": "1-hour express delivery within 5km", "price": 80.00, "category": "Express Delivery", "image": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088"},
        {"name": "Express Delivery (5-15km)", "description": "2-hour express delivery 5-15km", "price": 120.00, "category": "Express Delivery", "image": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088"},
        {"name": "Express Delivery (15-30km)", "description": "3-hour express delivery 15-30km", "price": 200.00, "category": "Express Delivery", "image": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088"},
        {"name": "Small Box", "description": "Packaging box for small items", "price": 15.00, "category": "Packaging", "image": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088"},
        {"name": "Medium Box", "description": "Packaging box for medium items", "price": 25.00, "category": "Packaging", "image": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088"},
        {"name": "Bubble Wrap", "description": "Protective bubble wrap for fragile items", "price": 10.00, "category": "Packaging", "image": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088"},
    ]
    
    for item in parcel_items:
        await db.menu_items.insert_one({
            "item_id": f"item_{uuid.uuid4().hex[:12]}",
            "restaurant_id": parcel_id,
            "available": True,
            "dietary_tags": [],
            **item,
        })
    print(f"Seeded No Limit Parcels: {len(parcel_items)} items")

    total_restaurants = await db.restaurants.count_documents({})
    total_items = await db.menu_items.count_documents({})
    total_services = await db.services.count_documents({})
    print(f"\nTotal: {total_restaurants} providers, {total_items} items, {total_services} services")

asyncio.run(seed())
