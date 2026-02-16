import mysql.connector
from config.settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_SSL

class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.db_type = "mysql" # Default

    def connect(self):
        """Establishes a connection to the database (MySQL or SQLite fallback)."""
        try:
            # Try connecting to MySQL
            self.conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                **DB_SSL
            )
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            self.conn.database = DB_NAME
            self.db_type = "mysql"
            return True
        except (mysql.connector.Error, Exception):
            # Fallback to SQLite
            try:
                import sqlite3
                self.conn = sqlite3.connect('ecommerce.db')
                self.cursor = self.conn.cursor()
                self.db_type = "sqlite"
                return True
            except Exception as e:
                print(f"Database connection failed: {e}")
                return False

    def _execute(self, query, params=None):
        """Executes a query handling DB-specific placeholder syntax."""
        if not self.cursor:
            return None
        
        try:
            if self.db_type == "sqlite":
                # Convert MySQL %s placeholder to SQLite ?
                query = query.replace("%s", "?")
                # SQLite doesn't support AUTO_INCREMENT in CREATE TABLE nicely safely via replace,
                # but our CREATE queries use AUTO_INCREMENT which is MySQL specific.
                # SQLite uses INTEGER PRIMARY KEY for auto increment behavior.
                query = query.replace("AUTO_INCREMENT", "") 
                # Also TIMESTAMP DEFAULT CURRENT_TIMESTAMP is supported in SQLite but let's be safe.
                
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
                
            if self.db_type == "sqlite":
                # Enable foreign keys or strictness if needed, but for now simple commit
                self.conn.commit() 
            return True
        except Exception as e:
            # print(f"Query Error: {e}") 
            # Suppress query errors for cleaner output, or log safely
            return False

    def create_tables(self):
        """Creates the necessary tables if they don't exist."""
        if not self.conn:
            return

        # Common types suitable for both
        # SQLite: INTEGER PRIMARY KEY is auto-increment
        pk = "INT AUTO_INCREMENT PRIMARY KEY" if self.db_type == "mysql" else "INTEGER PRIMARY KEY"
        
        query = f"""
        CREATE TABLE IF NOT EXISTS products (
            id {pk},
            name VARCHAR(512),
            price VARCHAR(50),
            availability VARCHAR(50),
            rating VARCHAR(50),
            sentiment_score FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        alerts_query = f"""
        CREATE TABLE IF NOT EXISTS alerts (
            id {pk},
            product_url TEXT,
            target_price DECIMAL(10, 2),
            email VARCHAR(255),
            is_notified BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        # Note: SQLite uses 0/1 for booleans
        
        self._execute(query)
        self._execute(alerts_query)

    def insert_product(self, data):
        """Inserts a scraped product into the database."""
        if not self.conn:
            return

        # Check for duplicates
        check_query = "SELECT id FROM products WHERE name = %s AND price = %s LIMIT 1"
        self._execute(check_query, (data.get('name', 'Unknown'), data.get('price', 'N/A')))
        
        if self.cursor.fetchone():
            return

        query = "INSERT INTO products (name, price, availability, rating, sentiment_score) VALUES (%s, %s, %s, %s, %s)"
        values = (
            data.get('name', 'Unknown'),
            data.get('price', 'N/A'),
            data.get('availability', 'Unknown'),
            data.get('rating', 'N/A'),
            data.get('sentiment_score', 0.0)
        )
        if self._execute(query, values) and self.db_type == "mysql":
             self.conn.commit()

    def add_alert(self, url, target_price, email):
        """Adds a new price alert to the database."""
        query = "INSERT INTO alerts (product_url, target_price, email) VALUES (%s, %s, %s)"
        if self._execute(query, (url, target_price, email)):
            if self.db_type == "mysql": self.conn.commit()
            return True
        return False

    def get_pending_alerts(self):
        """Fetches all alerts that have not yet been notified."""
        # SQLite uses 0/1, MySQL uses 0/1 (often mapped to False/True keywords, but integer is safest)
        val = 0 # Universal False for both SQLite and MySQL (TINYITY(1))
        
        query = f"SELECT id, product_url, target_price, email FROM alerts WHERE is_notified = {val}"
        
        print(f"Executing Query: {query}")
        self._execute(query)
        result = self.cursor.fetchall()
        print(f"Found {len(result)} alerts.")
        return result

    def mark_alert_sent(self, alert_id):
        """Marks an alert as sent (notified)."""
        val = 1 # Universal True
        query = f"UPDATE alerts SET is_notified = {val} WHERE id = %s"
        if self._execute(query, (alert_id,)):
             if self.db_type == "mysql": self.conn.commit()

    def close(self):
        """Closes the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
