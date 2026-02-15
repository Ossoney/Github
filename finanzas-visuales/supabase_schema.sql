-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- 1. Profiles (Users)
-- Extends Supabase Auth
CREATE TABLE profiles (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    updated_at TIMESTAMP WITH TIME ZONE,
    full_name TEXT,
    avatar_url TEXT
);
-- 2. Currencies (Reference table)
CREATE TABLE currencies (
    code TEXT PRIMARY KEY,
    -- "EUR", "USD"
    name TEXT NOT NULL,
    symbol TEXT NOT NULL
);
INSERT INTO currencies (code, name, symbol)
VALUES ('EUR', 'Euro', '€'),
    ('USD', 'US Dollar', '$'),
    ('GBP', 'British Pound', '£');
-- 3. Accounts (Wallets/Banks)
CREATE TABLE accounts (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    name TEXT NOT NULL,
    type TEXT CHECK (type IN ('cash', 'bank', 'credit', 'investment')) NOT NULL,
    currency_code TEXT REFERENCES currencies(code) DEFAULT 'EUR',
    balance DECIMAL(12, 2) DEFAULT 0.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
-- 4. Categories (Nested)
CREATE TABLE categories (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    name TEXT NOT NULL,
    icon TEXT,
    -- Lucide icon name or emoji
    type TEXT CHECK (type IN ('income', 'expense')) NOT NULL,
    parent_id UUID REFERENCES categories(id),
    -- Self-referencing for nesting
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
-- 5. Transactions
CREATE TABLE transactions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    account_id UUID REFERENCES accounts(id) NOT NULL,
    category_id UUID REFERENCES categories(id),
    amount DECIMAL(12, 2) NOT NULL,
    -- Negative for expense, positive for income
    currency_code TEXT REFERENCES currencies(code) NOT NULL,
    date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
-- SIMPLE ROW LEVEL SECURITY (RLS) POLICIES
-- Only allow users to see/edit their own data
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
-- Profiles
CREATE POLICY "Users can view own profile" ON profiles FOR
SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON profiles FOR
UPDATE USING (auth.uid() = id);
-- Accounts
CREATE POLICY "Users can view own accounts" ON accounts FOR
SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own accounts" ON accounts FOR
INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own accounts" ON accounts FOR
UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own accounts" ON accounts FOR DELETE USING (auth.uid() = user_id);
-- Categories
CREATE POLICY "Users can view own categories" ON categories FOR
SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own categories" ON categories FOR
INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own categories" ON categories FOR
UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own categories" ON categories FOR DELETE USING (auth.uid() = user_id);
-- Transactions
CREATE POLICY "Users can view own transactions" ON transactions FOR
SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own transactions" ON transactions FOR
INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own transactions" ON transactions FOR
UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own transactions" ON transactions FOR DELETE USING (auth.uid() = user_id);