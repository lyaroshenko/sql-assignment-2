import mysql.connector
import random
from datetime import datetime, timedelta

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySQL_Student123",
    database="ecommerce_db"
)
cursor = conn.cursor()

print("Inserting customers...")
for _ in range(100):
    values = []
    for _ in range(10000):
        name = f"Customer_{random.randint(1, 1000000)}"
        city = random.choice(['Kyiv', 'Lviv', 'Odesa', 'Dnipro', 'Kharkiv'])
        signup_date = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 2000))
        values.append((name, city, signup_date.date()))
    cursor.executemany(
        "INSERT INTO customers (name, city, signup_date) VALUES (%s, %s, %s)",
        values
    )
    conn.commit()

print("Inserting products...")
for _ in range(100):
    values = []
    for _ in range(10000):
        name = f"Product_{random.randint(1, 1000000)}"
        category = random.choice(['Electronics', 'Books', 'Clothing', 'Home'])
        price = round(random.uniform(5, 500), 2)
        values.append((name, category, price))
    cursor.executemany(
        "INSERT INTO products (name, category, price) VALUES (%s, %s, %s)",
        values
    )
    conn.commit()

print("Inserting orders...")
for _ in range(100):
    values = []
    for _ in range(10000):
        customer_id = random.randint(1, 1000000)
        product_id = random.randint(1, 1000000)
        order_date = datetime(2022, 1, 1) + timedelta(days=random.randint(0, 1000))
        total_amount = round(random.uniform(10, 1000), 2)
        values.append((customer_id, product_id, order_date.date(), total_amount))
    cursor.executemany(
        "INSERT INTO orders (customer_id, product_id, order_date, total_amount) VALUES (%s, %s, %s, %s)",
        values
    )
    conn.commit()

print("All data inserted successfully")
cursor.close()
conn.close()

