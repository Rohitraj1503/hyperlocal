-- Enable PostGIS extension for spatial queries
CREATE EXTENSION IF NOT EXISTS postgis;

-- Users Table (Customers, Merchants, Riders)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role VARCHAR(50) NOT NULL CHECK (role IN ('customer', 'merchant', 'rider')),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    is_active BOOLEAN DEFAULT true, -- Riders can toggle this
    location GEOGRAPHY(Point, 4326), -- PostGIS Point: Longitude, Latitude
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Inventory Table (Merchant Products)
CREATE TABLE inventory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID REFERENCES users(id) ON DELETE CASCADE,
    category VARCHAR(100) NOT NULL,
    type VARCHAR(100),
    name VARCHAR(255) NOT NULL,
    quantity INTEGER DEFAULT 0,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Orders Table
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID REFERENCES users(id),
    merchant_id UUID REFERENCES users(id),
    rider_id UUID REFERENCES users(id),
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'assigned', 'picked_up', 'delivered')),
    total_amount DECIMAL(10, 2) NOT NULL,
    pickup_location GEOGRAPHY(Point, 4326),
    dropoff_location GEOGRAPHY(Point, 4326),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Order Items
CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    inventory_id UUID REFERENCES inventory(id),
    quantity INTEGER NOT NULL,
    price_at_time DECIMAL(10, 2) NOT NULL
);

-- Function: Find nearby merchants/riders within radius (meters)
CREATE OR REPLACE FUNCTION get_nearby_users(
    origin GEOGRAPHY(Point, 4326),
    search_radius_meters FLOAT,
    user_role VARCHAR
)
RETURNS TABLE (
    user_id UUID,
    name VARCHAR,
    distance_meters FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        id as user_id, 
        users.name, 
        ST_Distance(location, origin) as distance_meters
    FROM users
    WHERE role = user_role 
      AND is_active = true
      AND ST_DWithin(location, origin, search_radius_meters)
    ORDER BY distance_meters ASC;
END;
$$ LANGUAGE plpgsql;
