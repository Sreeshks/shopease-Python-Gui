import json
import logging
from typing import Dict, List
from .config import USER_CREDENTIALS_FILE, ADMIN_CREDENTIALS_FILE, SHOPS_FILE, LOG_FILE

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initial shop data
INITIAL_SHOPS = {
    "Yuvarani foot wears": {
        "Location": "G6G8+4XM, Palace Rd, Keerankulangara, Thrissur, Kerala 680001",
        "Products": {
            "Nike": {"stock": 10, "Price": 1000, "Sizes": [7, 8, 9, 10], "Category": "Sneakers"},
            "New Balance": {"stock": 8, "Price": 2400, "Sizes": [6, 7, 8, 9, 10], "Category": "Sneakers"},
            "Puma": {"stock": 9, "Price": 1499, "Sizes": [7, 8, 9], "Category": "Sneakers"}
        }
    },
    # ... (other shops as in original code)
}

class DataHandler:
    def __init__(self):
        self.shops = {}
        self.admin_credentials = {
            "username": "admin",
            "password": "admin123",
            "is_signed_up": False,
            "shop_name": "Old Shop"
        }
        self.user_credentials: Dict[str, Dict] = {}
        self.load_data()

    def load_data(self):
        """Load data from JSON files."""
        try:
            with open(SHOPS_FILE, "r") as file:
                self.shops = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.shops = INITIAL_SHOPS
            self.save_shops()
            logging.info("Initialized shops data")

        try:
            with open(ADMIN_CREDENTIALS_FILE, "r") as file:
                self.admin_credentials = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.save_admin_credentials()
            logging.info("Initialized admin credentials")

        try:
            with open(USER_CREDENTIALS_FILE, "r") as file:
                self.user_credentials = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.save_user_credentials()
            logging.info("Initialized user credentials")

    def save_shops(self):
        """Save shop data to JSON file."""
        try:
            with open(SHOPS_FILE, "w") as file:
                json.dump(self.shops, file, indent=4)
        except IOError as e:
            logging.error(f"Error saving shops: {e}")

    def save_admin_credentials(self):
        """Save admin credentials to JSON file."""
        try:
            with open(ADMIN_CREDENTIALS_FILE, "w") as file:
                json.dump(self.admin_credentials, file, indent=4)
        except IOError as e:
            logging.error(f"Error saving admin credentials: {e}")

    def save_user_credentials(self):
        """Save user credentials to JSON file."""
        try:
            with open(USER_CREDENTIALS_FILE, "w") as file:
                json.dump(self.user_credentials, file, indent=4)
        except IOError as e:
            logging.error(f"Error saving user credentials: {e}")

    def export_inventory(self, shop_name: str, filename: str):
        """Export shop inventory to CSV."""
        import csv
        if shop_name not in self.shops:
            return False
        try:
            with open(filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Product", "Stock", "Price", "Sizes", "Category"])
                for product, data in self.shops[shop_name]["Products"].items():
                    writer.writerow([
                        product,
                        data["stock"],
                        data["Price"],
                        ",".join(map(str, data["Sizes"])),
                        data.get("Category", "")
                    ])
            logging.info(f"Exported inventory for {shop_name} to {filename}")
            return True
        except IOError as e:
            logging.error(f"Error exporting inventory: {e}")
            return False