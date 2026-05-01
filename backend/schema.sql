-- No Limit Delivery - Supabase PostgreSQL Schema
-- Run this in Supabase SQL Editor (https://supabase.com/dashboard → SQL Editor)

-- Services table
CREATE TABLE IF NOT EXISTS services (
    id SERIAL PRIMARY KEY,
    service_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    icon TEXT,
    emoji TEXT,
    type TEXT NOT NULL,
    description TEXT,
    active BOOLEAN DEFAULT true
);

-- Restaurants/Providers table
CREATE TABLE IF NOT EXISTS restaurants (
    id SERIAL PRIMARY KEY,
    restaurant_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    image TEXT,
    cuisine_type TEXT,
    rating FLOAT DEFAULT 0,
    delivery_time TEXT,
    price_range TEXT,
    location JSONB DEFAULT '{}',
    featured BOOLEAN DEFAULT false,
    active BOOLEAN DEFAULT true,
    service_type TEXT NOT NULL,
    menu_categories JSONB DEFAULT '[]',
    available_hours JSONB DEFAULT '{}'
);

-- Menu Items table
CREATE TABLE IF NOT EXISTS menu_items (
    id SERIAL PRIMARY KEY,
    item_id TEXT UNIQUE NOT NULL,
    restaurant_id TEXT NOT NULL REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    price FLOAT NOT NULL,
    image TEXT,
    category TEXT,
    available BOOLEAN DEFAULT true,
    dietary_tags JSONB DEFAULT '[]'
);

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_id TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name TEXT,
    phone TEXT,
    addresses JSONB DEFAULT '[]',
    loyalty_points INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    order_id TEXT UNIQUE NOT NULL,
    user_id TEXT NOT NULL,
    restaurant_id TEXT,
    restaurant_name TEXT,
    items JSONB DEFAULT '[]',
    subtotal FLOAT DEFAULT 0,
    delivery_fee FLOAT DEFAULT 30,
    tax FLOAT DEFAULT 0,
    total FLOAT DEFAULT 0,
    delivery_address JSONB DEFAULT '{}',
    payment_method TEXT DEFAULT 'cash',
    order_notes TEXT DEFAULT '',
    allergies JSONB DEFAULT '[]',
    tip FLOAT DEFAULT 0,
    promo_code TEXT,
    status TEXT DEFAULT 'pending',
    payment_status TEXT DEFAULT 'unpaid',
    pf_payment_id TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    estimated_delivery TIMESTAMPTZ
);

-- Reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    review_id TEXT UNIQUE NOT NULL,
    user_id TEXT NOT NULL,
    restaurant_id TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Payment Transactions table
CREATE TABLE IF NOT EXISTS payment_transactions (
    id SERIAL PRIMARY KEY,
    transaction_id TEXT UNIQUE NOT NULL,
    session_id TEXT,
    user_id TEXT NOT NULL,
    amount FLOAT NOT NULL,
    currency TEXT DEFAULT 'ZAR',
    payment_status TEXT DEFAULT 'pending',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_restaurants_service_type ON restaurants(service_type);
CREATE INDEX IF NOT EXISTS idx_restaurants_featured ON restaurants(featured);
CREATE INDEX IF NOT EXISTS idx_menu_items_restaurant ON menu_items(restaurant_id);
CREATE INDEX IF NOT EXISTS idx_menu_items_category ON menu_items(category);
CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Disable RLS for backend service access (using service_role key)
ALTER TABLE services ENABLE ROW LEVEL SECURITY;
ALTER TABLE restaurants ENABLE ROW LEVEL SECURITY;
ALTER TABLE menu_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE payment_transactions ENABLE ROW LEVEL SECURITY;

-- Allow full access for service role
CREATE POLICY "Service role full access" ON services FOR ALL USING (true);
CREATE POLICY "Service role full access" ON restaurants FOR ALL USING (true);
CREATE POLICY "Service role full access" ON menu_items FOR ALL USING (true);
CREATE POLICY "Service role full access" ON users FOR ALL USING (true);
CREATE POLICY "Service role full access" ON orders FOR ALL USING (true);
CREATE POLICY "Service role full access" ON reviews FOR ALL USING (true);
CREATE POLICY "Service role full access" ON payment_transactions FOR ALL USING (true);
