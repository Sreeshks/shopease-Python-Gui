import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Dict, List, Callable
from .config import THEMES, ICON_PATH
from .data import DataHandler
from .utils import validate_username, validate_password, show_tooltip
from email_handler import EmailHandler

class ShopEaseUI:
    def __init__(self, root: tk.Tk, data_handler: DataHandler):
        self.root = root
        self.data_handler = data_handler
        self.current_theme = "light"
        self.colors = THEMES[self.current_theme]
        self.current_button_index = 0
        self.buttons = []
        self.current_user = None

        self.root.title("ShopEase")
        self.root.geometry("1200x800")
        self.root.iconbitmap(ICON_PATH)
        self.root.configure(bg=self.colors["background"])

        self.email_handler = EmailHandler(self.root, self.create_main_menu)
        self.setup_styles()
        self.setup_menu()
        self.main_frame = ttk.Frame(self.root, padding=30, style="Frame.TFrame")
        self.main_frame.pack(fill="both", expand=True)
        self.show_splash()
        self.setup_system_tray()

    def setup_styles(self):
        """Configure UI styles."""
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.style.configure("TButton",
            padding=12,
            font=("Roboto", 12, "bold"),
            background=self.colors["primary"],
            foreground="white",
            borderwidth=0
        )
        self.style.map("TButton",
            background=[("active", self.colors["button_hover"])],
            foreground=[("active", "white")]
        )

        self.style.configure("TLabel",
            font=("Roboto", 12),
            background=self.colors["background"],
            foreground=self.colors["text"]
        )

        self.style.configure("TEntry",
            font=("Roboto", 12),
            fieldbackground=self.colors["input_bg"],
            padding=10,
            relief="flat",
            borderwidth=1
        )

        self.style.configure("Title.TLabel",
            font=("Roboto", 28, "bold"),
            background=self.colors["background"],
            foreground=self.colors["primary"]
        )

        self.style.configure("Subtitle.TLabel",
            font=("Roboto", 16, "bold"),
            background=self.colors["background"],
            foreground=self.colors["secondary"]
        )

        self.style.configure("Frame.TFrame",
            background=self.colors["background"],
            borderwidth=1,
            relief="flat"
        )

        self.style.configure("Card.TFrame",
            background=self.colors["input_bg"],
            borderwidth=1,
            relief="solid",
            bordercolor=self.colors["border"]
        )

    def update_theme(self, theme: str):
        """Update application theme."""
        self.current_theme = theme
        self.colors = THEMES[theme]
        self.setup_styles()
        self.refresh_ui()

    def refresh_ui(self):
        """Refresh UI to apply theme changes."""
        self.root.configure(bg=self.colors["background"])
        for widget in self.main_frame.winfo_children():
            widget.configure(style=widget.cget("style"))
        self.main_frame.configure(style="Frame.TFrame")

    def setup_menu(self):
        """Setup menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.create_main_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Toggle Theme", command=lambda: self.update_theme("dark" if self.current_theme == "light" else "light"))

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def setup_system_tray(self):
        """Setup system tray icon (simplified for Tkinter)."""
        # Note: System tray requires additional libraries like pystray for full functionality
        # This is a placeholder for basic minimize-to-tray
        def minimize_to_tray():
            self.root.withdraw()

        def restore_from_tray():
            self.root.deiconify()

        self.root.protocol("WM_DELETE_WINDOW", minimize_to_tray)
        # Add actual system tray icon with pystray in production

    def show_splash(self):
        """Show splash screen."""
        splash = tk.Toplevel(self.root)
        splash.overrideredirect(True)
        splash.geometry("600x400+400+200")
        # Placeholder for splash image
        tk.Label(splash, text="Welcome to ShopEase", font=("Roboto", 24)).pack(expand=True)
        splash.after(2000, lambda: [splash.destroy(), self.create_main_menu()])

    def show_about(self):
        """Show about dialog."""
        messagebox.showinfo("About", "ShopEase v1.0.0\nA product management system for footwear shops.\nDeveloped by Edwin, Abhirami, Sreesh")

    def clear_frame(self):
        """Clear the main frame."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.buttons = []
        self.current_button_index = 0

    def create_button(self, parent, text, command, width=None):
        btn = ttk.Button(parent, text=text, command=command, width=width, style="TButton")
        btn.pack(pady=8, padx=20, fill="x")
        self.buttons.append(btn)
        show_tooltip(btn, text)
        return btn

    def create_entry(self, parent, show=None):
        entry = ttk.Entry(parent, font=("Roboto", 12), show=show, style="TEntry")
        entry.pack(pady=8, padx=20, fill="x")
        return entry

    def setup_button_navigation(self):
        def on_arrow_key(event):
            if event.keysym == "Up":
                self.current_button_index = (self.current_button_index - 1) % len(self.buttons)
                self.buttons[self.current_button_index].focus_set()
            elif event.keysym == "Down":
                self.current_button_index = (self.current_button_index + 1) % len(self.buttons)
                self.buttons[self.current_button_index].focus_set()
            elif event.keysym == "Return":
                self.buttons[self.current_button_index].invoke()

        def on_tab(event):
            if event.state & 0x1:
                self.current_button_index = (self.current_button_index - 1) % len(self.buttons)
            else:
                self.current_button_index = (self.current_button_index + 1) % len(self.buttons)
            self.buttons[self.current_button_index].focus_set()
            return "break"

        for btn in self.buttons:
            btn.bind("<Up>", on_arrow_key)
            btn.bind("<Down>", on_arrow_key)
            btn.bind("<Return>", on_arrow_key)
            btn.bind("<Tab>", on_tab)
            btn.bind("<Shift-Tab>", on_tab)

    def create_main_menu(self):
        self.clear_frame()
        header_frame = ttk.Frame(self.main_frame, style="Frame.TFrame")
        header_frame.pack(fill="x", pady=(0, 20))
        ttk.Label(header_frame, text="ShopEase", style="Title.TLabel").pack(anchor="center")

        content_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        content_frame.pack(pady=20, padx=50, fill="both", expand=True)

        ttk.Label(content_frame, text="Welcome to ShopEase", style="Subtitle.TLabel").pack(pady=(20, 10))

        buttons = [
            ("Shopkeeper", self.shopkeeper_menu),
            ("User", self.user_menu),
            ("Contact", self.contact_info),
            ("Send Mail to Developer", self.email_handler.send_mail_window),
            ("Exit", self.root.quit)
        ]

        for text, command in buttons:
            self.create_button(content_frame, text, command)

        self.setup_button_navigation()
        if self.buttons:
            self.buttons[0].focus_set()

    def shopkeeper_menu(self):
        self.clear_frame()
        content_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        content_frame.pack(pady=20, padx=50, fill="both", expand=True)

        ttk.Label(content_frame, text="Shopkeeper Menu", style="Subtitle.TLabel").pack(pady=(20, 10))

        self.create_button(content_frame, "Sign-up", self.admin_signup_window)
        self.create_button(content_frame, "Login", self.admin_login_window)
        self.create_button(content_frame, "Back", self.create_main_menu)

    def user_menu(self):
        self.clear_frame()
        content_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        content_frame.pack(pady=20, padx=50, fill="both", expand=True)

        ttk.Label(content_frame, text="User Menu", style="Subtitle.TLabel").pack(pady=(20, 10))

        self.create_button(content_frame, "Sign-up", self.user_signup_window)
        self.create_button(content_frame, "Login", self.user_login_window)
        self.create_button(content_frame, "Back", self.create_main_menu)

    def admin_signup_window(self):
        self.clear_frame()
        content_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        content_frame.pack(pady=20, padx=50, fill="both", expand=True)

        ttk.Label(content_frame, text="Admin Sign-up", style="Subtitle.TLabel").pack(pady=(20, 10))

        ttk.Label(content_frame, text="Username (3-20 characters, alphanumeric):").pack(anchor="w", padx=20)
        username_entry = self.create_entry(content_frame)

        ttk.Label(content_frame, text="Password (minimum 6 characters):").pack(anchor="w", padx=20)
        password_entry = self.create_entry(content_frame, show="*")

        ttk.Label(content_frame, text="Shop Name:").pack(anchor="w", padx=20)
        shop_name_entry = self.create_entry(content_frame)

        def submit():
            if self.data_handler.admin_credentials["is_signed_up"]:
                messagebox.showerror("Error", "Admin is already signed up.")
                return

            username = username_entry.get().strip()
            password = password_entry.get().strip()
            shop_name = shop_name_entry.get().strip()

            if not validate_username(username):
                messagebox.showerror("Error", "Invalid username. Must be 3-20 characters, alphanumeric only.")
                return
            if not validate_password(password):
                messagebox.showerror("Error", "Invalid password. Must be at least 6 characters.")
                return
            if not shop_name:
                messagebox.showerror("Error", "Shop name cannot be empty.")
                return

            self.data_handler.admin_credentials.update({
                "username": username,
                "password": password,
                "shop_name": shop_name,
                "is_signed_up": True
            })
            self.data_handler.save_admin_credentials()
            messagebox.showinfo("Success", "Sign-up successful!")
            self.admin_panel()

        def on_username_enter(event):
            password_entry.focus_set()

        def on_password_enter(event):
            shop_name_entry.focus_set()

        def on_shop_name_enter(event):
            submit()

        username_entry.bind('<Return>', on_username_enter)
        password_entry.bind('<Return>', on_password_enter)
        shop_name_entry.bind('<Return>', on_shop_name_enter)

        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=20, fill="x")
        self.create_button(button_frame, "Submit", submit, width=15)
        self.create_button(button_frame, "Back", self.shopkeeper_menu, width=15)

    def admin_login_window(self):
        self.clear_frame()
        content_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        content_frame.pack(pady=20, padx=50, fill="both", expand=True)

        ttk.Label(content_frame, text="Admin Login", style="Subtitle.TLabel").pack(pady=(20, 10))

        ttk.Label(content_frame, text="Username:").pack(anchor="w", padx=20)
        username_entry = self.create_entry(content_frame)

        ttk.Label(content_frame, text="Password:").pack(anchor="w", padx=20)
        password_entry = self.create_entry(content_frame, show="*")

        def submit():
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if (username == self.data_handler.admin_credentials["username"] and 
                password == self.data_handler.admin_credentials["password"] and 
                self.data_handler.admin_credentials["is_signed_up"]):
                
                shop_name_label = ttk.Label(
                    content_frame,
                    text=f"Current shop: {self.data_handler.admin_credentials['shop_name']}",
                    style="TLabel"
                )
                shop_name_label.pack(pady=10)
                
                def change_shop_name():
                    new_window = tk.Toplevel(self.root)
                    new_window.title("Change Shop Name")
                    new_window.geometry("400x250")
                    new_window.configure(bg=self.colors["background"])

                    content = ttk.Frame(new_window, style="Card.TFrame")
                    content.pack(pady=20, padx=20, fill="both", expand=True)

                    ttk.Label(content, text="Enter new shop name:").pack(anchor="w", padx=10)
                    new_shop_entry = self.create_entry(content)

                    def save_shop_name():
                        new_shop_name = new_shop_entry.get().strip()
                        if new_shop_name:
                            self.data_handler.admin_credentials["shop_name"] = new_shop_name
                            self.data_handler.save_admin_credentials()
                            messagebox.showinfo("Success", "Shop name updated successfully!")
                            shop_name_label.config(text=f"Current shop: {new_shop_name}")
                            new_window.destroy()
                        else:
                            messagebox.showerror("Error", "Shop name cannot be empty.")

                    new_shop_entry.bind('<Return>', lambda e: save_shop_name())
                    self.create_button(content, "Save", save_shop_name)

                self.create_button(content_frame, "Change Shop Name", change_shop_name)
                self.create_button(content_frame, "Proceed to Admin Panel", self.admin_panel)
            else:
                messagebox.showerror("Error", "Invalid credentials or admin not signed up.")

        def on_username_enter(event):
            password_entry.focus_set()

        def on_password_enter(event):
            submit()

        username_entry.bind('<Return>', on_username_enter)
        password_entry.bind('<Return>', on_password_enter)

        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=20, fill="x")
        self.create_button(button_frame, "Login", submit, width=15)
        self.create_button(button_frame, "Back", self.shopkeeper_menu, width=15)

    def user_signup_window(self):
        self.clear_frame()
        content_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        content_frame.pack(pady=20, padx=50, fill="both", expand=True)

        ttk.Label(content_frame, text="User Sign-up", style="Subtitle.TLabel").pack(pady=(20, 10))

        ttk.Label(content_frame, text="Username (3-20 characters, alphanumeric):").pack(anchor="w", padx=20)
        username_entry = self.create_entry(content_frame)

        ttk.Label(content_frame, text="Password (minimum 6 characters):").pack(anchor="w", padx=20)
        password_entry = self.create_entry(content_frame, show="*")

        def submit():
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if not validate_username(username):
                messagebox.showerror("Error", "Invalid username. Must be 3-20 characters, alphanumeric only.")
                return
            if username in self.data_handler.user_credentials:
                messagebox.showerror("Error", "Username already exists.")
                return
            if not validate_password(password):
                messagebox.showerror("Error", "Invalid password. Must be at least 6 characters.")
                return

            self.data_handler.user_credentials[username] = {"password": password, "profile": {}}
            self.data_handler.save_user_credentials()
            messagebox.showinfo("Success", "User sign-up successful!")
            self.user_menu()

        def on_username_enter(event):
            password_entry.focus_set()

        def on_password_enter(event):
            submit()

        username_entry.bind('<Return>', on_username_enter)
        password_entry.bind('<Return>', on_password_enter)

        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=20, fill="x")
        self.create_button(button_frame, "Submit", submit, width=15)
        self.create_button(button_frame, "Back", self.user_menu, width=15)

    def user_login_window(self):
        self.clear_frame()
        content_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        content_frame.pack(pady=20, padx=50, fill="both", expand=True)

        ttk.Label(content_frame, text="User Login", style="Subtitle.TLabel").pack(pady=(20, 10))

        ttk.Label(content_frame, text="Username:").pack(anchor="w", padx=20)
        username_entry = self.create_entry(content_frame)

        ttk.Label(content_frame, text="Password:").pack(anchor="w", padx=20)
        password_entry = self.create_entry(content_frame, show="*")

        def submit():
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if (username in self.data_handler.user_credentials and 
                self.data_handler.user_credentials[username]["password"] == password):
                self.current_user = username
                messagebox.showinfo("Success", "User login successful!")
                self.user_panel()
            else:
                messagebox.showerror("Error", "Invalid username or password.")

        username_entry.bind('<Return>', lambda e: password_entry.focus())
        password_entry.bind('<Return>', lambda e: submit())

        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=20, fill="x")
        self.create_button(button_frame, "Login", submit, width=15)
        self.create_button(button_frame, "Back", self.user_menu, width=15)

    def admin_panel(self):
        self.clear_frame()
        content_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        content_frame.pack(pady=20, padx=50, fill="both", expand=True)

        ttk.Label(content_frame, text="Admin Panel", style="Subtitle.TLabel").pack(pady=(20, 10))

        buttons = [
            ("Add Products", self.add_products_window),
            ("Delete Product", self.delete_product_window),
            ("Update Product", self.update_product_window),
            ("Display Brands", self.display_brands),
            ("Shop Details", self.shop_details),
            ("Export Inventory", self.export_inventory_window),
            ("Logout", self.shopkeeper_menu)
        ]

        for text, command in buttons:
            self.create_button(content_frame, text, command)

    def user_panel(self):
        self.clear_frame()
        content_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        content_frame.pack(pady=20, padx=50, fill="both", expand=True)

        ttk.Label(content_frame, text="User Panel", style="Subtitle.TLabel").pack(pady=(20, 10))

        buttons = [
            ("Search Product", self.search_product_window),
            ("Search by Price", self.search_by_price_window),
            ("Display Brands", self.display_brands),
            ("Shop Details", self.shop_details),
            ("User Profile", self.user_profile_window),
            ("Logout", self.user_menu)
        ]

        for text, command in buttons:
            self.create_button(content_frame, text, command)

    def add_products_window(self):
        self.clear_frame()
        content_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        content_frame.pack(pady=20, padx=50, fill="both", expand=True)

        ttk.Label(content_frame, text="Add Products", style="Subtitle.TLabel").pack(pady=(20, 10))

        ttk.Label(content_frame, text="Shop Name:").pack(anchor="w", padx=20)
        shop_name_entry = self.create_entry(content_frame)

        product_frame = ttk.Frame(content_frame, style="Frame.TFrame")
        product_frame.pack(pady=10, padx=20, fill="x")

        ttk.Label(product_frame, text="Product Name:").pack(anchor="w")
        product_name_entry = self.create_entry(product_frame)

        ttk.Label(product_frame, text="Stock Quantity:").pack(anchor="w")
        stock_entry = self.create_entry(product_frame)

        ttk.Label(product_frame, text="Price:").pack(anchor="w")
        price_entry = self.create_entry(product_frame)

        ttk.Label(product_frame, text="Sizes (comma-separated):").pack(anchor="w")
        sizes_entry = self.create_entry(product_frame)

        ttk.Label(product_frame, text="Category:").pack(anchor="w")
        category_entry = self.create_entry(product_frame)

        def add_product():
            shop_name = shop_name_entry.get().strip()
            if shop_name not in self.data_handler.shops:
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

                category = category_entry.get().strip() or "Uncategorized"

                self.data_handler.shops[shop_name]["Products"][product_name] = {
                    "stock": stock,
                    "Price": price,
                    "Sizes": sizes_list,
                    "Category": category
                }
                self.data_handler.save_shops()
                messagebox.showinfo("Success", f"Product {product_name} added successfully!")
                
                product_name_entry.delete(0, tk.END)
                stock_entry.delete(0, tk.END)
                price_entry.delete(0, tk.END)
                sizes_entry.delete(0, tk.END)
                category_entry.delete(0, tk.END)

            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        def on_shop_name_enter(event):
            product_name_entry.focus_set()

        def on_product_name_enter(event):
            stock_entry.focus_set()

        def on_stock_enter(event):
            price_entry.focus_set()

        def on_price_enter(event):
            sizes_entry.focus_set()

        def on_sizes_enter(event):
            category_entry.focus_set()

        def on_category_enter(event):
            add_product()

        shop_name_entry.bind('<Return>', on_shop_name_enter)
        product_name_entry.bind('<Return>', on_product_name_enter)
        stock_entry.bind('<Return>', on_stock_enter)
        price_entry.bind('<Return>', on_price_enter)
        sizes_entry.bind('<Return>', on_sizes_enter)
        category_entry.bind('<Return>', on_category_enter)

        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=20, fill="x")
        self.create_button(button_frame, "Add Product", add_product, width=15)
        self.create_button(button_frame, "Done", self.admin_panel, width=15)

    def delete_product_window(self):
        self.clear_frame()
        content_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        content_frame.pack(pady=20, padx=50, fill="both", expand=True)

        ttk.Label(content_frame, text="Delete Product", style="Subtitle.TLabel").pack(pady=(20, 10))

        ttk.Label(content_frame, text="Shop Name:").pack(anchor="w", padx=20)
        shop_name_entry = self.create_entry(content_frame)

        ttk.Label(content_frame, text="Product Name:").pack(anchor="w", padx=20)
        product_name_entry = self.create_entry(content_frame)

        def delete():
            shop_name = shop_name_entry.get().strip()
            product_name = product_name_entry.get().strip()

            if shop_name not in self.data_handler.shops:
                messagebox.showerror("Error", "Shop not found!")
                return
            if product_name not in self.data_handler.shops[shop_name]["Products"]:
                messagebox.showerror("Error", "Product not found!")
                return

            del self.data_handler.shops[shop_name]["Products"][product_name]
            self.data_handler.save_shops()
            messagebox.showinfo("Success", "Product deleted successfully!")
            self.admin_panel()

        def on_shop_name_enter(event):
            product_name_entry.focus_set()

        def on_product_name_enter(event):
            delete()

        shop_name_entry.bind('<Return>', on_shop_name_enter)
        product_name_entry.bind('<Return>', on_product_name_enter)

        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=20, fill="x")
        self.create_button(button_frame, "Delete", delete, width=15)
        self.create_button(button_frame, "Back", self.admin_panel, width=15)

    def update_product_window(self):
        self.clear_frame()
        content_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        content_frame.pack(pady=20, padx=50, fill="both", expand=True)

        ttk.Label(content_frame, text="Update Product", style="Subtitle.TLabel").pack(pady=(20, 10))

        ttk.Label(content_frame, text="Shop Name:").pack(anchor="w", padx=20)
        shop_name_entry = self.create_entry(content_frame)

        ttk.Label(content_frame, text="Product Name:").pack(anchor="w", padx=20)
        product_name_entry = self.create_entry(content_frame)

        def check_product():
            shop_name = shop_name_entry.get().strip()
            product_name = product_name_entry.get().strip()

            if shop_name not in self.data_handler.shops:
                messagebox.showerror("Error", "Shop not found!")
                return
            if product_name not in self.data_handler.shops[shop_name]["Products"]:
                messagebox.showerror("Error", "Product not found!")
                return

            update_frame = ttk.Frame(content_frame, style="Frame.TFrame")
            update_frame.pack(pady=10, padx=20, fill="x")

            ttk.Label(update_frame, text="New Price:").pack(anchor="w")
            price_entry = self.create_entry(update_frame)

            ttk.Label(update_frame, text="New Stock:").pack(anchor="w")
            stock_entry = self.create_entry(update_frame)

            ttk.Label(update_frame, text="New Sizes (comma-separated):").pack(anchor="w")
            sizes_entry = self.create_entry(update_frame)

            ttk.Label(update_frame, text="New Category:").pack(anchor="w")
            category_entry = self.create_entry(update_frame)

            def update():
                try:
                    if price_entry.get().strip():
                        price = float(price_entry.get().strip())
                        if price <= 0:
                            raise ValueError("Price must be positive")
                        self.data_handler.shops[shop_name]["Products"][product_name]["Price"] = price

                    if stock_entry.get().strip():
                        stock = int(stock_entry.get().strip())
                        if stock < 0:
                            raise ValueError("Stock cannot be negative")
                        self.data_handler.shops[shop_name]["Products"][product_name]["stock"] = stock

                    if sizes_entry.get().strip():
                        sizes = sizes_entry.get().strip()
                        sizes_list = [int(size.strip()) for size in sizes.split(",") if size.strip()]
                        if not sizes_list:
                            raise ValueError("At least one size must be provided")
                        self.data_handler.shops[shop_name]["Products"][product_name]["Sizes"] = sizes_list

                    if category_entry.get().strip():
                        self.data_handler.shops[shop_name]["Products"][product_name]["Category"] = category_entry.get().strip()

                    self.data_handler.save_shops()
                    messagebox.showinfo("Success", "Product updated successfully!")
                    self.admin_panel()

                except ValueError as e:
                    messagebox.showerror("Error", f"Invalid input: {e}")

            def on_price_enter(event):
                stock_entry.focus_set()

            def on_stock_enter(event):
                sizes_entry.focus_set()

            def on_sizes_enter(event):
                category_entry.focus_set()

            def on_category_enter(event):
                update()

            price_entry.bind('<Return>', on_price_enter)
            stock_entry.bind('<Return>', on_stock_enter)
            sizes_entry.bind('<Return>', on_sizes_enter)
            category_entry.bind('<Return>', on_category_enter)

            self.create_button(update_frame, "Update", update)

        def on_shop_name_enter(event):
            product_name_entry.focus_set()

        def on_product_name_enter(event):
            check_product()

        shop_name_entry.bind('<Return>', on_shop_name_enter)
        product_name_entry.bind('<Return>', on_product_name_enter)

        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=20, fill="x")
        self.create_button(button_frame, "Check Product", check_product, width=15)
        self.create_button(button_frame, "Back", self.admin_panel, width=15)

    def get_search_suggestions(self, query: str) -> List[str]:
        query = query.lower()
        suggestions = set()
        
        for shop_data in self.data_handler.shops.values():
            for product in shop_data["Products"].keys():
                if query in product.lower():
                    suggestions.add(product)
                query_words = query.split()
                product_words = product.lower().split()
                if any(word in product_words for word in query_words):
                    suggestions.add(product)
        
        return sorted(list(suggestions))

    def create_suggestion_listbox(self, parent, entry_widget, callback):
        listbox = tk.Listbox(
            parent,
            height=5,
            font=("Roboto", 10),
            bg=self.colors["input_bg"],
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
        
        entry_widget.bind('<KeyRelease>', update_suggestions)
        listbox.bind('<<ListboxSelect>>', on_select)
        entry_widget.bind('<Escape>', on_escape)
        entry_widget.bind('<Up>', on_up_down)
        entry_widget.bind('<Down>', on_up_down)
        
        return listbox

    def search_product_window(self):
        self.clear_frame()
        content_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        content_frame.pack(pady=20, padx=50, fill="both", expand=True)

        ttk.Label(content_frame, text="Search Product", style="Subtitle.TLabel").pack(pady=(20, 10))

        search_frame = ttk.Frame(content_frame)
        search_frame.pack(fill="x", padx=20, pady=5)

        ttk.Label(search_frame, text="Product Name:").pack(anchor="w")
        product_name_entry = self.create_entry(search_frame)

        result_text = scrolledtext.ScrolledText(
            content_frame,
            height=15,
            font=("Roboto", 10),
            wrap=tk.WORD,
            bg=self.colors["input_bg"]
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
                    "Sizes": brand_data["Sizes"],
                    "Category": brand_data.get("Category", "Uncategorized")
                }
                for shop, shop_data in self.data_handler.shops.items()
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
                    result_text.insert(tk.END, f"Category: {result['Category']}\n")
                    result_text.insert(tk.END, "-" * 50 + "\n\n")
            else:
                result_text.insert(tk.END, "No matching products found.")

        suggestion_listbox = self.create_suggestion_listbox(
            search_frame,
            product_name_entry,
            search
        )

        def on_enter(event):
            search()
            result_text.focus_set()

        product_name_entry.bind('<Return>', on_enter)
        result_text.bind('<Return>', lambda e: product_name_entry.focus_set())

        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=20, fill="x")
        self.create_button(button_frame, "Search", search, width=15)
        self.create_button(button_frame, "Back", self.user_panel, width=15)

    def search_by_price_window(self):
        self.clear_frame()
        content_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        content_frame.pack(pady=20, padx=50, fill="both", expand=True)

        ttk.Label(content_frame, text="Search by Price", style="Subtitle.TLabel").pack(pady=(20, 10))

        ttk.Label(content_frame, text="Maximum Price:").pack(anchor="w", padx=20)
        price_entry = self.create_entry(content_frame)

        result_text = scrolledtext.ScrolledText(
            content_frame,
            height=15,
            font=("Roboto", 10),
            wrap=tk.WORD,
            bg=self.colors["input_bg"]
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
                        "Sizes": brand_data["Sizes"],
                        "Category": brand_data.get("Category", "Uncategorized")
                    }
                    for shop, shop_data in self.data_handler.shops.items()
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
                        result_text.insert(tk.END, f"Category: {result['Category']}\n")
                        result_text.insert(tk.END, "-" * 50 + "\n\n")
                else:
                    result_text.insert(tk.END, "No products found within price range.")

            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        def on_enter(event):
            search()
            result_text.focus_set()

        price_entry.bind('<Return>', on_enter)
        result_text.bind('<Return>', lambda e: price_entry.focus_set())

        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=20, fill="x")
        self.create_button(button_frame, "Search", search, width=15)
        self.create_button(button_frame, "Back", self.user_panel, width=15)

    def display_brands(self):
        self.clear_frame()
        content_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        content_frame.pack(pady=20, padx=50, fill="both", expand=True)

        ttk.Label(content_frame, text="Available Brands", style="Subtitle.TLabel").pack(pady=(20, 10))

        brands = sorted({brand for shop_data in self.data_handler.shops.values() for brand in shop_data["Products"]})
        result_text = scrolledtext.ScrolledText(content_frame, height=15, font=("Roboto", 10), bg=self.colors["input_bg"])
        result_text.pack(pady=10, fill="both", expand=True, padx=20)

        result_text.insert(tk.END, "Available Brands:\n\n")
        for brand in brands:
            result_text.insert(tk.END, f"• {brand}\n")

        self.create_button(content_frame, "Back", self.admin_panel if self.main_frame.winfo_children()[0].winfo_children()[0].cget("text") == "Admin Panel" else self.user_panel)

    def shop_details(self):
        self.clear_frame()
        content_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        content_frame.pack(pady=20, padx=50, fill="both", expand=True)

        ttk.Label(content_frame, text="Shop Details", style="Subtitle.TLabel").pack(pady=(20, 10))

        ttk.Label(content_frame, text="Shop Name:").pack(anchor="w", padx=20)
        shop_name_entry = self.create_entry(content_frame)

        result_text = scrolledtext.ScrolledText(
            content_frame,
            height=15,
            font=("Roboto", 10),
            wrap=tk.WORD,
            bg=self.colors["input_bg"]
        )
        result_text.pack(pady=10, fill="both", expand=True, padx=20)

        def get_shop_suggestions(query: str) -> List[str]:
            query = query.lower()
            return sorted([
                shop for shop in self.data_handler.shops.keys()
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

        suggestion_listbox = tk.Listbox(
            content_frame,
            height=5,
            font=("Roboto", 10),
            bg=self.colors["input_bg"],
            selectmode=tk.SINGLE
        )

        shop_name_entry.bind('<KeyRelease>', update_suggestions)
        suggestion_listbox.bind('<<ListboxSelect>>', on_select)
        shop_name_entry.bind('<Escape>', on_escape)

        def search():
            shop_name = shop_name_entry.get().strip()
            if shop_name in self.data_handler.shops:
                shop_data = self.data_handler.shops[shop_name]
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

        shop_name_entry.bind('<Return>', lambda e: search())

        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=20, fill="x")
        self.create_button(button_frame, "Search", search, width=15)
        self.create_button(button_frame, "Back", self.admin_panel if self.main_frame.winfo_children()[0].winfo_children()[0].cget("text") == "Admin Panel" else self.user_panel, width=15)

    def contact_info(self):
        self.clear_frame()
        content_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        content_frame.pack(pady=20, padx=50, fill="both", expand=True)

        ttk.Label(content_frame, text="Contact Information", style="Subtitle.TLabel").pack(pady=(20, 10))

        contact_text = scrolledtext.ScrolledText(content_frame, height=15, font=("Roboto", 10), bg=self.colors["input_bg"])
        contact_text.pack(pady=10, fill="both", expand=True, padx=20)

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
        self.create_button(content_frame, "Back", self.create_main_menu)

    def user_profile_window(self):
        self.clear_frame()
        content_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        content_frame.pack(pady=20, padx=50, fill="both", expand=True)

        ttk.Label(content_frame, text="User Profile", style="Subtitle.TLabel").pack(pady=(20, 10))

        ttk.Label(content_frame, text="Username:").pack(anchor="w", padx=20)
        username_label = ttk.Label(content_frame, text=self.current_user)
        username_label.pack(anchor="w", padx=20)

        ttk.Label(content_frame, text="New Password:").pack(anchor="w", padx=20)
        password_entry = self.create_entry(content_frame, show="*")

        def update_profile():
            new_password = password_entry.get().strip()
            if new_password and not validate_password(new_password):
                messagebox.showerror("Error", "Invalid password. Must be at least 6 characters.")
                return
            if new_password:
                self.data_handler.user_credentials[self.current_user]["password"] = new_password
                self.data_handler.save_user_credentials()
                messagebox.showinfo("Success", "Profile updated successfully!")
            self.user_panel()

        password_entry.bind('<Return>', lambda e: update_profile())

        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=20, fill="x")
        self.create_button(button_frame, "Update", update_profile, width=15)
        self.create_button(button_frame, "Back", self.user_panel, width=15)

    def export_inventory_window(self):
        self.clear_frame()
        content_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        content_frame.pack(pady=20, padx=50, fill="both", expand=True)

        ttk.Label(content_frame, text="Export Inventory", style="Subtitle.TLabel").pack(pady=(20, 10))

        ttk.Label(content_frame, text="Shop Name:").pack(anchor="w", padx=20)
        shop_name_entry = self.create_entry(content_frame)

        ttk.Label(content_frame, text="Output File (e.g., inventory.csv):").pack(anchor="w", padx=20)
        file_entry = self.create_entry(content_frame)

        def export():
            shop_name = shop_name_entry.get().strip()
            filename = file_entry.get().strip()
            if not filename.endswith(".csv"):
                filename += ".csv"
            if self.data_handler.export_inventory(shop_name, filename):
                messagebox.showinfo("Success", f"Inventory exported to {filename}")
            else:
                messagebox.showerror("Error", "Failed to export inventory. Check shop name.")
            self.admin_panel()

        def on_shop_name_enter(event):
            file_entry.focus_set()

        def on_file_enter(event):
            export()

        shop_name_entry.bind('<Return>', on_shop_name_enter)
        file_entry.bind('<Return>', on_file_enter)

        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=20, fill="x")
        self.create_button(button_frame, "Export", export, width=15)
        self.create_button(button_frame, "Back", self.admin_panel, width=15)