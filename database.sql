CREATE DATABASE IF NOT EXISTS delivery_service
    DEFAULT CHARACTER SET = 'utf8mb4';

USE delivery_service;

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255) NOT NULL
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role_id INT DEFAULT 2,
    last_login_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    image VARCHAR(255),
    description VARCHAR(255),
    category_id INT,
    availability ENUM('in_stock', 'out_of_stock') DEFAULT 'in_stock',
    quantity INT DEFAULT 0,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);


CREATE TABLE permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255) NOT NULL
);

CREATE TABLE role_permissions (
    role_id INT,
    permission_id INT,
    FOREIGN KEY (role_id) REFERENCES roles(id),
    FOREIGN KEY (permission_id) REFERENCES permissions(id)
);

CREATE TABLE shipping_methods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255) NOT NULL,
    fee DECIMAL(10,2) NOT NULL
);

CREATE TABLE shipments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    shipping_method_id INT,
    recipient_name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (shipping_method_id) REFERENCES shipping_methods(id)
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    cart_id INT NOT NULL,
    shipment_id INT,
    status ENUM('pending', 'paid', 'delivered', 'cancelled', 'success') DEFAULT 'pending',
    total_amount DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (shipment_id) REFERENCES shipments(id)
);


CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    price DECIMAL(10,2) NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE carts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    status ENUM('active', 'abandoned') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE cart_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cart_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    price DECIMAL(10,2) NOT NULL DEFAULT 0,
    FOREIGN KEY (cart_id) REFERENCES carts(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

INSERT INTO roles (name, description) VALUES 
('admin', 'Admin role'),
('user', 'User role');

INSERT INTO permissions (name, description) VALUES ('manage_products', 'Manage products permissionsd1');s




INSERT INTO role_permissions (role_id, permission_id) VALUES 
(1, 1);

INSERT INTO categories (name) VALUES 
('Fruits & Vegetables'), 
('Meat & Seafood'), 
('Dairy Products'), 
('Eggs & Breakfast'), 
('Snacks & Sweets'), 
('Beverages'), 
('Personal Care'), 
('Household Supplies'), 
('Pet Supplies');

INSERT INTO users (username, email, password, role_id) VALUES 
('admin1', 'admin1@example.com', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 1),
('admin2', 'admin2@example.com', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 1),
('user1', 'user1@example.com', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 2),
('user2', 'user2@example.com', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 2),
('user3', 'user3@example.com', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 2),
('user4', 'user4@example.com', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 2);

INSERT INTO products (name, price, category_id, image, description, availability, quantity) VALUES 
('Bananas', 3.0, 1, '/images/products/banana.png', 'Fresh yellow bananas, approx.1kg', 'in_stock', 120), 
('Spinach', 2.5, 1, '/images/products/spinach.png', 'Organic spinach leaves, 250g', 'in_stock', 90), 
('Apples', 5.99, 1, '/images/products/apple.png', 'Fresh and juicy red apples,1kg.', 'in_stock', 150),
('Chicken Breast', 8.99, 2, '/images/products/chicken breast.png', 'Skinless chicken breast fillets, 1kg.', 'in_stock', 80), 
('Salmon', 12.99, 2, '/images/products/salmon.png', 'Premium quality fresh salmon fillet, 500g', 'in_stock', 60), 
('Whole Milk', 2.8, 3, '/images/products/milk.png', 'Fresh whole milk, approx.1l', 'in_stock', 110), 
('Cheddar Cheese', 4.5, 3, '/images/products/cheese.png', 'Block of cheddar cheese, 500g', 'in_stock', 95), 
('Eggs', 4.2, 4, '/images/products/eggs.png', 'Free-range brown eggs, pack of 12.', 'in_stock', 140),
('Oats', 3.0, 4, '/images/products/oats.png', 'Rolled oats, high in fiber, 500g .', 'in_stock', 130),
('Potato chips', 2.5, 5, '/images/products/chips.png', 'Salted potato chips, 150g pack', 'in_stock', 200),
('Milk Chocolate Bar', 2.0, 5, '/images/products/chocolatebar.png', 'Smooth milk chocolate bar, 100g', 'in_stock', 180), 
('Orange Juice', 3.0, 6, '/images/products/orangejuice.png', '100% orange juice, no added sugar, 1L', 'in_stock', 160), 
('Instant Coffee', 6.5, 6, '/images/products/coffee.png', 'Instant coffee powder, strong blend, 200g', 'in_stock', 75), 
('Shampoo', 5.5, 7, '/images/products/shampoo.png', 'Moisturizing shampoo for all hair types', 'in_stock', 100), 
('Toothpaste', 2.8, 7, '/images/products/toothpaste.png', 'Fluoride toothpaste for fresh breath', 'in_stock', 130), 
('Dishwashing Liquid', 3.2, 8, '/images/products/dishwash.png', 'Lemon-scented dishwashing liquid, 1L', 'in_stock', 85), 
('Garbage Bags', 4.0, 8, '/images/products/grabagebag.png', 'Durable large garbage bags', 'in_stock', 95), 
('Dog Food', 12.0, 9, '/images/products/dogfood.png', 'Dry dog food with chicken flavor, 2kg', 'in_stock', 70), 
('Cat Litter', 6.0, 9, '/images/products/catlitter.png', 'Clumping cat litter, odor control, 5kg', 'in_stock', 65);

INSERT INTO shipping_methods (name, description, fee) VALUES 
('Free Shipping', 'Free shipping method', 0),
('Standard Shipping', 'Standard shipping method', 5.99),
('Express Shipping', 'Express shipping method', 10.99),
('Bike Shipping', 'Bike shipping method', 2.99);

# create carts and cart_items
INSERT INTO carts (user_id, status) VALUES 
(1, 'active'),
(2, 'active'),
(3, 'active'),
(4, 'active');

INSERT INTO cart_items (cart_id, product_id, quantity, price) VALUES 
(1, 1, 2, 3.0),
(2, 4, 1, 8.99),
(3, 14, 1, 6.99),
(4, 17, 1, 4.00);

INSERT INTO shipments (shipping_method_id, recipient_name, address, phone) VALUES
(1, 'William', '123 Apple St, Brisbane', '0400000001'), 
(2, 'Harry', '456 Mango Rd, Brisbane', '0400000002'),  
(3, 'Jake', '789 Peach Ave, Brisbane', '0400000003'), 
(4, 'Mater', '321 Berry Blvd, Brisbane', '0400000004'); 

INSERT INTO orders (user_id, cart_id, shipment_id, status, total_amount) VALUES
(1, 1, 1, 'delivered', 2 * 3.00),
(2, 2, 2, 'delivered', 1 * 8.99),
(3, 3, 3, 'delivered', 1 * 6.99),
(4, 4, 4, 'delivered', 1 * 4.00);

INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(1, 1, 2, 3.0),
(2, 4, 1, 8.99),
(3, 14, 1, 6.99),
(4, 17, 1, 4.00);

-- Update trigger
DELIMITER //
CREATE TRIGGER trg_products_bu
BEFORE UPDATE ON products
FOR EACH ROW
BEGIN
  IF NEW.quantity > 0 THEN
    SET NEW.availability = 'in_stock';
  ELSE
    SET NEW.availability = 'out_of_stock';
  END IF;
END;//
DELIMITER ;

-- Insert trigger
DELIMITER //
CREATE TRIGGER trg_products_bi
BEFORE INSERT ON products
FOR EACH ROW
BEGIN
  IF NEW.quantity > 0 THEN
    SET NEW.availability = 'in_stock';
  ELSE
    SET NEW.availability = 'out_of_stock';
  END IF;
END;//
DELIMITER ;
