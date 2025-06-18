import json
import re
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Dict, List, Any

# Define color scheme
COLORS = {
    "primary": "#2c3e50",
    "secondary": "#34495e",
    "accent": "#3498db",
    "background": "#ecf0f1",
    "text": "#2c3e50",
    "button_hover": "#2980b9",
    "success": "#27ae60",
    "error": "#e74c3c"
}

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
        self.root.geometry("1000x700")
        self.root.configure(bg=COLORS["background"])

        # Load credentials
        self.load_credentials()

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use clam theme as base
        
        # Configure styles
        self.style.configure("TButton",
            padding=10,
            font=("Helvetica", 12),
            background=COLORS["accent"],
            foreground="white"
        )
        self.style.map("TButton",
            background=[("active", COLORS["button_hover"])],
            foreground=[("active", "white")]
        )
        
        self.style.configure("TLabel",
            font=("Helvetica", 12),
            background=COLORS["background"],
            foreground=COLORS["text"]
        )
        
        self.style.configure("TEntry",
            font=("Helvetica", 12),
            fieldbackground="white",
            padding=5
        )
        
        self.style.configure("Title.TLabel",
            font=("Helvetica", 24, "bold"),
            background=COLORS["background"],
            foreground=COLORS["primary"]
        )
        
        self.style.configure("Subtitle.TLabel",
            font=("Helvetica", 16),
            background=COLORS["background"],
            foreground=COLORS["secondary"]
        )

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding=20, style="Main.TFrame")
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

    def create_button(self, parent, text, command, width=20):
        """Create a styled button with hover effect"""
        btn = ttk.Button(parent, text=text, command=command, width=width)
        btn.pack(fill="x", pady=10, padx=20)
        return btn

    def create_entry(self, parent, show=None):
        """Create a styled entry field with Enter key binding"""
        entry = ttk.Entry(parent, font=("Helvetica", 12), show=show)
        entry.pack(pady=5, padx=20, fill="x")
        return entry

    def create_main_menu(self):
        """Create the main menu interface."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Welcome to ShopEase", style="Title.TLabel").pack(pady=20)

        buttons = [
            ("Shopkeeper", self.shopkeeper_menu),
            ("User", self.user_menu),
            ("Contact", self.contact_info),
            ("Send Mail to Developer", self.send_mail),
            ("Exit", self.root.quit)
        ]

        for text, command in buttons:
            self.create_button(self.main_frame, text, command)

    def shopkeeper_menu(self):
        """Create shopkeeper menu."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Shopkeeper Menu", style="Subtitle.TLabel").pack(pady=20)

        self.create_button(self.main_frame, "Sign-up", self.admin_signup_window)
        self.create_button(self.main_frame, "Login", self.admin_login_window)
        self.create_button(self.main_frame, "Back", self.create_main_menu)

    def user_menu(self):
        """Create user menu."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="User Menu", style="Subtitle.TLabel").pack(pady=20)

        self.create_button(self.main_frame, "Sign-up", self.user_signup_window)
        self.create_button(self.main_frame, "Login", self.user_login_window)
        self.create_button(self.main_frame, "Back", self.create_main_menu)

    def admin_signup_window(self):
        """Create admin signup window."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Admin Sign-up", style="Subtitle.TLabel").pack(pady=20)

        # Username
        ttk.Label(self.main_frame, text="Username (3-20 characters, alphanumeric):", style="Subtitle.TLabel").pack(pady=5)
        username_entry = self.create_entry(self.main_frame)

        # Password
        ttk.Label(self.main_frame, text="Password (minimum 6 characters):", style="Subtitle.TLabel").pack(pady=5)
        password_entry = self.create_entry(self.main_frame, show="*")

        # Shop Name
        ttk.Label(self.main_frame, text="Shop Name:", style="Subtitle.TLabel").pack(pady=5)
        shop_name_entry = self.create_entry(self.main_frame)

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
            messagebox.showinfo("Success", "Sign-up successful!")
            # Redirect to admin panel after successful signup
            self.admin_panel()

        # Bind Enter key navigation
        def on_username_enter(event):
            password_entry.focus_set()

        def on_password_enter(event):
            shop_name_entry.focus_set()

        def on_shop_name_enter(event):
            submit()

        username_entry.bind('<Return>', on_username_enter)
        password_entry.bind('<Return>', on_password_enter)
        shop_name_entry.bind('<Return>', on_shop_name_enter)

        self.create_button(self.main_frame, "Submit", submit)
        self.create_button(self.main_frame, "Back", self.shopkeeper_menu)

    def admin_login_window(self):
        """Create admin login window."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Admin Login", style="Title.TLabel").pack(pady=20)

        ttk.Label(self.main_frame, text="Username:", style="Subtitle.TLabel").pack(pady=5)
        username_entry = self.create_entry(self.main_frame)

        ttk.Label(self.main_frame, text="Password:", style="Subtitle.TLabel").pack(pady=5)
        password_entry = self.create_entry(self.main_frame, show="*")

        def submit():
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if (username == admin_credentials["username"] and 
                password == admin_credentials["password"] and 
                admin_credentials["is_signed_up"]):
                
                # Shop name change option
                shop_name_label = ttk.Label(
                    self.main_frame,
                    text=f"Current shop: {admin_credentials['shop_name']}",
                    style="Subtitle.TLabel"
                )
                shop_name_label.pack(pady=5)
                
                def change_shop_name():
                    new_window = tk.Toplevel(self.root)
                    new_window.title("Change Shop Name")
                    new_window.geometry("400x200")
                    new_window.configure(bg=COLORS["background"])

                    ttk.Label(new_window, text="Enter new shop name:", style="Subtitle.TLabel").pack(pady=10)
                    new_shop_entry = self.create_entry(new_window)

                    def save_shop_name():
                        new_shop_name = new_shop_entry.get().strip()
                        if new_shop_name:
                            admin_credentials["shop_name"] = new_shop_name
                            self.save_credentials(ADMIN_CREDENTIALS_FILE, admin_credentials)
                            messagebox.showinfo("Success", "Shop name updated successfully!")
                            shop_name_label.config(text=f"Current shop: {new_shop_name}")
                            new_window.destroy()
                        else:
                            messagebox.showerror("Error", "Shop name cannot be empty.")

                    # Bind Enter key to save function
                    new_shop_entry.bind('<Return>', lambda e: save_shop_name())

                    self.create_button(new_window, "Save", save_shop_name)
                
                self.create_button(self.main_frame, "Change Shop Name", change_shop_name)
                self.create_button(self.main_frame, "Proceed to Admin Panel", self.admin_panel)
            else:
                messagebox.showerror("Error", "Invalid credentials or admin not signed up.")

        # Bind Enter key navigation
        def on_username_enter(event):
            password_entry.focus_set()

        def on_password_enter(event):
            submit()

        username_entry.bind('<Return>', on_username_enter)
        password_entry.bind('<Return>', on_password_enter)

        self.create_button(self.main_frame, "Login", submit)
        self.create_button(self.main_frame, "Back", self.shopkeeper_menu)

    def user_signup_window(self):
        """Create user signup window."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="User Sign-up", style="Subtitle.TLabel").pack(pady=20)

        # Username
        ttk.Label(self.main_frame, text="Username (3-20 characters, alphanumeric):", style="Subtitle.TLabel").pack(pady=5)
        username_entry = self.create_entry(self.main_frame)

        # Password
        ttk.Label(self.main_frame, text="Password (minimum 6 characters):", style="Subtitle.TLabel").pack(pady=5)
        password_entry = self.create_entry(self.main_frame, show="*")

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
            messagebox.showinfo("Success", "User sign-up successful!")
            self.user_menu()

        self.create_button(self.main_frame, "Submit", submit)
        self.create_button(self.main_frame, "Back", self.user_menu)

    def user_login_window(self):
        """Create user login window."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="User Login", style="Title.TLabel").pack(pady=20)

        ttk.Label(self.main_frame, text="Username:", style="Subtitle.TLabel").pack(pady=5)
        username_entry = self.create_entry(self.main_frame)

        ttk.Label(self.main_frame, text="Password:", style="Subtitle.TLabel").pack(pady=5)
        password_entry = self.create_entry(self.main_frame, show="*")

        def submit():
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if username in user_credentials and user_credentials[username] == password:
                messagebox.showinfo("Success", "User login successful!")
                self.user_panel()
            else:
                messagebox.showerror("Error", "Invalid username or password.")

        # Bind Enter key to submit function
        username_entry.bind('<Return>', lambda e: password_entry.focus())
        password_entry.bind('<Return>', lambda e: submit())

        self.create_button(self.main_frame, "Login", submit)
        self.create_button(self.main_frame, "Back", self.user_menu)

    def admin_panel(self):
        """Create admin panel interface."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Admin Panel", style="Subtitle.TLabel").pack(pady=20)

        buttons = [
            ("Add Products", self.add_products_window),
            ("Delete Product", self.delete_product_window),
            ("Update Product", self.update_product_window),
            ("Display Brands", self.display_brands),
            ("Shop Details", self.shop_details),
            ("Logout", self.shopkeeper_menu)
        ]

        for text, command in buttons:
            self.create_button(self.main_frame, text, command)

    def user_panel(self):
        """Create user panel interface."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="User Panel", style="Subtitle.TLabel").pack(pady=20)

        buttons = [
            ("Search Product", self.search_product_window),
            ("Search by Price", self.search_by_price_window),
            ("Display Brands", self.display_brands),
            ("Shop Details", self.shop_details),
            ("Logout", self.user_menu)
        ]

        for text, command in buttons:
            self.create_button(self.main_frame, text, command)

    def add_products_window(self):
        """Create window for adding products."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Add Products", style="Subtitle.TLabel").pack(pady=20)

        # Shop Name
        ttk.Label(self.main_frame, text="Shop Name:", style="Subtitle.TLabel").pack(pady=5)
        shop_name_entry = self.create_entry(self.main_frame)

        # Product Details Frame
        product_frame = ttk.LabelFrame(self.main_frame, text="Product Details")
        product_frame.pack(pady=10, fill="x")

        ttk.Label(product_frame, text="Product Name:", style="Subtitle.TLabel").pack(pady=5)
        product_name_entry = self.create_entry(product_frame)

        ttk.Label(product_frame, text="Stock Quantity:", style="Subtitle.TLabel").pack(pady=5)
        stock_entry = self.create_entry(product_frame)

        ttk.Label(product_frame, text="Price:", style="Subtitle.TLabel").pack(pady=5)
        price_entry = self.create_entry(product_frame)

        ttk.Label(product_frame, text="Sizes (comma-separated):", style="Subtitle.TLabel").pack(pady=5)
        sizes_entry = self.create_entry(product_frame)

        def add_product():
            shop_name = shop_name_entry.get().strip()
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

        self.create_button(self.main_frame, "Add Product", add_product)
        self.create_button(self.main_frame, "Done", self.admin_panel)

    def delete_product_window(self):
        """Create window for deleting products."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Delete Product", style="Subtitle.TLabel").pack(pady=20)

        ttk.Label(self.main_frame, text="Shop Name:", style="Subtitle.TLabel").pack(pady=5)
        shop_name_entry = self.create_entry(self.main_frame)

        ttk.Label(self.main_frame, text="Product Name:", style="Subtitle.TLabel").pack(pady=5)
        product_name_entry = self.create_entry(self.main_frame)

        def delete():
            shop_name = shop_name_entry.get().strip()
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

        self.create_button(self.main_frame, "Delete", delete)
        self.create_button(self.main_frame, "Back", self.admin_panel)

    def update_product_window(self):
        """Create window for updating products."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Update Product", style="Subtitle.TLabel").pack(pady=20)

        ttk.Label(self.main_frame, text="Shop Name:", style="Subtitle.TLabel").pack(pady=5)
        shop_name_entry = self.create_entry(self.main_frame)

        ttk.Label(self.main_frame, text="Product Name:", style="Subtitle.TLabel").pack(pady=5)
        product_name_entry = self.create_entry(self.main_frame)

        def check_product():
            shop_name = shop_name_entry.get().strip()
            product_name = product_name_entry.get().strip()

            if shop_name not in shops:
                messagebox.showerror("Error", "Shop not found!")
                return
            if product_name not in shops[shop_name]["Products"]:
                messagebox.showerror("Error", "Product not found!")
                return

            update_frame = ttk.LabelFrame(self.main_frame, text="Update Options")
            update_frame.pack(pady=10, fill="x")

            ttk.Label(update_frame, text="New Price:", style="Subtitle.TLabel").pack(pady=5)
            price_entry = self.create_entry(update_frame)

            ttk.Label(update_frame, text="New Stock:", style="Subtitle.TLabel").pack(pady=5)
            stock_entry = self.create_entry(update_frame)

            ttk.Label(update_frame, text="New Sizes (comma-separated):", style="Subtitle.TLabel").pack(pady=5)
            sizes_entry = self.create_entry(update_frame)

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

            self.create_button(update_frame, "Update", update)

        self.create_button(self.main_frame, "Check Product", check_product)
        self.create_button(self.main_frame, "Back", self.admin_panel)

    def get_search_suggestions(self, query: str) -> List[str]:
        """Get search suggestions based on partial matches."""
        query = query.lower()
        suggestions = set()
        
        # Get all unique product names
        for shop_data in shops.values():
            for product in shop_data["Products"].keys():
                # Check if query is a substring of the product name
                if query in product.lower():
                    suggestions.add(product)
                # Also check if product name contains any word from the query
                query_words = query.split()
                product_words = product.lower().split()
                if any(word in product_words for word in query_words):
                    suggestions.add(product)
        
        return sorted(list(suggestions))

    def create_suggestion_listbox(self, parent, entry_widget, callback):
        """Create a suggestion listbox that appears below the entry widget."""
        listbox = tk.Listbox(
            parent,
            height=5,
            font=("Helvetica", 10),
            bg="white",
            selectmode=tk.SINGLE,
            relief=tk.SOLID,
            borderwidth=1
        )
        
        def update_suggestions(*args):
            query = entry_widget.get().strip()
            suggestions = self.get_search_suggestions(query)
            
            listbox.delete(0, tk.END)
            if suggestions and query:
                for suggestion in suggestions:
                    listbox.insert(tk.END, suggestion)
                listbox.pack(pady=2, padx=20, fill="x")
            else:
                listbox.pack_forget()
        
        def on_select(event):
            if listbox.curselection():
                selected = listbox.get(listbox.curselection())
                entry_widget.delete(0, tk.END)
                entry_widget.insert(0, selected)
                listbox.pack_forget()
                callback()
        
        def on_escape(event):
            listbox.pack_forget()
        
        def on_up_down(event):
            if not listbox.winfo_ismapped():
                return
            
            if event.keysym == 'Up':
                if listbox.curselection():
                    current = listbox.curselection()[0]
                    if current > 0:
                        listbox.selection_clear(current)
                        listbox.selection_set(current - 1)
                        listbox.see(current - 1)
            elif event.keysym == 'Down':
                if listbox.curselection():
                    current = listbox.curselection()[0]
                    if current < listbox.size() - 1:
                        listbox.selection_clear(current)
                        listbox.selection_set(current + 1)
                        listbox.see(current + 1)
                elif listbox.size() > 0:
                    listbox.selection_set(0)
        
        # Bind events
        entry_widget.bind('<KeyRelease>', update_suggestions)
        listbox.bind('<<ListboxSelect>>', on_select)
        entry_widget.bind('<Escape>', on_escape)
        entry_widget.bind('<Up>', on_up_down)
        entry_widget.bind('<Down>', on_up_down)
        
        return listbox

    def search_product_window(self):
        """Create window for searching products."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Search Product", style="Title.TLabel").pack(pady=20)

        # Create a frame for the search bar and suggestions
        search_frame = ttk.Frame(self.main_frame)
        search_frame.pack(fill="x", padx=20, pady=5)

        ttk.Label(search_frame, text="Product Name:", style="Subtitle.TLabel").pack(anchor="w")
        product_name_entry = self.create_entry(search_frame)

        result_text = scrolledtext.ScrolledText(
            self.main_frame,
            height=15,
            font=("Helvetica", 10),
            wrap=tk.WORD,
            background="white"
        )
        result_text.pack(pady=10, fill="both", expand=True, padx=20)

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

        # Create suggestion listbox
        suggestion_listbox = self.create_suggestion_listbox(
            search_frame,
            product_name_entry,
            search
        )

        # Bind Enter key to search function and focus management
        def on_enter(event):
            search()
            result_text.focus_set()

        product_name_entry.bind('<Return>', on_enter)
        result_text.bind('<Return>', lambda e: product_name_entry.focus_set())

        self.create_button(self.main_frame, "Search", search)
        self.create_button(self.main_frame, "Back", self.user_panel)

    def search_by_price_window(self):
        """Create window for searching products by price."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Search by Price", style="Title.TLabel").pack(pady=20)

        ttk.Label(self.main_frame, text="Maximum Price:", style="Subtitle.TLabel").pack(pady=5)
        price_entry = self.create_entry(self.main_frame)

        result_text = scrolledtext.ScrolledText(
            self.main_frame,
            height=15,
            font=("Helvetica", 10),
            wrap=tk.WORD,
            background="white"
        )
        result_text.pack(pady=10, fill="both", expand=True, padx=20)

        def search():
            try:
                max_price = float(price_entry.get().strip())
                if max_price <= 0:
                    raise ValueError("Price must be positive")

                results = [
                    {
                        "Shop": shop,
                        "Location": shop_data["Location"],
                        "Brand": brand,
                        "stock": brand_data["stock"],
                        "Price": brand_data["Price"],
                        "Sizes": brand_data["Sizes"]
                    }
                    for shop, shop_data in shops.items()
                    for brand, brand_data in shop_data["Products"].items()
                    if brand_data["Price"] <= max_price
                ]

                result_text.delete(1.0, tk.END)
                if results:
                    result_text.insert(tk.END, "Products within price range:\n\n")
                    for result in results:
                        result_text.insert(tk.END, f"Shop: {result['Shop']}\n")
                        result_text.insert(tk.END, f"Location: {result['Location']}\n")
                        result_text.insert(tk.END, f"Brand: {result['Brand']}\n")
                        result_text.insert(tk.END, f"Stock: {result['stock']}\n")
                        result_text.insert(tk.END, f"Price: ₹{result['Price']}\n")
                        result_text.insert(tk.END, f"Sizes: {result['Sizes']}\n")
                        result_text.insert(tk.END, "-" * 50 + "\n\n")
                else:
                    result_text.insert(tk.END, "No products found within price range.")

            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        # Bind Enter key to search function and focus management
        def on_enter(event):
            search()
            result_text.focus_set()

        price_entry.bind('<Return>', on_enter)
        result_text.bind('<Return>', lambda e: price_entry.focus_set())

        self.create_button(self.main_frame, "Search", search)
        self.create_button(self.main_frame, "Back", self.user_panel)

    def display_brands(self):
        """Display all available brands."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Available Brands", style="Subtitle.TLabel").pack(pady=20)

        brands = sorted({brand for shop_data in shops.values() for brand in shop_data["Products"]})
        result_text = scrolledtext.ScrolledText(self.main_frame, height=15, font=("Helvetica", 10))
        result_text.pack(pady=10, fill="both", expand=True)

        result_text.insert(tk.END, "Available Brands:\n\n")
        for brand in brands:
            result_text.insert(tk.END, f"• {brand}\n")

        self.create_button(self.main_frame, "Back", self.admin_panel if self.main_frame.winfo_children()[0].cget("text") == "Admin Panel" else self.user_panel)

    def shop_details(self):
        """Create window for shop details."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Shop Details", style="Subtitle.TLabel").pack(pady=20)

        ttk.Label(self.main_frame, text="Shop Name:", style="Subtitle.TLabel").pack(pady=5)
        shop_name_entry = self.create_entry(self.main_frame)

        result_text = scrolledtext.ScrolledText(
            self.main_frame,
            height=15,
            font=("Helvetica", 10),
            wrap=tk.WORD,
            background="white"
        )
        result_text.pack(pady=10, fill="both", expand=True, padx=20)

        def get_shop_suggestions(query: str) -> List[str]:
            """Get shop name suggestions based on partial matches."""
            query = query.lower()
            return sorted([
                shop for shop in shops.keys()
                if query in shop.lower()
            ])

        def update_suggestions(*args):
            query = shop_name_entry.get().strip()
            suggestions = get_shop_suggestions(query)
            
            suggestion_listbox.delete(0, tk.END)
            if suggestions and query:
                for suggestion in suggestions:
                    suggestion_listbox.insert(tk.END, suggestion)
                suggestion_listbox.pack(pady=2, padx=20, fill="x")
            else:
                suggestion_listbox.pack_forget()

        def on_select(event):
            if suggestion_listbox.curselection():
                selected = suggestion_listbox.get(suggestion_listbox.curselection())
                shop_name_entry.delete(0, tk.END)
                shop_name_entry.insert(0, selected)
                suggestion_listbox.pack_forget()
                search()

        def on_escape(event):
            suggestion_listbox.pack_forget()

        # Create suggestion listbox
        suggestion_listbox = tk.Listbox(
            self.main_frame,
            height=5,
            font=("Helvetica", 10),
            bg="white",
            selectmode=tk.SINGLE
        )

        # Bind events
        shop_name_entry.bind('<KeyRelease>', update_suggestions)
        suggestion_listbox.bind('<<ListboxSelect>>', on_select)
        shop_name_entry.bind('<Escape>', on_escape)

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

        # Bind Enter key to search function
        shop_name_entry.bind('<Return>', lambda e: search())

        self.create_button(self.main_frame, "Search", search)
        self.create_button(self.main_frame, "Back", self.admin_panel if self.main_frame.winfo_children()[0].cget("text") == "Admin Panel" else self.user_panel)

    def contact_info(self):
        """Display contact information."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Contact Information", style="Subtitle.TLabel").pack(pady=20)

        contact_text = scrolledtext.ScrolledText(self.main_frame, height=15, font=("Helvetica", 10))
        contact_text.pack(pady=10, fill="both", expand=True)

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
        self.create_button(self.main_frame, "Back", self.create_main_menu)

    def send_mail(self):
        """Create window for sending mail."""
        self.clear_frame()

        ttk.Label(self.main_frame, text="Contact Developer", style="Subtitle.TLabel").pack(pady=20)

        ttk.Label(self.main_frame, text="Recipient's Email:", style="Subtitle.TLabel").pack(pady=5)
        recipient_entry = self.create_entry(self.main_frame)

        ttk.Label(self.main_frame, text="Subject:", style="Subtitle.TLabel").pack(pady=5)
        subject_entry = self.create_entry(self.main_frame)

        ttk.Label(self.main_frame, text="Message:", style="Subtitle.TLabel").pack(pady=5)
        message_text = scrolledtext.ScrolledText(self.main_frame, height=5, font=("Helvetica", 10))
        message_text.pack(pady=5)

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

        self.create_button(self.main_frame, "Send", send)
        self.create_button(self.main_frame, "Back", self.create_main_menu)

if __name__ == "__main__":
    root = tk.Tk()
    app = ShopEaseApp(root)
    root.mainloop()