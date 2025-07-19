create database byte1;
USE byte1;

-- Create users table
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    review VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Insert users
INSERT INTO users(username, email, password_hash, review) 
VALUES
('ali', 'ali@example.com', 'hash1', 'very bad'),
('sara', 'sara@example.com', 'hash2', 'Reliable delivery.'),
('bilal', 'bilal@example.com', 'hash3', 'Great support.'),
('hayat', 'hayat@example.com', 'hash3', 'Affordable pricing.'),
('tania', 'tania@example.com', 'hash4', 'Quick responses.'),
('omar', 'omar@example.com', 'hash5', 'Very professional.'),
('ayesha', 'ayesha@example.com', 'hash6', 'Satisfactory.'),
('john', 'john@example.com', 'hash7', 'good product'),
('naina', 'naina@example.com', 'hash8', 'It is a good chair go for it'),
('zain', 'zain@example.com', 'hash9', 'good quality product');

-- Create vendor table
CREATE TABLE vendor (
    vendor_id INT PRIMARY KEY,
    account_creation_date DATE NOT NULL,
    rating DECIMAL(3, 2) DEFAULT 0.0 CHECK (rating BETWEEN 0.0 AND 5.0),
    email VARCHAR(100)
);

-- Insert vendors (linked to emails in users)
INSERT INTO vendor (vendor_id, account_creation_date, rating, email) 
VALUES
(1, '2023-01-01', 4.5, 'ali@example.com'),
(2, '2023-02-01', 4.6, 'sara@example.com'),
(3, '2023-02-10', 4.2, 'bilal@example.com'),
(4, '2023-03-01', 4.8, 'tania@example.com'),
(5, '2023-03-15', 3.9, 'omar@example.com');

-- Create reviews table
CREATE TABLE reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    vendor_id INT,
    rating DECIMAL(2, 1) CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (vendor_id) REFERENCES vendor(vendor_id)
);

-- Insert reviews (only using existing user_id and vendor_id)

-- Collective Anomaly (same rating, same vendor, 4 new users)
INSERT INTO reviews (user_id, vendor_id, rating, timestamp)
VALUES
(7, 2, 5.0, '2025-06-18 08:00:00'),
(8, 2, 5.0, '2025-06-18 08:01:00'),
(9, 2, 5.0, '2025-06-18 08:02:00'),
(10, 2, 5.0, '2025-06-18 08:03:00');

-- Point Anomaly (sharp rating drop in one hour for vendor 1)
INSERT INTO reviews (user_id, vendor_id, rating, timestamp)
VALUES
(1, 1, 4.5, '2025-06-17 10:00:00'),
(2, 1, 4.2, '2025-06-17 10:05:00'),
(3, 1, 4.6, '2025-06-17 10:10:00'),
(4, 1, 1.5, '2025-06-18 10:00:00'),
(5, 1, 1.0, '2025-06-18 10:01:00'),
(6, 1, 1.2, '2025-06-18 10:02:00');

-- Contextual Anomaly (before/after rating shift for vendor 3)
INSERT INTO reviews (user_id, vendor_id, rating, timestamp)
VALUES
(1, 3, 4.8, '2025-06-16 12:00:00'),
(2, 3, 4.6, '2025-06-16 12:10:00'),
(3, 3, 4.7, '2025-06-16 12:15:00'),
(4, 3, 2.0, '2025-06-18 09:00:00'),
(5, 3, 1.9, '2025-06-18 09:05:00'),
(6, 3, 2.1, '2025-06-18 09:10:00');



SELECT * FROM users;
SELECT * FROM vendor;
SELECT * FROM reviews;