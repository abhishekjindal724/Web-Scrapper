import mysql.connector
from config.settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establishes a connection to the MySQL database."""
        try:
            # First connect without database to create it if it doesn't exist
            self.conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD
            )
            self.cursor = self.conn.cursor()
            
            # Create database if not exists
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            
            # Switch to the database
            self.conn.database = DB_NAME
            
            return True
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            return False

    def create_tables(self):
        """Creates the necessary tables if they don't exist."""
        if not self.conn:
            return

        query = """
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(512),
            price VARCHAR(50),
            availability VARCHAR(50),
            rating VARCHAR(50),
            sentiment_score FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        alerts_query = """
        CREATE TABLE IF NOT EXISTS alerts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_url TEXT,
            target_price DECIMAL(10, 2),
            email VARCHAR(255),
            is_notified BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        try:
            self.cursor.execute(query)
            self.cursor.execute(alerts_query)
            self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Error creating tables: {err}")

    def insert_product(self, data):
        """Inserts a scraped product into the database."""
        if not self.conn or not self.cursor:
            return

        # Check for duplicates (same name and price)
        check_query = "SELECT id FROM products WHERE name = %s AND price = %s LIMIT 1"
        try:
            self.cursor.execute(check_query, (data.get('name', 'Unknown'), data.get('price', 'N/A')))
            if self.cursor.fetchone():
                return
        except mysql.connector.Error as err:
            print(f"Error checking duplicates: {err}")

        query = "INSERT INTO products (name, price, availability, rating, sentiment_score) VALUES (%s, %s, %s, %s, %s)"
        values = (
            data.get('name', 'Unknown'),
            data.get('price', 'N/A'),
            data.get('availability', 'Unknown'),
            data.get('rating', 'N/A'),
            data.get('sentiment_score', 0.0)
        )
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Error inserting product: {err}")

    def add_alert(self, url, target_price, email):
        """Adds a new price alert to the database."""
        if not self.conn:
            return False
        query = "INSERT INTO alerts (product_url, target_price, email) VALUES (%s, %s, %s)"
        try:
            self.cursor.execute(query, (url, target_price, email))
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error adding alert: {err}")
            return False

    def get_pending_alerts(self):
        """Fetches all alerts that have not yet been notified."""
        if not self.conn:
            return []
        query = "SELECT id, product_url, target_price, email FROM alerts WHERE is_notified = FALSE"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error fetching alerts: {err}")
            return []

    def mark_alert_sent(self, alert_id):
        """Marks an alert as sent (notified)."""
        if not self.conn:
            return
        query = "UPDATE alerts SET is_notified = TRUE WHERE id = %s"
        try:
            self.cursor.execute(query, (alert_id,))
            self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Error updating alert: {err}")

    def close(self):
        """Closes the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
