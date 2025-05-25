
-- Create database
CREATE DATABASE IF NOT EXISTS expense_tracker CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Use the database
USE expense_tracker;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Create expense categories table
CREATE TABLE IF NOT EXISTS expense_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Create expenses table
CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    description VARCHAR(255) NOT NULL,
    expense_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES expense_categories(id) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- Add indexes for performance
CREATE INDEX idx_expenses_user_id ON expenses(user_id);
CREATE INDEX idx_expenses_category_id ON expenses(category_id);
CREATE INDEX idx_expenses_expense_date ON expenses(expense_date);

-- Insert default expense categories
INSERT INTO expense_categories (name, description) VALUES
    ('Food', 'Expenses related to groceries and eating out'),
    ('Entertainment', 'Movies, games, and other entertainment activities'),
    ('Transportation', 'Public transport, fuel, car maintenance'),
    ('Housing', 'Rent, mortgage, utilities, maintenance'),
    ('Healthcare', 'Medical expenses, insurance, medications'),
    ('Education', 'Tuition fees, books, courses'),
    ('Shopping', 'Clothing, electronics, and other retail purchases'),
    ('Travel', 'Vacations and business trips'),
    ('Personal', 'Personal care and miscellaneous expenses'),
    ('Other', 'Expenses that do not fit in other categories');

-- Create a view for expense summaries by category
CREATE OR REPLACE VIEW expense_summary_by_category AS
SELECT 
    u.username,
    ec.name AS category,
    SUM(e.amount) AS total_amount,
    COUNT(e.id) AS transaction_count,
    MIN(e.expense_date) AS earliest_date,
    MAX(e.expense_date) AS latest_date
FROM expenses e
JOIN users u ON e.user_id = u.id
JOIN expense_categories ec ON e.category_id = ec.id
GROUP BY u.username, ec.name;

-- Create a view for monthly expense summaries
CREATE OR REPLACE VIEW monthly_expense_summary AS
SELECT 
    u.username,
    YEAR(e.expense_date) AS year,
    MONTH(e.expense_date) AS month,
    ec.name AS category,
    SUM(e.amount) AS total_amount
FROM expenses e
JOIN users u ON e.user_id = u.id
JOIN expense_categories ec ON e.category_id = ec.id
GROUP BY u.username, YEAR(e.expense_date), MONTH(e.expense_date), ec.name;