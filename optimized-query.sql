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
CREATE INDEX idx_order_date ON orders(order_date);
CREATE INDEX idx_category ON products(category);
CREATE INDEX idx_product_id ON orders(product_id);