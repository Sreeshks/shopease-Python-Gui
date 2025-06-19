import json
import re
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

def load_credentials(file_path: str, default_data: Dict) -> Dict:
    """Load credentials from a JSON file."""
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return default_data

def save_credentials(file_path: str, data: Dict) -> None:
    """Save credentials to a JSON file."""
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Error saving credentials: {e}")

def validate_username(username: str) -> bool:
    """Validate username format."""
    return bool(username and re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

def validate_password(password: str) -> bool:
    """Validate password format."""
    return len(password) >= 6

def display_brands() -> None:
    """Display all available brands."""
    brands = {brand for shop_data in shops.values() for brand in shop_data["Products"]}
    print("\nAvailable Brands:")
    print("-" * 40)
    for brand in sorted(brands):
        print(f"• {brand}")
    print("-" * 40)

def search_product(product_name: str) -> List[Dict[str, Any]]:
    """Search for a product across all shops."""
    return [
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

def search_shop(shop_name: str) -> None:
    """Search for a specific shop and display its details."""
    if shop_name in shops:
        shop_data = shops[shop_name]
        product_count = len(shop_data["Products"])
        product_names = ", ".join(shop_data["Products"].keys())
        print("\nShop Details:")
        print("-" * 40)
        print(f"Shop: {shop_name}")
        print(f"Location: {shop_data['Location']}")
        print(f"Product Count: {product_count}")
        print(f"Products: {product_names}")
        print("-" * 40)
    else:
        print(f"\nShop '{shop_name}' not found.")

def admin_signup() -> bool:
    """Handle admin signup process."""
    if admin_credentials["is_signed_up"]:
        print("\nAdmin is already signed up.")
        return False

    print("\nAdmin Sign-up")
    print("-" * 40)
    username = input("Enter admin username (3-20 characters, alphanumeric): ")
    if not validate_username(username):
        print("Invalid username. Must be 3-20 characters, alphanumeric only.")
        return False

    password = input("Enter admin password (minimum 6 characters): ")
    if not validate_password(password):
        print("Invalid password. Must be at least 6 characters.")
        return False

    shop_name = input("Enter shop name: ").strip()
    if not shop_name:
        print("Shop name cannot be empty.")
        return False

    admin_credentials.update({
        "username": username,
        "password": password,
        "shop_name": shop_name,
        "is_signed_up": True
    })
    save_credentials(ADMIN_CREDENTIALS_FILE, admin_credentials)
    print("\nSign-up successful!")
    print("-" * 40)
    return True

def admin_login() -> bool:
    """Handle admin login process."""
    print("\nAdmin Login")
    print("-" * 40)
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    if (username == admin_credentials["username"] and 
        password == admin_credentials["password"] and 
        admin_credentials["is_signed_up"]):
        print("\nLogin successful!")
        print(f"Current shop: {admin_credentials['shop_name']}")
        if input("Change shop name? (y/n): ").lower() == 'y':
            new_shop_name = input("Enter new shop name: ").strip()
            if new_shop_name:
                admin_credentials["shop_name"] = new_shop_name
                save_credentials(ADMIN_CREDENTIALS_FILE, admin_credentials)
                print("Shop name updated successfully!")
        return True
    print("\nInvalid credentials or admin not signed up.")
    return False

def user_signup() -> bool:
    """Handle user signup process."""
    print("\nUser Sign-up")
    print("-" * 40)
    username = input("Enter username (3-20 characters, alphanumeric): ")
    if not validate_username(username):
        print("Invalid username. Must be 3-20 characters, alphanumeric only.")
        return False

    if username in user_credentials:
        print("Username already exists.")
        return False

    password = input("Enter password (minimum 6 characters): ")
    if not validate_password(password):
        print("Invalid password. Must be at least 6 characters.")
        return False

    user_credentials[username] = password
    save_credentials(USER_CREDENTIALS_FILE, user_credentials)
    print("\nUser sign-up successful!")
    print("-" * 40)
    return True

def user_login() -> bool:
    """Handle user login process."""
    print("\nUser Login")
    print("-" * 40)
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in user_credentials and user_credentials[username] == password:
        print("\nUser login successful!")
        return True
    print("\nInvalid username or password.")
    return False

def add_products() -> None:
    """Add multiple products to a shop, asking shop name only once."""
    shop_name = input("\nEnter shop name: ").strip()
    if shop_name not in shops:
        print("Shop not found!")
        return

    print("\nEnter products (leave product name empty to finish):")
    while True:
        product_name = input("Product name: ").strip()
        if not product_name:
            break

        try:
            stock = int(input(f"Stock quantity for {product_name}: "))
            if stock < 0:
                raise ValueError("Stock cannot be negative")
                
            price = float(input(f"Price for {product_name}: "))
            if price <= 0:
                raise ValueError("Price must be positive")

            sizes = input(f"Sizes for {product_name} (comma-separated): ").strip()
            sizes_list = [int(size.strip()) for size in sizes.split(",") if size.strip()]
            if not sizes_list:
                raise ValueError("At least one size must be provided")

            shops[shop_name]["Products"][product_name] = {
                "stock": stock,
                "Price": price,
                "Sizes": sizes_list
            }
            print(f"Product {product_name} added successfully!")
        except ValueError as e:
            print(f"Error: {e}")
            continue

def delete_product() -> None:
    """Delete a product from a shop."""
    shop_name = input("\nEnter shop name: ").strip()
    if shop_name not in shops:
        print("Shop not found!")
        return

    product_name = input("Enter product name: ").strip()
    if product_name in shops[shop_name]["Products"]:
        del shops[shop_name]["Products"][product_name]
        print("Product deleted successfully!")
    else:
        print("Product not found!")

def update_product() -> None:
    """Update product details."""
    shop_name = input("\nEnter shop name: ").strip()
    if shop_name not in shops:
        print("Shop not found!")
        return

    product_name = input("Enter product name: ").strip()
    if product_name not in shops[shop_name]["Products"]:
        print("Product not found!")
        return

    while True:
        print("\nUpdate Options:")
        print("1. Price")
        print("2. Stock")
        print("3. Sizes")
        print("4. Done")
        choice = input("Choose an option (1-4): ")

        try:
            if choice == "1":
                price = float(input("New price: "))
                if price <= 0:
                    raise ValueError("Price must be positive")
                shops[shop_name]["Products"][product_name]["Price"] = price
                print("Price updated successfully!")
            elif choice == "2":
                stock = int(input("New stock: "))
                if stock < 0:
                    raise ValueError("Stock cannot be negative")
                shops[shop_name]["Products"][product_name]["stock"] = stock
                print("Stock updated successfully!")
            elif choice == "3":
                sizes = input("New sizes (comma-separated): ").strip()
                sizes_list = [int(size.strip()) for size in sizes.split(",") if size.strip()]
                if not sizes_list:
                    raise ValueError("At least one size must be provided")
                shops[shop_name]["Products"][product_name]["Sizes"] = sizes_list
                print("Sizes updated successfully!")
            elif choice == "4":
                break
            else:
                print("Invalid choice!")
        except ValueError as e:
            print(f"Error: {e}")

def main() -> None:
    """Main program loop."""
    global admin_credentials, user_credentials
    admin_credentials = load_credentials(ADMIN_CREDENTIALS_FILE, admin_credentials)
    user_credentials = load_credentials(USER_CREDENTIALS_FILE, user_credentials)

    while True:
        print("\n=== ShopEase: Product Search & Management System ===")
        print("1. Shopkeeper")
        print("2. User")
        print("3. Contact")
        print("4. Send Mail to Developer")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            print("\n=== Shopkeeper Menu ===")
            print("1. Sign-up")
            print("2. Login")
            admin_choice = input("Enter choice (1-2): ").strip()

            if admin_choice == "1":
                admin_signup()
            elif admin_choice == "2":
                if admin_login():
                    while True:
                        print("\n=== Admin Panel ===")
                        print("1. Add Products")
                        print("2. Delete Product")
                        print("3. Update Product")
                        print("4. Display Brands")
                        print("5. Shop Details")
                        print("6. Logout")
                        
                        admin_action = input("Enter choice (1-6): ").strip()
                        
                        if admin_action == "1":
                            add_products()
                        elif admin_action == "2":
                            delete_product()
                        elif admin_action == "3":
                            update_product()
                        elif admin_action == "4":
                            display_brands()
                        elif admin_action == "5":
                            search_shop(admin_credentials["shop_name"])
                        elif admin_action == "6":
                            print("\nLogged out successfully!")
                            break
                        else:
                            print("\nInvalid choice!")

        elif choice == "2":
            print("\n=== User Menu ===")
            print("1. Sign-up")
            print("2. Login")
            user_choice = input("Enter choice (1-2): ").strip()

            if user_choice == "1":
                user_signup()
            elif user_choice == "2":
                if user_login():
                    while True:
                        print("\n=== User Panel ===")
                        print("1. Search Product")
                        print("2. Search by Price")
                        print("3. Display Brands")
                        print("4. Shop Details")
                        print("5. Logout")
                        
                        user_action = input("Enter choice (1-5): ").strip()
                        
                        if user_action == "1":
                            product_name = input("\nEnter product name: ").strip()
                            results = search_product(product_name)
                            if results:
                                print("\nMatching products found:")
                                for result in results:
                                    print("\n" + "-" * 40)
                                    print(f"Shop: {result['Shop']}")
                                    print(f"Location: {result['Location']}")
                                    print(f"Stock: {result['stock']}")
                                    print(f"Price: ₹{result['Price']}")
                                    print(f"Sizes: {result['Sizes']}")
                                    print("-" * 40)
                            else:
                                print("\nNo matching products found.")
                        
                        elif user_action == "2":
                            try:
                                max_price = float(input("\nEnter maximum price: "))
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
                                
                                if results:
                                    print("\nProducts within price range:")
                                    for result in results:
                                        print("\n" + "-" * 40)
                                        print(f"Shop: {result['Shop']}")
                                        print(f"Location: {result['Location']}")
                                        print(f"Brand: {result['Brand']}")
                                        print(f"Stock: {result['stock']}")
                                        print(f"Price: ₹{result['Price']}")
                                        print(f"Sizes: {result['Sizes']}")
                                        print("-" * 40)
                                else:
                                    print("\nNo products found within price range.")
                            except ValueError as e:
                                print(f"Error: {e}")
                        
                        elif user_action == "3":
                            display_brands()
                        elif user_action == "4":
                            shop_name = input("\nEnter shop name: ").strip()
                            search_shop(shop_name)
                        elif user_action == "5":
                            print("\nLogged out successfully!")
                            break
                        else:
                            print("\nInvalid choice!")

        elif choice == "3":
            print("\n=== Contact Information ===")
            print("Website: https://en.wikipedia.org/wiki/Shoe")
            print("Instagram: https://www.instagram.com/shope_ease")
            print("Telegram: http://t.me/ShopEase")
            print("Email: shopease@gmail.com")
            print("Phone: +918129690147, +918157843684")
            print("Developers: Edwin, Abhirami, Sreesh")
            print("-" * 40)

        elif choice == "4":
            print("\n=== Contact Developer ===")
            recipient = input("Recipient's email: ").strip()
            subject = input("Subject: ").strip()
            message = input("Message: ").strip()
            print("\nSending mail...")
            print("Mail sent successfully!")
            print("-" * 40)

        elif choice == "5":
            print("\nThank you for using ShopEase!")
            break

        else:
            print("\nInvalid choice!")

if __name__ == "__main__":
    main()