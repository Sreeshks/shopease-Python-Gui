import json
import re
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Dict, List, Any

# Define the shops dictionary with initial data
shops = {
    "Yuvarani foot wears": {
        "Location": "G6G8+4XM, Palace Rd, Keerankulangara, Thrissur, Kerala 680001",
        "Products": {
            "Nike": {"stock": 10, "Price": 1000, "Sizes": [7, 8, 9, 10]},
            "New Balance": {"stock": 8, "Price": 2400, "Sizes": [6, 7, 8, 9, 10]},
            "Puma": {"stock": 9, "Price": 1499, "Sizes": [7, 8, 9]}
        }
    },
    "Kobbler": {
        "Location": "G6G6+9G3, Machingal Ln, Naikkanal, Thrissur, Kerala 680022",
        "Products": {
            "Adidas": {"stock": 8, "Price": 1500, "Sizes": [6, 7, 8, 9, 10]},
            "Sneaker": {"stock": 14, "Price": 3000, "Sizes": [7, 8, 9]},
            "Converse": {"stock": 20, "Price": 1500, "Sizes": [6, 7, 8, 9, 10]}
        }
    },
    "Woodland": {
        "Location": "Shop No. 25/479, Gokul Building, M.G. Road, Opposite Ramdas Theatre, Thrissur, Kerala 680001",
        "Products": {
            "Reebok": {"stock": 10, "Price": 2000, "Sizes": [6, 7, 8, 9, 10]},
            "Converse": {"stock": 16, "Price": 1800, "Sizes": [7, 8, 9]},
            "Skechers": {"stock": 14, "Price": 2500, "Sizes": [6, 7, 8, 9, 10]}
        }
    },
    "DOC & MARK": {
        "Location": "SBU03, Woodlands Avenue, Room No :25, 789, MG Road, Naikkanal, Thrissur, Kerala 680001",
        "Products": {
            "Reebok": {"stock": 12, "Price": 1900, "Sizes": [6, 7, 9, 10]},
            "Vans": {"stock": 12, "Price": 1800, "Sizes": [3, 7, 8, 9]},
            "Skechers": {"stock": 10, "Price": 2570, "Sizes": [4, 7, 8, 9, 10]}
        }
    },
    "Bongo": {
        "Location": "G6F6+QQH, Kodungallur - Shornur Rd, Naduvilal, Marar Road Area, Naikkanal, Thrissur, Kerala 680001",
        "Products": {
            "Converse": {"stock": 12, "Price": 2000, "Sizes": [6, 7, 8, 9, 10]},
            "Nike": {"stock": 10, "Price": 1800, "Sizes": [7, 8, 9]},
            "Adidas": {"stock": 12, "Price": 2500, "Sizes": [6, 7, 8, 9, 10]}
        }
    },
    "Flexfootwear": {
        "Location": "G6C7+WPQ, Swaraj Round, Thrissur, Kerala 680001",
        "Products": {
            "Puma": {"stock": 10, "Price": 2000, "Sizes": [6, 7, 8, 9, 10]},
            "Sneaker": {"stock": 8, "Price": 1800, "Sizes": [7, 8, 9]},
            "Skechers": {"stock": 12, "Price": 2500, "Sizes": [6, 7, 8, 9, 10]}
        }
    }
}

# File paths for credentials
USER_CREDENTIALS_FILE = "user_credentials.json"
ADMIN_CREDENTIALS_FILE = "admin_credentials.json"

# Initialize credentials
admin_credentials = {
    "username": "admin",
    "password": "admin123",
    "is_signed_up": False,
    "shop_name": "Old Shop"
}
user_credentials: Dict[str, str] = {}

class ShopEaseApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("ShopEase: Product Search & Management")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f2f5")

        # Load credentials
        self.load_credentials()

        # Style configuration
        self.style = ttk.Style()
        self.style.configure("TButton", padding=10, font=("Helvetica", 12), background="#4CAF50", foreground="white")
        self.style.configure("TLabel", font=("Helvetica", 12), background="#f0f2f5")
        self.style.configure("TEntry", font=("Helvetica", 12))
        self.style.configure("Header.TLabel", font=("Helvetica", 24, "bold"), background="#f0f2f5")
        self.style.configure("SubHeader.TLabel", font=("Helvetica", 16, "bold"), background="#f0f2f5")

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill="both", expand=True)

        # Create main menu
        self.create_main_menu()

    def load_credentials(self):
        """Load credentials from JSON files."""
        global admin_credentials, user_credentials
        try:
            with open(ADMIN_CREDENTIALS_FILE, "r") as file:
                admin_credentials = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.save_credentials(ADMIN_CREDENTIALS_FILE, admin_credentials)

        try:
            with open(USER_CREDENTIALS_FILE, "r") as file:
                user_credentials = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.save_credentials(USER_CREDENTIALS_FILE, user_credentials)

    def save_credentials(self, file_path: str, data: Dict):
        """Save credentials to a JSON file."""
        try:
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
        except IOError as e:
            messagebox.showerror("Error", f"Error saving credentials: {e}")

    def validate_username(self, username: str) -> bool:
        """Validate username format."""
        return bool(username and re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

    def validate_password(self, password: str) -> bool:
        """Validate password format."""
        return len(password) >= 6

    def clear_frame(self):
        """Clear the main frame."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def create_main_menu(self):
        """Create the main menu interface."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Welcome to ShopEase", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)

        buttons = [
            ("Shopkeeper", self.shopkeeper_menu),
            ("User", self.user_menu),
            ("Contact", self.contact_info),
            ("Send Mail to Developer", self.send_mail),
            ("Exit", self.root.quit)
        ]

        for i, (text, command) in enumerate(buttons, start=1):
            ttk.Button(self.main_frame, text=text, command=command).grid(row=i, column=0, columnspan=2, sticky="ew", pady=10)

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

    def shopkeeper_menu(self):
        """Create shopkeeper menu."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Shopkeeper Menu", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)

        ttk.Button(self.main_frame, text="Sign-up", command=self.admin_signup_window).grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)
        ttk.Button(self.main_frame, text="Login", command=self.admin_login_window).grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.create_main_menu).grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

    def user_menu(self):
        """Create user menu."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="User Menu", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)

        ttk.Button(self.main_frame, text="Sign-up", command=self.user_signup_window).grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)
        ttk.Button(self.main_frame, text="Login", command=self.user_login_window).grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.create_main_menu).grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

    def admin_signup_window(self):
        """Create admin signup window and proceed to admin panel on success."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Admin Sign-up", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)

        # Username
        ttk.Label(self.main_frame, text="Username (3-20 characters, alphanumeric):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        username_entry = ttk.Entry(self.main_frame)
        username_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        # Password
        ttk.Label(self.main_frame, text="Password (minimum 6 characters):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        password_entry = ttk.Entry(self.main_frame, show="*")
        password_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

        # Shop Name
        ttk.Label(self.main_frame, text="Shop Name:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        shop_name_entry = ttk.Entry(self.main_frame)
        shop_name_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=5)

        def submit():
            if admin_credentials["is_signed_up"]:
                messagebox.showerror("Error", "Admin is already signed up.")
                return

            username = username_entry.get().strip()
            password = password_entry.get().strip()
            shop_name = shop_name_entry.get().strip()

            if not self.validate_username(username):
                messagebox.showerror("Error", "Invalid username. Must be 3-20 characters, alphanumeric only.")
                return
            if not self.validate_password(password):
                messagebox.showerror("Error", "Invalid password. Must be at least 6 characters.")
                return
            if not shop_name:
                messagebox.showerror("Error", "Shop name cannot be empty.")
                return

            admin_credentials.update({
                "username": username,
                "password": password,
                "shop_name": shop_name,
                "is_signed_up": True
            })
            self.save_credentials(ADMIN_CREDENTIALS_FILE, admin_credentials)
            messagebox.showinfo("Success", "Sign-up successful! Proceeding to Admin Panel.")
            self.admin_panel()

        ttk.Button(self.main_frame, text="Submit", command=submit).grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.shopkeeper_menu).grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.main_frame.columnconfigure(1, weight=1)

    def admin_login_window(self):
        """Create admin login window."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Admin Login", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)

        # Username
        ttk.Label(self.main_frame, text="Username:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        username_entry = ttk.Entry(self.main_frame)
        username_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        # Password
        ttk.Label(self.main_frame, text="Password:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        password_entry = ttk.Entry(self.main_frame, show="*")
        password_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

        def submit():
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if (username == admin_credentials["username"] and 
                password == admin_credentials["password"] and 
                admin_credentials["is_signed_up"]):
                
                # Ask for shop name change once in a dialog
                change_shop = messagebox.askyesno("Change Shop Name", f"Current shop: {admin_credentials['shop_name']}\nWould you like to change the shop name?")
                if change_shop:
                    new_window = tk.Toplevel(self.root)
                    new_window.title("Change Shop Name")
                    new_window.geometry("400x200")
                    new_window.configure(bg="#f0f2f5")

                    ttk.Label(new_window, text="Enter new shop name:", style="SubHeader.TLabel").pack(pady=10)
                    new_shop_entry = ttk.Entry(new_window)
                    new_shop_entry.pack(pady=10, padx=20, fill="x")

                    def save_shop_name():
                        new_shop_name = new_shop_entry.get().strip()
                        if new_shop_name:
                            admin_credentials["shop_name"] = new_shop_name
                            self.save_credentials(ADMIN_CREDENTIALS_FILE, admin_credentials)
                            messagebox.showinfo("Success", "Shop name updated successfully!")
                            new_window.destroy()
                            self.admin_panel()
                        else:
                            messagebox.showerror("Error", "Shop name cannot be empty.")

                    ttk.Button(new_window, text="Save", command=save_shop_name).pack(pady=10)
                else:
                    self.admin_panel()
            else:
                messagebox.showerror("Error", "Invalid credentials or admin not signed up.")

        ttk.Button(self.main_frame, text="Login", command=submit).grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.shopkeeper_menu).grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.main_frame.columnconfigure(1, weight=1)

    def user_signup_window(self):
        """Create user signup window and proceed to user panel on success."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="User Sign-up", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)

        # Username
        ttk.Label(self.main_frame, text="Username (3-20 characters, alphanumeric):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        username_entry = ttk.Entry(self.main_frame)
        username_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        # Password
        ttk.Label(self.main_frame, text="Password (minimum 6 characters):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        password_entry = ttk.Entry(self.main_frame, show="*")
        password_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

        def submit():
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if not self.validate_username(username):
                messagebox.showerror("Error", "Invalid username. Must be 3-20 characters, alphanumeric only.")
                return
            if username in user_credentials:
                messagebox.showerror("Error", "Username already exists.")
                return
            if not self.validate_password(password):
                messagebox.showerror("Error", "Invalid password. Must be at least 6 characters.")
                return

            user_credentials[username] = password
            self.save_credentials(USER_CREDENTIALS_FILE, user_credentials)
            messagebox.showinfo("Success", "User sign-up successful! Proceeding to User Panel.")
            self.user_panel()

        ttk.Button(self.main_frame, text="Submit", command=submit).grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.user_menu).grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.main_frame.columnconfigure(1, weight=1)

    def user_login_window(self):
        """Create user login window."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="User Login", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)

        # Username
        ttk.Label(self.main_frame, text="Username:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        username_entry = ttk.Entry(self.main_frame)
        username_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        # Password
        ttk.Label(self.main_frame, text="Password:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        password_entry = ttk.Entry(self.main_frame, show="*")
        password_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

        def submit():
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if username in user_credentials and user_credentials[username] == password:
                messagebox.showinfo("Success", "User login successful!")
                self.user_panel()
            else:
                messagebox.showerror("Error", "Invalid username or password.")

        ttk.Button(self.main_frame, text="Login", command=submit).grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.user_menu).grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.main_frame.columnconfigure(1, weight=1)

    def admin_panel(self):
        """Create admin panel interface."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Admin Panel", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)

        buttons = [
            ("Add Products", self.add_products_window),
            ("Delete Product", self.delete_product_window),
            ("Update Product", self.update_product_window),
            ("Display Brands", self.display_brands),
            ("Shop Details", self.shop_details),
            ("Logout", self.shopkeeper_menu)
        ]

        for i, (text, command) in enumerate(buttons, start=1):
            ttk.Button(self.main_frame, text=text, command=command).grid(row=i, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

    def user_panel(self):
        """Create user panel interface."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="User Panel", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)

        buttons = [
            ("Search Product", self.search_product_window),
            ("Search by Price", self.search_by_price_window),
            ("Display Brands", self.display_brands),
            ("Shop Details", self.shop_details),
            ("Logout", self.user_menu)
        ]

        for i, (text, command) in enumerate(buttons, start=1):
            ttk.Button(self.main_frame, text=text, command=command).grid(row=i, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

    def add_products_window(self):
        """Create window for adding products using admin's shop name."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Add Products", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)

        # Display current shop name
        shop_name = admin_credentials["shop_name"]
        ttk.Label(self.main_frame, text=f"Shop: {shop_name}", style="SubHeader.TLabel").grid(row=1, column=0, columnspan=2, pady=10)

        # Product Details Frame
        product_frame = ttk.LabelFrame(self.main_frame, text="Product Details")
        product_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        ttk.Label(product_frame, text="Product Name:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        product_name_entry = ttk.Entry(product_frame)
        product_name_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

        ttk.Label(product_frame, text="Stock Quantity:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        stock_entry = ttk.Entry(product_frame)
        stock_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        ttk.Label(product_frame, text="Price:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        price_entry = ttk.Entry(product_frame)
        price_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

        ttk.Label(product_frame, text="Sizes (comma-separated):").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        sizes_entry = ttk.Entry(product_frame)
        sizes_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=5)

        def add_product():
            if shop_name not in shops:
                messagebox.showerror("Error", "Shop not found!")
                return

            product_name = product_name_entry.get().strip()
            if not product_name:
                messagebox.showerror("Error", "Product name cannot be empty.")
                return

            try:
                stock = int(stock_entry.get().strip())
                if stock < 0:
                    raise ValueError("Stock cannot be negative")
                
                price = float(price_entry.get().strip())
                if price <= 0:
                    raise ValueError("Price must be positive")

                sizes = sizes_entry.get().strip()
                sizes_list = [int(size.strip()) for size in sizes.split(",") if size.strip()]
                if not sizes_list:
                    raise ValueError("At least one size must be provided")

                shops[shop_name]["Products"][product_name] = {
                    "stock": stock,
                    "Price": price,
                    "Sizes": sizes_list
                }
                messagebox.showinfo("Success", f"Product {product_name} added successfully!")
                
                # Clear product entries for next product
                product_name_entry.delete(0, tk.END)
                stock_entry.delete(0, tk.END)
                price_entry.delete(0, tk.END)
                sizes_entry.delete(0, tk.END)

            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        ttk.Button(self.main_frame, text="Add Product", command=add_product).grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        ttk.Button(self.main_frame, text="Done", command=self.admin_panel).grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        product_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

    def delete_product_window(self):
        """Create window for deleting products."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Delete Product", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)

        # Display admin's shop name
        shop_name = admin_credentials["shop_name"]
        ttk.Label(self.main_frame, text=f"Shop: {shop_name}", style="SubHeader.TLabel").grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Label(self.main_frame, text="Product Name:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        product_name_entry = ttk.Entry(self.main_frame)
        product_name_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

        def delete():
            product_name = product_name_entry.get().strip()

            if shop_name not in shops:
                messagebox.showerror("Error", "Shop not found!")
                return
            if product_name not in shops[shop_name]["Products"]:
                messagebox.showerror("Error", "Product not found!")
                return

            del shops[shop_name]["Products"][product_name]
            messagebox.showinfo("Success", "Product deleted successfully!")
            self.admin_panel()

        ttk.Button(self.main_frame, text="Delete", command=delete).grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.admin_panel).grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.main_frame.columnconfigure(1, weight=1)

    def update_product_window(self):
        """Create window for updating products."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Update Product", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)

        # Display admin's shop name
        shop_name = admin_credentials["shop_name"]
        ttk.Label(self.main_frame, text=f"Shop: {shop_name}", style="SubHeader.TLabel").grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Label(self.main_frame, text="Product Name:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        product_name_entry = ttk.Entry(self.main_frame)
        product_name_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

        def check_product():
            product_name = product_name_entry.get().strip()

            if shop_name not in shops:
                messagebox.showerror("Error", "Shop not found!")
                return
            if product_name not in shops[shop_name]["Products"]:
                messagebox.showerror("Error", "Product not found!")
                return

            # Clear previous update fields if any
            for widget in self.main_frame.winfo_children()[3:-2]:
                widget.destroy()

            update_frame = ttk.LabelFrame(self.main_frame, text="Update Options")
            update_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

            ttk.Label(update_frame, text="New Price (leave blank to keep unchanged):").grid(row=0, column=0, sticky="w", padx=10, pady=5)
            price_entry = ttk.Entry(update_frame)
            price_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

            ttk.Label(update_frame, text="New Stock (leave blank to keep unchanged):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
            stock_entry = ttk.Entry(update_frame)
            stock_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

            ttk.Label(update_frame, text="New Sizes (comma-separated, leave blank to keep unchanged):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
            sizes_entry = ttk.Entry(update_frame)
            sizes_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

            def update():
                try:
                    if price_entry.get().strip():
                        price = float(price_entry.get().strip())
                        if price <= 0:
                            raise ValueError("Price must be positive")
                        shops[shop_name]["Products"][product_name]["Price"] = price

                    if stock_entry.get().strip():
                        stock = int(stock_entry.get().strip())
                        if stock < 0:
                            raise ValueError("Stock cannot be negative")
                        shops[shop_name]["Products"][product_name]["stock"] = stock

                    if sizes_entry.get().strip():
                        sizes = sizes_entry.get().strip()
                        sizes_list = [int(size.strip()) for size in sizes.split(",") if size.strip()]
                        if not sizes_list:
                            raise ValueError("At least one size must be provided")
                        shops[shop_name]["Products"][product_name]["Sizes"] = sizes_list

                    messagebox.showinfo("Success", "Product updated successfully!")
                    self.admin_panel()

                except ValueError as e:
                    messagebox.showerror("Error", f"Invalid input: {e}")

            ttk.Button(update_frame, text="Update", command=update).grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        ttk.Button(self.main_frame, text="Check Product", command=check_product).grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.admin_panel).grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.main_frame.columnconfigure(1, weight=1)

    def search_product_window(self):
        """Create window for searching products."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Search Product", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)

        ttk.Label(self.main_frame, text="Product Name:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        product_name_entry = ttk.Entry(self.main_frame)
        product_name_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        result_text = scrolledtext.ScrolledText(self.main_frame, height=15, font=("Helvetica", 10))
        result_text.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        def search():
            product_name = product_name_entry.get().strip()
            results = [
                {
                    "Shop": shop,
                    "Location": shop_data["Location"],
                    "stock": brand_data["stock"],
                    "Price": brand_data["Price"],
                    "Sizes": brand_data["Sizes"]
                }
                for shop, shop_data in shops.items()
                for brand, brand_data in shop_data["Products"].items()
                if product_name.lower() == brand.lower()
            ]

            result_text.delete(1.0, tk.END)
            if results:
                result_text.insert(tk.END, "Matching products found:\n\n")
                for result in results:
                    result_text.insert(tk.END, f"Shop: {result['Shop']}\n")
                    result_text.insert(tk.END, f"Location: {result['Location']}\n")
                    result_text.insert(tk.END, f"Stock: {result['stock']}\n")
                    result_text.insert(tk.END, f"Price: ₹{result['Price']}\n")
                    result_text.insert(tk.END, f"Sizes: {result['Sizes']}\n")
                    result_text.insert(tk.END, "-" * 50 + "\n\n")
            else:
                result_text.insert(tk.END, "No matching products found.")

        ttk.Button(self.main_frame, text="Search", command=search).grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.user_panel).grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=1)

    def search_by_price_window(self):
        """Create window for searching products by price."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Search by Price", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)

        ttk.Label(self.main_frame, text="Maximum Price:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        price_entry = ttk.Entry(self.main_frame)
        price_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        result_text = scrolledtext.ScrolledText(self.main_frame, height=15, font=("Helvetica", 10))
        result_text.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        def search():
            try:
                max_price = float(price_entry.get().strip())
                if max_price <= 0:
                    raise ValueError("Price must be positive")

                results = [
                    {
                        "Shop": {"Name": shop, "Location": shop_data["Location"]},
                        "Brand": brand,
                        "stock": brand_data["stock"],
                        "Price": brand_data["Price"],
                        "Sizes": brand_data["Sizes"]
                    }
                    for shop, shop_data in shops.items()
                    for brand in shop_data["Products"].items()
                    if brand_data["Price"] <= max_price
                ]

                result_text.delete(1.0, tk.END).pack()
                if results:
                    result_text.insert(tk.END, "Products within price range:\n\n")
                    for result in results:
                        result_text.insert(tk.END, f"Shop: {result['Shop']['Name']}\n")
                        result_text.insert(tk.END, f"Location: {result['Location']}\n")
                        result_text.insert(tk.END, f"Brand: {result['Brand']}\n")
                        result_text.insert(tk.END, f"stock: {result['Stock']}\n")
                        result_text.insert(tk.END, f"Price: ₹{result['Price']}\n")
                        result_text.insert(tk.END, f"Sizes: {result['Sizes']}\n")
                        result_text.insert(tk.END, "-" * 50 + "\n\n")
                    else:
                        result_text.insert(tk.END, "No products found within price range.")

            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        ttk.Button(self.main_frame, text="Search", command=search).grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.user_panel).grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=1)

    def display_brands(self):
        """Display all available brands."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Available Brands", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)

        brands = sorted({brand for shop_data in shops.values() for brand in shop_data["Products"]})
        result_text = scrolledtext.ScrolledText(self.main_frame, height=15, font=("Helvetica", 10))
        result_text.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        result_text.insert(tk.END, "Available Brands:\n\n")
        for brand in brands:
            result_text.insert(tk.END, f"• {brand}\n")

        ttk.Button(self.main_frame, text="Back", command=self.admin_panel if self.main_frame.winfo_children()[0].cget("text") == "Admin Panel" else self.user_panel).grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

    def shop_details(self):
        """Create window for shop details."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Shop Details", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)

        ttk.Label(self.main_frame, text="Shop Name:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        shop_name_entry = ttk.Entry(self.main_frame)
        shop_name_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        result_text = scrolledtext.ScrolledText(self.main_frame, height=15, font=("Helvetica", 10))
        result_text.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        def search():
            shop_name = shop_name_entry.get().strip()
            if shop_name in shops:
                shop_data = shops[shop_name]
                product_count = len(shop_data["Products"])
                product_names = ", ".join(shop_data["Products"].keys())

                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Shop: {shop_name}\n")
                result_text.insert(tk.END, f"Location: {shop_data['Location']}\n")
                result_text.insert(tk.END, f"Product Count: {product_count}\n")
                result_text.insert(tk.END, f"Products: {product_names}\n")
            else:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Shop '{shop_name}' not found.")

        ttk.Button(self.main_frame, text="Search", command=search).grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.admin_panel if self.main_frame.winfo_children()[0].cget("text") == "Admin Panel" else self.user_panel).grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=1)

    def contact_info(self):
        """Display contact information."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Contact Information", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)

        contact_text = scrolledtext.ScrolledText(self.main_frame, height=15, font=("Helvetica", 10))
        contact_text.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        contact_info = [
            "Website: https://en.wikipedia.org/wiki/Shoe",
            "Instagram: https://www.instagram.com/shope_ease",
            "Telegram: http://t.me/ShopEase",
            "Email: shopease@gmail.com",
            "Phone: +918129690147, +918157843684",
            "Developers: Edwin, Abhirami, Sreesh"
        ]

        for info in contact_info:
            contact_text.insert(tk.END, f"{info}\n")

        contact_text.config(state="disabled")
        ttk.Button(self.main_frame, text="Back", command=self.create_main_menu).grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

    def send_mail(self):
        """Create window for sending mail."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Contact Developer", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)

        ttk.Label(self.main_frame, text="Recipient's Email:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        recipient_entry = ttk.Entry(self.main_frame)
        recipient_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        ttk.Label(self.main_frame, text="Subject:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        subject_entry = ttk.Entry(self.main_frame)
        subject_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

        ttk.Label(self.main_frame, text="Message:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        message_text = scrolledtext.ScrolledText(self.main_frame, height=5, font=("Helvetica", 10))
        message_text.grid(row=3, column=1, sticky="nsew", padx=10, pady=5)

        def send():
            recipient = recipient_entry.get().strip()
            subject = subject_entry.get().strip()
            message = message_text.get(1.0, tk.END).strip()

            if not all([recipient, subject, message]):
                messagebox.showerror("Error", "All fields are required.")
                return

            # Simulate sending mail
            messagebox.showinfo("Success", "Mail sent successfully!")
            self.create_main_menu()

        ttk.Button(self.main_frame, text="Send", command=send).grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.create_main_menu).grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(3, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = ShopEaseApp(root)
    root.mainloop()