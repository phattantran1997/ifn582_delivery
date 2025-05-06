USE delivery_service;
CREATE DATABASE IF NOT EXISTS delivery_service
    DEFAULT CHARACTER SET = 'utf8mb4';USE delivery_service;

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

INSERT INTO categories (name) VALUES ('Food'), ('Grocery'), ('Medical');

INSERT INTO users (username, email) VALUES 
('John Doe', 'john@example.com'),
('Jane Smith', 'jane@example.com');

INSERT INTO products (name, price, category_id) VALUES 
('Pizza', 12.99, 1), 
('Bread', 3.99, 2), 
('Aspirin', 5.99, 3);