import sqlite3
import pandas as pd
from pathlib import Path

# Database path - adjust if your database is in a different location
DB_PATH = "retail_commerce.db"

def execute_query(query, description=""):
    """Execute a SQL query and display results"""
    try:
        conn = sqlite3.connect(DB_PATH)

        print(f"\n{'='*80}")
        if description:
            print(f"QUERY: {description}")
        print(f"{'='*80}")
        print(f"SQL:\n{query}")
        print(f"{'-'*80}")

        # Use pandas for nice formatting
        df = pd.read_sql_query(query, conn)

        if len(df) == 0:
            print("No results found.")
        else:
            print(f"\nResults ({len(df)} rows):")
            print(df.to_string(index=False))

        conn.close()
        return df

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return None

def main():
    """Run a series of test queries to explore the database"""

    print("\n" + "="*80)
    print("SQL QUERY BUDDY - Database Testing Suite")
    print("="*80)

    # Check if database exists
    if not Path(DB_PATH).exists():
        print(f"\n❌ Database file '{DB_PATH}' not found!")
        print("Make sure you've created the database first.")
        return

    # Query 1: Simple SELECT - See all customers
    execute_query(
        """
        SELECT * FROM customers
        """,
        "Query 1: View all customers"
    )

    # Query 2: Simple SELECT - See all products
    execute_query(
        """
        SELECT * FROM products
        ORDER BY category, price DESC
        """,
        "Query 2: View all products ordered by category and price"
    )

    # Query 3: Aggregation - Count by region
    execute_query(
        """
        SELECT
            region,
            COUNT(*) as customer_count
        FROM customers
        GROUP BY region
        ORDER BY customer_count DESC
        """,
        "Query 3: Customer count by region"
    )

    # Query 4: Simple JOIN - Orders with customer names
    execute_query(
        """
        SELECT
            o.order_id,
            c.name as customer_name,
            o.order_date,
            o.total_amount
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        ORDER BY o.order_date DESC
        """,
        "Query 4: Orders with customer names (JOIN)"
    )

    # Query 5: Aggregation with JOIN - Top customers by total spending
    execute_query(
        """
        SELECT
            c.name as customer_name,
            c.region,
            COUNT(o.order_id) as order_count,
            SUM(o.total_amount) as total_spent
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.name, c.region
        ORDER BY total_spent DESC
        """,
        "Query 5: Top customers by total spending"
    )

    # Query 6: Complex JOIN - What products were in each order
    execute_query(
        """
        SELECT
            o.order_id,
            c.name as customer_name,
            p.name as product_name,
            p.category,
            oi.quantity,
            oi.subtotal
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        ORDER BY o.order_id, p.name
        """,
        "Query 6: Detailed order breakdown with products (Multi-table JOIN)"
    )

    # Query 7: Aggregation - Revenue by product category
    execute_query(
        """
        SELECT
            p.category,
            COUNT(DISTINCT oi.order_id) as orders,
            SUM(oi.quantity) as units_sold,
            SUM(oi.subtotal) as total_revenue
        FROM products p
        JOIN order_items oi ON p.product_id = oi.product_id
        GROUP BY p.category
        ORDER BY total_revenue DESC
        """,
        "Query 7: Revenue by product category"
    )

    # Query 8: Filter with aggregation - Electronics revenue by customer
    execute_query(
        """
        SELECT
            c.name as customer_name,
            SUM(oi.subtotal) as electronics_spending
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        WHERE p.category = 'Electronics'
        GROUP BY c.customer_id, c.name
        ORDER BY electronics_spending DESC
        """,
        "Query 8: Electronics spending by customer"
    )

    # Query 9: Date-based filter - Orders in 2024
    execute_query(
        """
        SELECT
            strftime('%Y-%m', order_date) as month,
            COUNT(*) as order_count,
            SUM(total_amount) as monthly_revenue
        FROM orders
        WHERE order_date >= '2024-01-01'
        GROUP BY month
        ORDER BY month
        """,
        "Query 9: Monthly revenue for 2024"
    )

    # Query 10: Subquery - Customers who spent more than average
    execute_query(
        """
        SELECT
            c.name,
            SUM(o.total_amount) as total_spent
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.name
        HAVING SUM(o.total_amount) > (
            SELECT AVG(customer_total)
            FROM (
                SELECT SUM(total_amount) as customer_total
                FROM orders
                GROUP BY customer_id
            )
        )
        ORDER BY total_spent DESC
        """,
        "Query 10: Customers who spent above average (Subquery)"
    )

    print("\n" + "="*80)
    print("✅ Testing Complete!")
    print("="*80)
    print("\nKey Learnings:")
    print("1. Simple SELECTs help you see raw data")
    print("2. JOINs connect related tables (customers ↔ orders ↔ products)")
    print("3. GROUP BY with aggregations (SUM, COUNT) give insights")
    print("4. Complex queries can answer business questions")
    print("\nNext Step: These are the types of queries your AI agent will generate!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
