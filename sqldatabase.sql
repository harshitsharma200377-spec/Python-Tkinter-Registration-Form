CREATE DATABASE registration_db;

USE registration_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(255),
    gender VARCHAR(20),
    country VARCHAR(100)
);