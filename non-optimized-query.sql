SELECT c.name, p.name, o.total_amount, o.order_date
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN products p ON o.product_id = p.product_id
WHERE YEAR(o.order_date) = 2023
  AND LOWER(p.category) = 'electronics'
ORDER BY o.order_date DESC
LIMIT 1000;
