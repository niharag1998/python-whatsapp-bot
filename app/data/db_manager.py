import sqlite3
import logging
from datetime import datetime
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path="app/data/development.db"):
        """Initialize the database manager with the path to the SQLite database."""
        self.db_path = db_path
        self._ensure_db_directory()
        self._init_db()

    def _ensure_db_directory(self):
        """Ensure the database directory exists."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    def _init_db(self):
        """Initialize the database with required tables."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create trades table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS trades (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        person_name TEXT NOT NULL,
                        product_name TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        price REAL NOT NULL,
                        status TEXT DEFAULT 'pending',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                # Create messages table for tracking WhatsApp messages
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        wa_id TEXT NOT NULL,
                        message_type TEXT NOT NULL,
                        message_content TEXT,
                        direction TEXT NOT NULL,
                        status TEXT DEFAULT 'sent',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                conn.commit()
                logging.info("Database initialized successfully")
        except sqlite3.Error as e:
            logging.error(f"Database initialization error: {e}")
            raise

    def add_trade(self, person_name, product_name, quantity, price):
        """Add a new trade to the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO trades (person_name, product_name, quantity, price)
                    VALUES (?, ?, ?, ?)
                ''', (person_name, product_name, quantity, price))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            logging.error(f"Error adding trade: {e}")
            raise

    def update_trade_status(self, trade_id, status):
        """Update the status of a trade."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE trades 
                    SET status = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (status, trade_id))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            logging.error(f"Error updating trade status: {e}")
            raise

    def get_trade(self, trade_id):
        """Get a trade by ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM trades WHERE id = ?', (trade_id,))
                return cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"Error getting trade: {e}")
            raise

    def get_all_trades(self, status=None):
        """Get all trades, optionally filtered by status."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                if status:
                    cursor.execute('SELECT * FROM trades WHERE status = ? ORDER BY created_at DESC', (status,))
                else:
                    cursor.execute('SELECT * FROM trades ORDER BY created_at DESC')
                return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Error getting trades: {e}")
            raise

    def log_message(self, wa_id, message_type, message_content, direction):
        """Log a WhatsApp message."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO messages (wa_id, message_type, message_content, direction)
                    VALUES (?, ?, ?, ?)
                ''', (wa_id, message_type, message_content, direction))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            logging.error(f"Error logging message: {e}")
            raise

    def get_message_history(self, wa_id, limit=50):
        """Get message history for a specific WhatsApp ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM messages 
                    WHERE wa_id = ? 
                    ORDER BY created_at DESC 
                    LIMIT ?
                ''', (wa_id, limit))
                return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Error getting message history: {e}")
            raise

    def clear_development_data(self):
        """Clear all data from the database (for development purposes only)."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM trades')
                cursor.execute('DELETE FROM messages')
                conn.commit()
                logging.info("Development data cleared successfully")
        except sqlite3.Error as e:
            logging.error(f"Error clearing development data: {e}")
            raise 