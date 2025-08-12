-- Performance indexes for analytics queries
-- Creates indexes on frequently queried columns

-- Orders table indexes
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_payment_status ON orders(payment_status);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(order_status);

-- Order items table indexes
CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product ON order_items(product_id);

-- Products table indexes
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_active ON products(is_active);

-- Customers table indexes
CREATE INDEX IF NOT EXISTS idx_customers_first_order ON customers(first_order_date);
CREATE INDEX IF NOT EXISTS idx_customers_last_order ON customers(last_order_date);
CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);

-- Inventory table indexes
CREATE INDEX IF NOT EXISTS idx_inventory_reorder ON inventory(on_hand_qty, reorder_point);

-- Composite indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_orders_date_status ON orders(order_date, payment_status);
CREATE INDEX IF NOT EXISTS idx_orders_customer_date ON orders(customer_id, order_date);
