"""
Student 2418326
locustfile_2418326.py
Load testing scenarios for Online Bookstore application

This file defines realistic user behavior patterns for load testing the application
under concurrent load. It simulates multiple users performing common tasks such as
browsing books, managing shopping carts, and completing purchases.

Usage:
    locust -f locustfile_2418326.py --host http://localhost:5000
    
    Then open browser to http://localhost:8089 to configure:
    - Number of users to simulate
    - Spawn rate (users per second)
    - Run time
"""

from locust import HttpUser, task, between, SequentialTaskSet
import random


class BrowsingBehavior(SequentialTaskSet):
    """
    Sequential task set representing a complete user journey from browsing to checkout.
    This ensures tasks execute in a realistic order rather than randomly.
    """
    
    @task
    def load_homepage(self):
        """Browse the homepage and view available books."""
        with self.client.get("/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Homepage failed with status {response.status_code}")
    
    @task
    def add_book_to_cart(self):
        """Add a random book to the shopping cart."""
        books = ['The Great Gatsby', '1984', 'Moby Dick', 'I Ching']
        book_title = random.choice(books)
        quantity = random.randint(1, 3)
        
        with self.client.post("/add-to-cart", 
                            data={'title': book_title, 'quantity': str(quantity)},
                            catch_response=True) as response:
            if response.status_code == 200 or response.status_code == 302:
                response.success()
            else:
                response.failure(f"Add to cart failed with status {response.status_code}")
    
    @task
    def view_cart(self):
        """View the current shopping cart contents."""
        with self.client.get("/cart", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"View cart failed with status {response.status_code}")
    
    @task
    def update_cart_quantity(self):
        """Update the quantity of an item in the cart."""
        books = ['The Great Gatsby', '1984', 'Moby Dick']
        book_title = random.choice(books)
        new_quantity = random.randint(1, 5)
        
        with self.client.post("/update-cart",
                            data={'title': book_title, 'quantity': str(new_quantity)},
                            catch_response=True) as response:
            if response.status_code == 200 or response.status_code == 302:
                response.success()
            else:
                response.failure(f"Update cart failed with status {response.status_code}")
    
    @task
    def proceed_to_checkout(self):
        """Navigate to the checkout page."""
        with self.client.get("/checkout", catch_response=True) as response:
            if response.status_code == 200 or response.status_code == 302:
                response.success()
            else:
                response.failure(f"Checkout page failed with status {response.status_code}")
    
    @task
    def stop_browsing(self):
        """Stop the sequential task set and allow user to start over."""
        self.interrupt()


class CasualBrowser(HttpUser):
    """
    Simulates casual browsers who view pages but don't complete purchases.
    These users represent the majority of website traffic.
    """
    wait_time = between(2, 5)  # Wait 2-5 seconds between actions
    weight = 3  # 3x more common than purchasers
    
    @task(5)
    def browse_homepage(self):
        """Most common action: viewing the homepage."""
        self.client.get("/")
    
    @task(2)
    def view_cart(self):
        """Less common: checking the cart without adding items."""
        self.client.get("/cart")
    
    @task(1)
    def browse_account(self):
        """Occasionally check account page (may redirect to login)."""
        self.client.get("/account")


class ActiveShopper(HttpUser):
    """
    Simulates active shoppers who add items to cart and may complete purchases.
    These users represent engaged customers performing transactions.
    """
    wait_time = between(1, 3)  # Faster actions (engaged users)
    weight = 2  # Less common than casual browsers
    tasks = [BrowsingBehavior]  # Uses sequential task set
    
    def on_start(self):
        """
        Called when a simulated user starts. Can be used for login or setup.
        Currently just ensures the user starts with a fresh session.
        """
        # In a real scenario, this might log in or set up session data
        pass


class RegisteredUser(HttpUser):
    """
    Simulates registered users who log in and interact with their accounts.
    These users represent returning customers with accounts.
    """
    wait_time = between(1, 4)
    weight = 1  # Least common user type
    
    def on_start(self):
        """Log in with demo account credentials."""
        self.client.post("/login", data={
            'email': 'demo@bookstore.com',
            'password': 'demo123'
        })
    
    @task(3)
    def browse_homepage(self):
        """Browse homepage while logged in."""
        self.client.get("/")
    
    @task(2)
    def add_item_to_cart(self):
        """Add items to cart."""
        books = ['The Great Gatsby', '1984']
        self.client.post("/add-to-cart", data={
            'title': random.choice(books),
            'quantity': str(random.randint(1, 2))
        })
    
    @task(1)
    def view_account(self):
        """Check account page (order history, profile)."""
        self.client.get("/account")
    
    @task(1)
    def logout(self):
        """Log out (then will log back in on next iteration)."""
        self.client.get("/logout")


class StressTestUser(HttpUser):
    """
    Aggressive user for stress testing. Performs rapid actions with minimal wait time.
    Use this class to identify breaking points and performance degradation under extreme load.
    
    To use: Comment out other user classes and uncomment this one.
    """
    wait_time = between(0.1, 0.5)  # Very fast actions
    weight = 1
    
    @task
    def rapid_homepage_requests(self):
        """Rapid-fire homepage requests."""
        self.client.get("/")
    
    @task
    def rapid_cart_operations(self):
        """Rapid cart add/view/update cycle."""
        self.client.post("/add-to-cart", data={'title': '1984', 'quantity': '1'})
        self.client.get("/cart")
        self.client.post("/update-cart", data={'title': '1984', 'quantity': '2'})


# Configuration for different testing scenarios
# Uncomment the scenario you want to test:

# SCENARIO 1: Realistic mixed traffic (default)
# Uses all user types with realistic distributions
# Good for: Baseline performance testing
# Command: locust -f locustfile_2418326.py --host http://localhost:5000

# SCENARIO 2: Peak shopping period
# Increase ActiveShopper weight to simulate high-traffic periods
# Good for: Testing capacity during sales or promotions
# Command: locust -f locustfile_2418326.py --host http://localhost:5000 --users 100 --spawn-rate 10

# SCENARIO 3: Stress test
# Use only StressTestUser (comment out other classes)
# Good for: Finding breaking points and maximum capacity
# Command: locust -f locustfile_2418326.py --host http://localhost:5000 --users 200 --spawn-rate 20