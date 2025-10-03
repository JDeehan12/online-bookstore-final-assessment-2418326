"""
Student 2418326
conftest.py
Pytest configuration and fixtures for testing the Online Bookstore application.
"""

import pytest
import sys
import os

# Add parent directory to path to import app and models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app, users, orders
from models import Book, Cart, User


@pytest.fixture
def app():
    """Create and configure a test Flask application instance."""
    flask_app.config.update({
        'TESTING': True,
        'SECRET_KEY': 'test_secret_key',
        'WTF_CSRF_ENABLED': False  # Disable CSRF for testing
    })
    
    # Clear global state before each test
    users.clear()
    orders.clear()
    
    # Re-add demo user
    demo_user = User("demo@bookstore.com", "demo123", "Demo User", "123 Demo Street")
    users["demo@bookstore.com"] = demo_user
    
    yield flask_app
    
    # Cleanup after test
    users.clear()
    orders.clear()


@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture
def sample_books():
    """Provide sample books for testing."""
    return [
        Book("Test Book 1", "Fiction", 10.99, "/images/test1.jpg"),
        Book("Test Book 2", "Science", 15.99, "/images/test2.jpg"),
        Book("Test Book 3", "History", 12.49, "/images/test3.jpg")
    ]


@pytest.fixture
def empty_cart():
    """Provide an empty cart for testing."""
    return Cart()


@pytest.fixture
def cart_with_items(sample_books):
    """Provide a cart pre-populated with test items."""
    cart = Cart()
    cart.add_book(sample_books[0], 2)
    cart.add_book(sample_books[1], 1)
    return cart


@pytest.fixture
def test_user():
    """Provide a test user for authentication testing."""
    return User(
        email="test@example.com",
        password="testpass123",
        name="Test User",
        address="123 Test Street, Test City"
    )