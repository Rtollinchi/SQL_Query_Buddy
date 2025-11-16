import sqlite3

DB_PATH = "retail_commerce.db"

def create_database():
    """Create the database with schema and sample data"""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Creating retail commerce database...")

    # Create Customers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        region TEXT,
        signup_date DATE
    )
    """)

    # Create Products Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT,
        price DECIMAL(10,2)
    )
    """)

    # Create Orders Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date DATE,
        total_amount DECIMAL(10,2),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
    """)

    # Create Order Items Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        item_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        subtotal DECIMAL(10,2),
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
    """)

    print("✅ Tables created successfully")

    # Insert Sample Customers
    customers = [
        (1, 'Alice Chen', 'alice.chen@example.com', 'California', '2024-02-01'),
        (2, 'John Patel', 'john.patel@example.com', 'New York', '2024-05-15'),
        (3, 'Maria Lopez', 'maria.lopez@example.com', 'Texas', '2023-11-30'),
        (4, 'David Johnson', 'david.johnson@example.com', 'Florida', '2024-07-22'),
        (5, 'Sofia Khan', 'sofia.khan@example.com', 'Illinois', '2024-04-10')
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO customers VALUES (?, ?, ?, ?, ?)",
        customers
    )
    print(f"✅ Inserted {len(customers)} customers")

    # Insert Sample Products
    products = [
        (1, 'Laptop Pro 15', 'Electronics', 1200.00),
        (2, 'Wireless Mouse', 'Accessories', 40.00),
        (3, 'Standing Desk', 'Furniture', 300.00),
        (4, 'Noise Cancelling Headphones', 'Electronics', 150.00),
        (5, 'Office Chair Deluxe', 'Furniture', 180.00)
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO products VALUES (?, ?, ?, ?)",
        products
    )
    print(f"✅ Inserted {len(products)} products")

    # Insert Sample Orders
    orders = [
    (101, 1, '2025-01-12', 1240.00),
    (102, 2, '2025-03-05', 340.00),
    (103, 3, '2025-02-20', 1600.00),
    (104, 1, '2025-10-02', 330.00),
    (105, 4, '2025-11-05', 480.00),
    (106, 5, '2025-11-10', 180.00)
]
    cursor.executemany(
        "INSERT OR IGNORE INTO orders VALUES (?, ?, ?, ?)",
        orders
    )
    print(f"✅ Inserted {len(orders)} orders")

    # Insert Sample Order Items
    order_items = [
        (1, 101, 1, 1, 1200.00),
        (2, 101, 2, 1, 40.00),
        (3, 102, 2, 2, 80.00),
        (4, 102, 4, 1, 150.00),
        (5, 103, 3, 5, 1500.00),
        (6, 103, 2, 2, 80.00),
        (7, 104, 5, 1, 180.00),
        (8, 104, 2, 3, 120.00),
        (9, 105, 4, 3, 450.00),
        (10, 106, 5, 1, 180.00)
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO order_items VALUES (?, ?, ?, ?, ?)",
        order_items
    )
    print(f"✅ Inserted {len(order_items)} order items")

    conn.commit()
    conn.close()

    print(f"\n🎉 Database '{DB_PATH}' created successfully!")
    print("\nDatabase Summary:")
    print("- 5 customers across 5 regions")
    print("- 5 products in 3 categories")
    print("- 6 orders")
    print("- 10 order items")
    print("\nReady for testing! Run: python test_queries.py")

if __name__ == "__main__":
    create_database()
