# SQL Optimization Assignment
## Liliia Yaroshenko, AI28

## Overview
This project demonstrates SQL query optimization using an e-commerce schema with 3 tables and 1,000,000+ rows each. The goal is to compare a non-optimized query with an optimized version that gives identical results but runs faster.

---

## Schema
- `customers`: customer info
- `products`: product catalog
- `orders`: each order links a customer to a product

```sql
CREATE TABLE customers (
  customer_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100),
  city VARCHAR(100),
  signup_date DATE
);

CREATE TABLE products (
  product_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100),
  category VARCHAR(50),
  price DECIMAL(10,2)
);

CREATE TABLE orders (
  order_id INT PRIMARY KEY AUTO_INCREMENT,
  customer_id INT,
  product_id INT,
  order_date DATE,
  total_amount DECIMAL(10,2),
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

## Data Insertion

Synthetic data was inserted using a Python script with 100 batches of 10,000 rows per table.

## Non-Optimized Query

```sql
SELECT c.name, p.name, o.total_amount, o.order_date
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN products p ON o.product_id = p.product_id
WHERE YEAR(o.order_date) = 2023
  AND LOWER(p.category) = 'electronics'
ORDER BY o.order_date DESC
LIMIT 1000;
```
### Problems

YEAR() disables index on order_date
LOWER() disables index on category
Full table scans and slow sorting

## Optimized Query

```sql
WITH filtered_orders AS (
  SELECT order_id, customer_id, product_id, total_amount, order_date
  FROM orders USE INDEX (idx_order_date)
  WHERE order_date BETWEEN '2023-01-01' AND '2023-12-31'
),
filtered_products AS (
  SELECT product_id, name
  FROM products USE INDEX (idx_category)
  WHERE category = 'Electronics'
)
SELECT c.name, fp.name, fo.total_amount, fo.order_date
FROM filtered_orders fo
JOIN customers c ON c.customer_id = fo.customer_id
JOIN filtered_products fp ON fp.product_id = fo.product_id
ORDER BY fo.order_date DESC
LIMIT 1000;
```

### Improvements

- `CTEs isolate filtered subsets`
- `Indexes used for order_date and category`
- `Faster joins and sorting`

### Indexes Used

```sql
CREATE INDEX idx_order_date ON orders(order_date);
CREATE INDEX idx_category ON products(category);
CREATE INDEX idx_product_id ON orders(product_id);
```
## Files in Repo

- `schema.sql`: table creation
- `insert_data.py`: data generation
- `queries.sql`: both query versions
- `explain_output.txt`: execution plans
- `README.md`: documentation