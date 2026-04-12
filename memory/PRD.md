# No Limit Delivery - Product Requirements Document (Complete)

## App Overview
**No Limit Delivery** - Premium food delivery mobile app with AI-powered recommendations, real-time order tracking, and loyalty rewards.

## Color Palette
- **Primary Sage**: #87A96B / #2E8B57
- **Black**: #000000
- **White**: #FFFFFF
- **Pale Sage**: #D4E4C7 / #E8F5E9
- **Accents**: #F5A623 (stars), #E74C3C (errors)

## Complete Screen Inventory (20+ screens)

### Authentication
1. **Splash Screen** (`/index`) - Logo + tagline, auto-redirect
2. **Onboarding** (`/onboarding`) - 3 swipeable slides
3. **Login** (`/auth/login`) - Email/password + Google OAuth
4. **Signup** (`/auth/signup`) - Name, email, phone, password
5. **Google Callback** (`/auth/google-callback`) - OAuth exchange

### Main Tabs
6. **Home** (`/(tabs)/home`) - Greeting, location, search, promo banner, categories (emoji), featured restaurants, all restaurants
7. **Search** (`/(tabs)/search`) - Text search, cuisine filters, AI Randomizer tab, Mood-based tab
8. **Orders** (`/(tabs)/orders`) - Order history with status badges
9. **Profile** (`/(tabs)/profile`) - Avatar, loyalty banner, stats, menu items

### Restaurant & Ordering
10. **Restaurant Detail** (`/restaurant/[id]`) - Hero image, info card, available hours, Menu/Reviews tabs, menu items with add to cart
11. **Cart** (`/cart`) - Items, quantity controls, summary, checkout button
12. **Checkout** (`/checkout`) - Delivery address, payment, order summary, place order
13. **Order Tracking** (`/order-tracking/[id]`) - Real-time Socket.IO, progress timeline, order details

### Profile Sub-screens
14. **Loyalty Rewards** (`/rewards`) - Tiers (Bronze/Silver/Gold/Platinum), points, redeemable rewards, how to earn
15. **Delivery Addresses** (`/addresses`) - Add/edit/delete/set default addresses
16. **Payment Methods** (`/payment-methods`) - Card management with set default
17. **Notifications** (`/notifications`) - Toggle settings for order updates, marketing, rewards
18. **My Reviews** (`/my-reviews`) - Review history with ratings, empty state with how-to guide
19. **Help & Support** (`/help`) - Contact options (email, phone, live chat), FAQ accordion, about section

## Tech Stack
- **Frontend**: Expo SDK 54, expo-router, Zustand, Socket.io-client, React Native
- **Backend**: FastAPI, python-socketio, Motor (MongoDB), bcrypt, emergentintegrations
- **AI**: OpenAI GPT-5.2 via Emergent LLM Key
- **Payments**: Stripe (mock mode, ready for real keys)
- **Database**: MongoDB (15 seeded restaurants with menus)
- **Auth**: JWT + Google OAuth (Emergent-managed)

## Test Credentials
- Email: test@demo.com / Password: test123
- Stripe test card: 4242 4242 4242 4242 (any expiry/CVC)
