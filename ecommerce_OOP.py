class ECommerce:
    users = {}  # Stores registered users
    products = {}  # Stores products
    
    def __init__(self):
        self.logged_in_user = None  # Tracks the current logged-in user
    
# ---- User Functionalities ----
    def register(self):
        """Registers a new user."""
        username = input("Enter username: ")
        if username in self.users:
            print("Username already taken!")
            return
        password = input("Enter password: ")
        self.users[username] = {"password": password, "wallet": 1000}
        print(f"User '{username}' registered successfully!")
    
    def login(self):
        """Logs in an existing user."""
        username = input("Enter username: ")
        password = input("Enter password: ")
        
        if username in self.users and self.users[username]["password"] == password:
            self.logged_in_user = username
            print(f"Welcome, {username}!")
        else:
            print("Invalid username or password.")
    
    def logout(self):
        """Logs out the current user."""
        if self.logged_in_user:
            print(f"User '{self.logged_in_user}' logged out.")
            self.logged_in_user = None
        else:
            print("No user is logged in.")

# ---- Product Functionalities ----
    def add_product(self):
        """Adds a new product (Admin feature)."""
        if self.logged_in_user is None:
            print("You must be logged in to add products.")
            return

        product_id = str(len(self.products) + 1)
        name = input("Enter product name: ")
        price = float(input("Enter product price: "))
        quantity = int(input("Enter product quantity: "))

        self.products[product_id] = {"name": name, "price": price, "quantity": quantity}
        print(f"Product '{name}' added successfully with {quantity} in stock!")

    def view_products(self):
        """Displays available products."""
        if not self.products:
            print("No products available.")
            return
        
        print("\nAvailable Products:")
        for pid, details in self.products.items():
            print(f"{pid}. {details['name']} - ${details['price']} (Stock: {details['quantity']})")

    def buy_product(self):
        """Allows logged-in user to buy a product."""
        if self.logged_in_user is None:
            print("You must be logged in to buy products.")
            return

        self.view_products()
        product_id = input("Enter product ID to buy: ")
        
        if product_id not in self.products:
            print("Invalid product ID.")
            return
        
        product = self.products[product_id]
        if product["quantity"] <= 0:
            print(f"Sorry, {product['name']} is out of stock.")
            return
        
        quantity = int(input(f"Enter quantity of {product['name']} to buy: "))

        if quantity <= 0:
            print("Quantity must be at least 1.")
            return

        if product["quantity"] < quantity:
            print(f"Only {product['quantity']} left in stock!")
            return

        total_price = product["price"] * quantity
        user_wallet = self.users[self.logged_in_user]["wallet"]

        if user_wallet >= total_price:
            self.users[self.logged_in_user]["wallet"] -= total_price
            product["quantity"] -= quantity  # Reduce stock
            print(f"Purchase successful! You bought {quantity} {product['name']}(s) for ${total_price}.")
            print(f"Remaining balance: ${self.users[self.logged_in_user]['wallet']}")
        else:
            print("Insufficient balance. Please add funds.")

    def user_details(self):
        """Displays the current logged-in user's details."""
        if self.logged_in_user is None:
            print("No user is logged in.")
            return
        
        user = self.users[self.logged_in_user]
        print(f"\nUser: {self.logged_in_user}\nWallet Balance: ${user['wallet']}")

    def run(self):
        """Runs the E-Commerce app."""
        while True:
            print("\n1. Register\n2. Login\n3. Add Product\n4. View Products\n5. Buy Product\n6. View User Details\n7. Logout\n8. Exit")
            choice = input("Choose an option: ")
            
            if choice == "1":
                self.register()
            elif choice == "2":
                self.login()
            elif choice == "3":
                self.add_product()
            elif choice == "4":
                self.view_products()
            elif choice == "5":
                self.buy_product()
            elif choice == "6":
                self.user_details()
            elif choice == "7":
                self.logout()
            elif choice == "8":
                print("Exiting E-Commerce app. Goodbye!")
                break
            else:
                print("Invalid choice! Try again.")
##

from abc import ABC, abstractmethod

class User(ABC):
    users = {}  # Stores all registered users

    def __init__(self, username, password):
        self.username = username
        self.__password = password      # Encapsulation
        self.__wallet = 2000000            # Default wallet balance
        User.users[username] = self     # Store user instance

    @abstractmethod
    def view_products(self, products):
        """Abstract method to view products"""
        pass

    def get_wallet_balance(self):
        """Getter for wallet balance"""
        return self.__wallet

    def set_wallet_balance(self, amount):
        """Setter for wallet balance"""
        if amount >= 0:
            self.__wallet = amount
        else:
            print("Invalid amount!")

    def check_password(self, password):
        """Validates user password"""
        return self.__password == password

    wallet_balance=property(get_wallet_balance,set_wallet_balance)




    
    

class Admin(User):
    products = {}  # Stores products

    def __init__(self, username, password):
        super().__init__(username, password)

    def add_product(self, name, price, quantity):
        """Adds a new product"""
        product_id = str(len(Admin.products) + 1)
        Admin.products[product_id] = {"name": name, "price": price, "quantity": quantity}
        print(f"Product '{name}' added successfully!")

    def view_products(self, products=None):
        """Displays available products"""
        if not Admin.products:
            print("No products available.")
            return
        print("\nAvailable Products:")
        for pid, details in Admin.products.items():
            print(f"{pid}. {details['name']} - ${details['price']} (Stock: {details['quantity']})")
##
A1=Admin('admin1',123)
A1.add_product('iphone',100000,4)
A1.add_product('MI',20000,2)

class Customer(User):
    def __init__(self, username, password):
        super().__init__(username, password)

    def buy_product(self, product_id, quantity):
        """Allows customers to buy products"""
        if product_id not in Admin.products:
            print("Invalid product ID.")
            return
        
        product = Admin.products[product_id]
        if product["quantity"] <= 0:
            print(f"Sorry, {product['name']} is out of stock.")
            return

        if quantity <= 0:
            print("Quantity must be at least 1.")
            return

        if product["quantity"] < quantity:
            print(f"Only {product['quantity']} left in stock!")
            return

        total_price = product["price"] * quantity
        if self.get_wallet_balance() >= total_price:
            self.set_wallet_balance(self.get_wallet_balance() - total_price)
            product["quantity"] -= quantity  # Reduce stock
            print(f"Purchase successful! You bought {quantity} {product['name']}(s) for ${total_price}.")
            print(f"Remaining balance: ${self.get_wallet_balance()}")
        else:
            print("Insufficient balance.")

    def view_products(self, products=None):
        """Customers can view products"""
        if not Admin.products:
            print("No products available.")
            return
        print("\nAvailable Products:")
        for pid, details in Admin.products.items():
            print(f"{pid}. {details['name']} - ${details['price']} (Stock: {details['quantity']})")



c1=Customer('customer1',123)












class ECommerce:
    def __init__(self):
        self.logged_in_user = None

    def register(self, user_type):
        """Registers a new user (Admin or Customer)"""
        username = input("Enter username: ")
        if username in User.users:
            print("Username already taken!")
            return
        password = input("Enter password: ")

        if user_type == "admin":
            self.logged_in_user = Admin(username, password)
        else:
            self.logged_in_user = Customer(username, password)
        print(f"User '{username}' registered successfully as {user_type.capitalize()}!")

    def login(self):
        """Logs in an existing user"""
        username = input("Enter username: ")
        password = input("Enter password: ")

        if username in User.users and User.users[username].check_password(password):
            self.logged_in_user = User.users[username]
            print(f"Welcome, {username}!")
        else:
            print("Invalid username or password.")

    def logout(self):
        """Logs out the current user"""
        if self.logged_in_user:
            print(f"User '{self.logged_in_user.username}' logged out.")
            self.logged_in_user = None
        else:
            print("No user is logged in.")

    def run(self):
        """Runs the E-Commerce app"""
        while True:
            print("\n1. Register as Admin\n2. Register as Customer\n3. Login\n4. Add Product\n5.View Products\n6. Buy Product\n7. View Wallet\n8. Logout\n9.\n10set_wallet_balance. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                self.register("admin")
            elif choice == "2":
                self.register("customer")
            elif choice == "3":
                self.login()
            elif choice == "4":
                if isinstance(self.logged_in_user, Admin): #type(self.logged_in_user)=='Admin'
                    name = input("Enter product name: ")
                    price = float(input("Enter product price: "))
                    quantity = int(input("Enter product quantity: "))
                    self.logged_in_user.add_product(name, price, quantity)
                else:
                    print("Only Admins can add products.")
            elif choice == "5":
                if self.logged_in_user:
                    self.logged_in_user.view_products()
                else:
                    print("Please login first.")
            elif choice == "6":
                if isinstance(self.logged_in_user, Customer):
                    product_id = input("Enter product ID to buy: ")
                    quantity = int(input("Enter quantity to buy: "))
                    self.logged_in_user.buy_product(product_id, quantity)
                else:
                    print("Only Customers can buy products.")
            elif choice == "7":
                if self.logged_in_user:
                    print(f"Wallet Balance: ${self.logged_in_user.get_wallet_balance()}")
                else:
                    print("Please login first.")
            elif choice == "8":
                self.logout()
            elif choice == "9":
                print("Exiting E-Commerce app. Goodbye!")
                break
            elif choice == "10":
                if self.logged_in_user:
                    amount=int(input('Enetr Balance'))
                    print(f"Wallet Balance: ${self.logged_in_user.set_wallet_balance(amount)}")
            else:
                print("Invalid choice! Try again.")




e1=ECommerce()

c2=ECommerce()












                

### Run the application
if __name__ == "__main__":
    ecommerce_app = ECommerce()
    ecommerce_app.run()







from abc import ABC,abstractmethod


class User(ABC):
    user={}
    def __init__(self,name,password):
        self.name=name
        self.__password=password
        self.__wallet_balance=1000
        User.user[name]=self
    @abstractmethod
    def view_products(self,products):
        pass
    def get_wallet_balance(self):
        return self.__wallet_balance
    def set_wallet_balance(self,balance):
        self.__wallet_balance=balance
    def check_password(self,password):
        return self.__password==password
    wallet_balance=property(get_wallet_balance,set_wallet_balance)
        
        
class Admin(User):
    products={}
    def __init__(self,username,password):
        super().__init__(username,password)
    def add_products(self,pname,price,quantity):
        product_id=str(len(Admin.products)+1)
        Admin.products[product_id]={'name':pname,'price':price,'quantity':quantity}
        print(f'{pname} is added succussfully!!!!')
    def view_products(self,products=None):
        if not Admin.products:
            print('No products are available')
            return
        else:
            print('Available products are :-')
            for pid,details in Admin.products.items():
                print(f"{pid} : {details['name']} --${details['price']}---(Stock:{details['quantity']})")
            
            
a=Admin('yash',123)
