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

INSERT INTO categories (name) VALUES ('Food'), ('Grocery'), ('Medical');

INSERT INTO roles (name, description) VALUES 
('admin', 'Admin role'),
('user', 'User role');

INSERT INTO permissions (name, description) VALUES ('manage_products', 'Manage products permissionsd1');s




INSERT INTO role_permissions (role_id, permission_id) VALUES 
(1, 1);

INSERT INTO users (username, email, password, role_id) VALUES 
('admin', 'admin@example.com', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 1),
('user1', 'user1@example.com', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 2);

INSERT INTO products (name, price, category_id, image, description) VALUES 
('Pizza', 12.99, 1, '/images/products/pizza.png', 'A delicious pizza with fresh ingredients and a crispy crust. Perfect for a quick and easy meal.'), 
('Bread', 3.99, 2, '/images/products/bread.png', 'A fresh bread with a soft texture and a delicious flavor. Perfect for a quick and easy meal.'), 
('Aspirin', 5.99, 3, '/images/products/aspirin.png', 'A pain reliever that helps reduce inflammation and swelling. Perfect for a quick and easy meal.');

INSERT INTO shipping_methods (name, description, fee) VALUES 
('Standard Shipping', 'Standard shipping method', 5.99),
('Express Shipping', 'Express shipping method', 10.99),
('Free Shipping', 'Free shipping method', 0),
('Bike Shipping', 'Bike shipping method', 2.99);

# create carts and cart_items
INSERT INTO carts (user_id, status) VALUES 
(1, 'active'),
(2, 'active');

INSERT INTO cart_items (cart_id, product_id, quantity, price) VALUES 
(1, 1, 2, 12.99),
(1, 2, 1, 3.99),
(2, 3, 3, 5.99);
