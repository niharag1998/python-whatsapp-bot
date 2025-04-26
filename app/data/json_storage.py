import json
import os
import logging
from pathlib import Path
from datetime import datetime

class JsonStorage:
    def __init__(self, data_file="app/data/development_data.json"):
        """Initialize the JSON storage with the path to the data file."""
        self.data_file = data_file
        self._ensure_data_directory()
        self.data = self._load_data()

    def _ensure_data_directory(self):
        """Ensure the data directory exists."""
        Path(self.data_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Create the file if it doesn't exist
        if not os.path.exists(self.data_file):
            self._save_data({"trades": [], "messages": []})

    def _load_data(self):
        """Load data from the JSON file."""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return default structure if file doesn't exist or is invalid
            return {"trades": [], "messages": []}

    def _save_data(self, data=None):
        """Save data to the JSON file."""
        if data is None:
            data = self.data
            
        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            logging.error(f"Error saving data: {e}")
            return False

    def add_trade(self, person_name, product_name, quantity, price):
        """Add a new trade to the storage."""
        trade = {
            "id": len(self.data["trades"]) + 1,
            "person_name": person_name,
            "product_name": product_name,
            "quantity": quantity,
            "price": price,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        self.data["trades"].append(trade)
        self._save_data()
        return trade["id"]

    def update_trade_status(self, trade_id, status):
        """Update the status of a trade."""
        for trade in self.data["trades"]:
            if trade["id"] == trade_id:
                trade["status"] = status
                trade["updated_at"] = datetime.now().isoformat()
                self._save_data()
                return True
        return False

    def get_trade(self, trade_id):
        """Get a trade by ID."""
        for trade in self.data["trades"]:
            if trade["id"] == trade_id:
                return trade
        return None

    def get_all_trades(self, status=None):
        """Get all trades, optionally filtered by status."""
        if status:
            return [trade for trade in self.data["trades"] if trade["status"] == status]
        return self.data["trades"]

    def log_message(self, wa_id, message_type, message_content, direction):
        """Log a WhatsApp message."""
        message = {
            "id": len(self.data["messages"]) + 1,
            "wa_id": wa_id,
            "message_type": message_type,
            "message_content": message_content,
            "direction": direction,
            "status": "sent",
            "created_at": datetime.now().isoformat()
        }
        
        self.data["messages"].append(message)
        self._save_data()
        return message["id"]

    def get_message_history(self, wa_id, limit=50):
        """Get message history for a specific WhatsApp ID."""
        messages = [msg for msg in self.data["messages"] if msg["wa_id"] == wa_id]
        return sorted(messages, key=lambda x: x["created_at"], reverse=True)[:limit]

    def clear_data(self):
        """Clear all data (for development purposes only)."""
        self.data = {"trades": [], "messages": []}
        self._save_data()
        logging.info("Development data cleared successfully")
        return True 