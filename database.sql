CREATE DATABASE IF NOT EXISTS delivery_service;
USE delivery_service;

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

INSERT INTO categories (name) VALUES ('Food'), ('Grocery'), ('Medical');

INSERT INTO products (name, category_id) VALUES 
('Pizza', 1), 
('Bread', 2), 
('Aspirin', 3); 