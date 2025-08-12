-- Database schema creation script
-- Creates all tables with proper constraints and relationships

-- Categories table
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    category_id INTEGER NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    unit_cost DECIMAL(10,2) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    first_order_date DATE,
    last_order_date DATE,
    signup_date DATE,
    customer_city VARCHAR(100),
    customer_state VARCHAR(50),
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    order_date TIMESTAMP NOT NULL,
    order_status VARCHAR(20) NOT NULL,
    payment_amount DECIMAL(10,2) NOT NULL CHECK (payment_amount >= 0),
    payment_status VARCHAR(20) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Order items table
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id VARCHAR(50) NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
    discount DECIMAL(10,2) DEFAULT 0 CHECK (discount >= 0),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Inventory table
CREATE TABLE IF NOT EXISTS inventory (
    product_id INTEGER PRIMARY KEY,
    on_hand_qty INTEGER NOT NULL DEFAULT 0,
    reorder_point INTEGER NOT NULL DEFAULT 0,
    reorder_qty INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
