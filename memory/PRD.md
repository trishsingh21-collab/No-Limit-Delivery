# No Limit Delivery - Product Requirements Document

## Overview
Premium food delivery mobile app with AI-powered recommendations, real-time order tracking, and loyalty rewards.

## Color Palette
- **Primary**: Sage Green (#87A96B / #2E8B57)
- **Secondary**: Black (#000000)
- **Background**: White (#FFFFFF)
- **Accents**: Pale Sage (#D4E4C7), Light Gray (#F5F5F5)

## Core Features

### 1. Authentication
- **JWT Email/Password Auth**: Signup + Login with bcrypt hashing
- **Google OAuth**: Emergent-managed Google Social Login
- **Session Management**: 7-day session tokens stored in cookies + AsyncStorage

### 2. Home Screen
- Personalized greeting (time-based)
- AI Quick Actions (Randomizer, Mood-based suggestions)
- Category browsing (Pizza, Burgers, Sushi, Healthy, Desserts, Chinese)
- Featured restaurants carousel
- All restaurants list with ratings, delivery time, price range

### 3. Search & Discovery
- Text search with restaurant/cuisine matching
- Cuisine filters (Italian, American, Japanese, etc.)
- AI "What should I eat?" randomizer
- Mood-based food suggestions (Comfort, Healthy, Quick, Indulgent)

### 4. Restaurant Detail
- Hero image with floating back/heart/share buttons
- Restaurant info card (name, description, rating, delivery time, price)
- **Available hours** display (weekdays/weekends + open/closed status)
- Menu/Reviews tab navigation
- Menu items grouped by category with:
  - Name, description, price, calorie badge
  - Thumbnail image
  - Green "+" add to cart button
- Floating cart button showing total

### 5. Cart
- Item list with images, prices, quantity controls (+/-)
- Remove items
- Clear cart
- Order summary (subtotal, delivery fee, tax, total)
- "Proceed to Checkout" button

### 6. Checkout
- Delivery address input (street, city, ZIP, instructions)
- Payment method selection
- Order summary
- "Place Order" button → creates order → navigates to tracking

### 7. Order Tracking (Real-time)
- Socket.IO-based real-time status updates
- Visual progress timeline (6 stages):
  - Order Placed → Confirmed → Preparing → Ready → On the Way → Delivered
- Estimated delivery time
- Order details and delivery address
- "Order Again" button when delivered

### 8. AI Features (OpenAI GPT-5.2 via Emergent LLM Key)
- Personalized recommendations based on order history
- "What should I eat?" randomizer
- Mood-based food suggestions

### 9. Loyalty/Rewards
- Points earned: 1 point per dollar spent
- Points displayed on profile
- (Future: Tiers, redemption options)

### 10. Profile Dashboard
- User info (name, email, phone)
- Stats (orders, points, addresses)
- Menu items: Delivery Addresses, Payment Methods, Rewards, Reviews, Settings, Help
- Logout functionality

## Tech Stack
- **Frontend**: Expo (React Native), expo-router, Zustand, Socket.io-client
- **Backend**: FastAPI, python-socketio, Motor (MongoDB)
- **AI**: OpenAI GPT-5.2 via Emergent LLM Key
- **Payments**: Stripe (mock mode, ready for real keys)
- **Database**: MongoDB (15 pre-seeded restaurants)
- **Auth**: JWT + Google OAuth (Emergent-managed)

## Database Collections
- `users` - User profiles with loyalty points
- `restaurants` - 15 seeded restaurants
- `menu_items` - Menu items per restaurant
- `orders` - User orders with status tracking
- `reviews` - User reviews
- `user_sessions` - Auth sessions
- `payment_transactions` - Stripe payment records

## Test Credentials
- Email: test@demo.com / Password: test123
- Stripe test card: 4242 4242 4242 4242
