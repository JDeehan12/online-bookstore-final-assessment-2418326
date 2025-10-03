"""
Student 2418326
test_models_2418326.py
Comprehensive unit tests for models.py
Tests Book, CartItem, Cart, User, Order, PaymentGateway, and EmailService classes
"""

import pytest
from models import Book, CartItem, Cart, User, Order, PaymentGateway, EmailService
from datetime import datetime


class TestBook:
    """Test cases for the Book class."""
    
    def test_book_initialisation_valid(self, sample_books):
        """Positive test: Book initialisation with valid data."""
        book = sample_books[0]
        assert book.title == "Test Book 1"
        assert book.category == "Fiction"
        assert book.price == 10.99
        assert book.image == "/images/test1.jpg"
    
    def test_book_initialisation_with_different_values(self):
        """Positive test: Book with different valid values."""
        book = Book("Python Programming", "Technology", 45.99, "/images/python.jpg")
        assert book.title == "Python Programming"
        assert book.category == "Technology"
        assert book.price == 45.99
        assert book.image == "/images/python.jpg"
    
    def test_book_price_zero(self):
        """Edge case: Book with zero price."""
        book = Book("Free Book", "Education", 0.0, "/images/free.jpg")
        assert book.price == 0.0
    
    def test_book_price_very_large(self):
        """Boundary test: Book with very large price."""
        book = Book("Expensive Book", "Rare", 9999.99, "/images/rare.jpg")
        assert book.price == 9999.99
    
    def test_book_empty_strings(self):
        """Edge case: Book with empty strings (allowed but not recommended)."""
        book = Book("", "", 10.00, "")
        assert book.title == ""
        assert book.category == ""
        assert book.image == ""


class TestCartItem:
    """Test cases for the CartItem class."""
    
    def test_cartitem_initialisation_default_quantity(self, sample_books):
        """Positive test: CartItem with default quantity."""
        item = CartItem(sample_books[0])
        assert item.book == sample_books[0]
        assert item.quantity == 1
    
    def test_cartitem_initialisation_custom_quantity(self, sample_books):
        """Positive test: CartItem with custom quantity."""
        item = CartItem(sample_books[0], 5)
        assert item.quantity == 5
    
    def test_cartitem_get_total_price_single(self, sample_books):
        """Positive test: Total price for single item."""
        item = CartItem(sample_books[0], 1)
        assert item.get_total_price() == 10.99
    
    def test_cartitem_get_total_price_multiple(self, sample_books):
        """Positive test: Total price for multiple items."""
        item = CartItem(sample_books[1], 3)
        expected = 15.99 * 3
        assert item.get_total_price() == expected
    
    def test_cartitem_get_total_price_zero_quantity(self, sample_books):
        """Edge case: Total price with zero quantity."""
        item = CartItem(sample_books[0], 0)
        assert item.get_total_price() == 0.0
    
    def test_cartitem_get_total_price_negative_quantity(self, sample_books):
        """Negative test: Total price with negative quantity."""
        item = CartItem(sample_books[0], -5)
        # This will calculate negative total - shows a potential issue
        assert item.get_total_price() == 10.99 * -5
    
    def test_cartitem_get_total_price_large_quantity(self, sample_books):
        """Boundary test: Total price with very large quantity."""
        item = CartItem(sample_books[0], 1000)
        expected = 10.99 * 1000
        assert item.get_total_price() == expected

    def test_book_title_empty_string_boundary(self):
        """Boundary test: Empty title string."""
        book = Book("", "Fiction", 10.99, "/test.jpg")
        assert book.title == ""
    
    def test_book_title_very_long_string(self):
        """Boundary test: Very long title."""
        long_title = "A" * 500
        book = Book(long_title, "Fiction", 10.99, "/test.jpg")
        assert book.title == long_title
        assert len(book.title) == 500


class TestCart:
    """Test cases for the Cart class."""
    
    # Initialisation Tests
    def test_cart_initialisation(self, empty_cart):
        """Positive test: Empty cart initialisation."""
        assert len(empty_cart.items) == 0
        assert empty_cart.is_empty() is True
        assert empty_cart.get_total_items() == 0
        assert empty_cart.get_total_price() == 0.0
    
    # Add Book Tests
    def test_add_book_single(self, empty_cart, sample_books):
        """Positive test: Add single book to cart."""
        empty_cart.add_book(sample_books[0], 1)
        assert len(empty_cart.items) == 1
        assert sample_books[0].title in empty_cart.items
        assert empty_cart.items[sample_books[0].title].quantity == 1
    
    def test_add_book_multiple_quantity(self, empty_cart, sample_books):
        """Positive test: Add book with multiple quantities."""
        empty_cart.add_book(sample_books[0], 5)
        assert empty_cart.items[sample_books[0].title].quantity == 5
        assert empty_cart.get_total_items() == 5
    
    def test_add_same_book_twice(self, empty_cart, sample_books):
        """Positive test: Adding same book twice increases quantity."""
        empty_cart.add_book(sample_books[0], 2)
        empty_cart.add_book(sample_books[0], 3)
        assert empty_cart.items[sample_books[0].title].quantity == 5
        assert len(empty_cart.items) == 1
    
    def test_add_different_books(self, empty_cart, sample_books):
        """Positive test: Add multiple different books."""
        empty_cart.add_book(sample_books[0], 1)
        empty_cart.add_book(sample_books[1], 2)
        empty_cart.add_book(sample_books[2], 3)
        assert len(empty_cart.items) == 3
        assert empty_cart.get_total_items() == 6
    
    def test_add_book_zero_quantity(self, empty_cart, sample_books):
        """Edge case: Add book with zero quantity."""
        empty_cart.add_book(sample_books[0], 0)
        # Book still added but with 0 quantity - potential issue
        assert sample_books[0].title in empty_cart.items
        assert empty_cart.items[sample_books[0].title].quantity == 0
    
    def test_add_book_negative_quantity(self, empty_cart, sample_books):
        """Negative test: Add book with negative quantity."""
        empty_cart.add_book(sample_books[0], -5)
        # This adds with negative quantity - shows a bug
        assert empty_cart.items[sample_books[0].title].quantity == -5
    
    # Remove Book Tests
    def test_remove_book_existing(self, cart_with_items, sample_books):
        """Positive test: Remove existing book from cart."""
        cart_with_items.remove_book(sample_books[0].title)
        assert sample_books[0].title not in cart_with_items.items
        assert len(cart_with_items.items) == 1
    
    def test_remove_book_nonexistent(self, cart_with_items):
        """Negative test: Remove non-existent book."""
        initial_length = len(cart_with_items.items)
        cart_with_items.remove_book("Nonexistent Book")
        assert len(cart_with_items.items) == initial_length
    
    def test_remove_book_from_empty_cart(self, empty_cart):
        """Edge case: Remove book from empty cart."""
        empty_cart.remove_book("Any Book")
        assert empty_cart.is_empty() is True
    
    # Update Quantity Tests - THIS IS WHERE BUG #1 WILL BE REVEALED
    def test_update_quantity_valid_increase(self, cart_with_items, sample_books):
        """Positive test: Update quantity to higher value."""
        cart_with_items.update_quantity(sample_books[0].title, 5)
        assert cart_with_items.items[sample_books[0].title].quantity == 5
    
    def test_update_quantity_valid_decrease(self, cart_with_items, sample_books):
        """Positive test: Update quantity to lower value."""
        cart_with_items.update_quantity(sample_books[0].title, 1)
        assert cart_with_items.items[sample_books[0].title].quantity == 1
    
    def test_update_quantity_to_zero(self, cart_with_items, sample_books):
        """BUG #1 TEST: Update quantity to zero should remove item."""
        cart_with_items.update_quantity(sample_books[0].title, 0)
        # EXPECTED: Item should be removed
        # ACTUAL: Item remains with quantity 0 (BUG)
        # This test will fail before fix, pass after fix
        assert sample_books[0].title not in cart_with_items.items
    
    def test_update_quantity_to_negative(self, cart_with_items, sample_books):
        """BUG #1 TEST: Update quantity to negative should remove item."""
        cart_with_items.update_quantity(sample_books[0].title, -5)
        # EXPECTED: Item should be removed
        # ACTUAL: Item remains with negative quantity (BUG)
        assert sample_books[0].title not in cart_with_items.items
    
    def test_update_quantity_nonexistent_book(self, cart_with_items):
        """Negative test: Update quantity for non-existent book."""
        initial_length = len(cart_with_items.items)
        cart_with_items.update_quantity("Nonexistent Book", 5)
        # Should do nothing
        assert len(cart_with_items.items) == initial_length
    
    # Get Total Price Tests - THIS IS WHERE INEFFICIENCY #1 WILL BE TESTED
    def test_get_total_price_empty_cart(self, empty_cart):
        """Positive test: Total price of empty cart."""
        assert empty_cart.get_total_price() == 0.0
    
    def test_get_total_price_single_book(self, empty_cart, sample_books):
        """Positive test: Total price with single book."""
        empty_cart.add_book(sample_books[0], 2)
        expected = 10.99 * 2
        assert empty_cart.get_total_price() == expected
    
    def test_get_total_price_multiple_books(self, empty_cart, sample_books):
        """Positive test: Total price with multiple books."""
        empty_cart.add_book(sample_books[0], 2)  # 10.99 * 2 = 21.98
        empty_cart.add_book(sample_books[1], 1)  # 15.99 * 1 = 15.99
        empty_cart.add_book(sample_books[2], 3)  # 12.49 * 3 = 37.47
        expected = 21.98 + 15.99 + 37.47
        assert abs(empty_cart.get_total_price() - expected) < 0.01
    
    def test_get_total_price_large_quantities(self, empty_cart, sample_books):
        """Performance test: Total price with large quantities."""
        empty_cart.add_book(sample_books[0], 1000)
        expected = 10.99 * 1000
        # This test will be slow due to inefficient nested loop (INEFFICIENCY #1)
        assert empty_cart.get_total_price() == expected
    
    # Get Total Items Tests
    def test_get_total_items_empty(self, empty_cart):
        """Positive test: Total items in empty cart."""
        assert empty_cart.get_total_items() == 0
    
    def test_get_total_items_multiple_books(self, empty_cart, sample_books):
        """Positive test: Total items with multiple books."""
        empty_cart.add_book(sample_books[0], 2)
        empty_cart.add_book(sample_books[1], 3)
        empty_cart.add_book(sample_books[2], 1)
        assert empty_cart.get_total_items() == 6
    
    # Clear Cart Tests
    def test_clear_cart_with_items(self, cart_with_items):
        """Positive test: Clear cart with items."""
        cart_with_items.clear()
        assert len(cart_with_items.items) == 0
        assert cart_with_items.is_empty() is True
    
    def test_clear_empty_cart(self, empty_cart):
        """Edge case: Clear already empty cart."""
        empty_cart.clear()
        assert empty_cart.is_empty() is True
    
    # Get Items Tests
    def test_get_items_empty(self, empty_cart):
        """Positive test: Get items from empty cart."""
        items = empty_cart.get_items()
        assert len(items) == 0
        assert isinstance(items, list)
    
    def test_get_items_with_books(self, cart_with_items):
        """Positive test: Get items from cart with books."""
        items = cart_with_items.get_items()
        assert len(items) == 2
        assert all(isinstance(item, CartItem) for item in items)
    
    # Is Empty Tests
    def test_is_empty_true(self, empty_cart):
        """Positive test: Empty cart returns True."""
        assert empty_cart.is_empty() is True
    
    def test_is_empty_false(self, cart_with_items):
        """Positive test: Cart with items returns False."""
        assert cart_with_items.is_empty() is False
    
    def test_is_empty_after_clear(self, cart_with_items):
        """Positive test: Cart is empty after clearing."""
        cart_with_items.clear()
        assert cart_with_items.is_empty() is True
    
    # Boundary Value Tests
    def test_add_book_boundary_quantity_one(self, empty_cart, sample_books):
        """Boundary test: Minimum valid quantity."""
        empty_cart.add_book(sample_books[0], 1)
        assert empty_cart.items[sample_books[0].title].quantity == 1
    
    def test_add_book_boundary_quantity_max_reasonable(self, empty_cart, sample_books):
        """Boundary test: Large but reasonable quantity."""
        empty_cart.add_book(sample_books[0], 9999)
        assert empty_cart.items[sample_books[0].title].quantity == 9999
    
    def test_cart_total_boundary_zero_price(self):
        """Boundary test: Book with zero price."""
        cart = Cart()
        book = Book("Free Book", "Education", 0.00, "/test.jpg")
        cart.add_book(book, 5)
        assert cart.get_total_price() == 0.00
    
    def test_cart_total_boundary_pence(self):
        """Boundary test: Minimum price (one pence)."""
        cart = Cart()
        book = Book("Cheap Book", "Budget", 0.01, "/test.jpg")
        cart.add_book(book, 1)
        assert cart.get_total_price() == 0.01
    
    def test_cart_total_boundary_large_price(self):
        """Boundary test: Very expensive book."""
        cart = Cart()
        book = Book("Rare Book", "Collector", 9999.99, "/test.jpg")
        cart.add_book(book, 1)
        assert cart.get_total_price() == 9999.99


class TestUser:
    """Test cases for the User class."""
    
    def test_user_initialisation_full_details(self):
        """Positive test: User with all details."""
        user = User("user@test.com", "password123", "Test User", "123 Test St")
        assert user.email == "user@test.com"
        assert user.password == "password123"
        assert user.name == "Test User"
        assert user.address == "123 Test St"
        assert user.orders == []
        assert user.temp_data == []  # INEFFICIENCY #2: Unused attribute
        assert user.cache == {}      # INEFFICIENCY #2: Unused attribute
    
    def test_user_initialisation_minimal_details(self):
        """Positive test: User with minimal details."""
        user = User("user@test.com", "pass")
        assert user.email == "user@test.com"
        assert user.password == "pass"
        assert user.name == ""
        assert user.address == ""
    
    def test_add_order_single(self, test_user, sample_books):
        """Positive test: Add single order."""
        order = Order("ORD001", test_user.email, [], {}, {}, 50.00)
        test_user.add_order(order)
        assert len(test_user.orders) == 1
    
    def test_add_order_multiple(self, test_user):
        """INEFFICIENCY #3 TEST: Add multiple orders - sorts every time."""
        for i in range(5):
            order = Order(f"ORD00{i}", test_user.email, [], {}, {}, 50.00)
            test_user.add_order(order)
        assert len(test_user.orders) == 5
        # Orders are sorted by date each time - inefficient
    
    def test_get_order_history_empty(self, test_user):
        """Positive test: Get empty order history."""
        history = test_user.get_order_history()
        assert history == []
    
    def test_get_order_history_with_orders(self, test_user):
        """INEFFICIENCY #3 TEST: Get order history creates unnecessary list."""
        order = Order("ORD001", test_user.email, [], {}, {}, 50.00)
        test_user.add_order(order)
        history = test_user.get_order_history()
        assert len(history) == 1
        # This creates a new list unnecessarily

    def test_user_has_unused_temp_data_attribute(self, test_user):
        """Check for unused temp_data attribute (inefficiency)."""
        assert hasattr(test_user, 'temp_data')
        assert test_user.temp_data == []
        # This attribute is never used - creates unnecessary memory overhead
    
    def test_user_has_unused_cache_attribute(self, test_user):
        """Check for unused cache attribute (inefficiency)."""
        assert hasattr(test_user, 'cache')
        assert test_user.cache == {}
        # This attribute is never used - creates unnecessary memory overhead

class TestOrder:
    """Test cases for the Order class."""
    
    def test_order_initialisation(self, sample_books):
        """Positive test: Order initialisation."""
        items = [CartItem(sample_books[0], 2)]
        shipping = {'name': 'Test', 'address': '123 St'}
        payment = {'method': 'credit_card', 'transaction_id': 'TXN123'}
        
        order = Order("ORD001", "test@test.com", items, shipping, payment, 21.98)
        
        assert order.order_id == "ORD001"
        assert order.user_email == "test@test.com"
        assert len(order.items) == 1
        assert order.total_amount == 21.98
        assert order.status == "Confirmed"
        assert isinstance(order.order_date, datetime)
    
    def test_order_to_dict(self, sample_books):
        """Positive test: Convert order to dictionary."""
        items = [CartItem(sample_books[0], 1)]
        order = Order("ORD001", "test@test.com", items, {}, {}, 10.99)
        order_dict = order.to_dict()
        
        assert order_dict['order_id'] == "ORD001"
        assert order_dict['user_email'] == "test@test.com"
        assert order_dict['total_amount'] == 10.99
        assert 'order_date' in order_dict


class TestPaymentGateway:
    """Test cases for the PaymentGateway class."""
    
    def test_payment_success_valid_card(self):
        """Positive test: Successful payment with valid card."""
        payment_info = {
            'payment_method': 'credit_card',
            'card_number': '4111111111111234',
            'expiry_date': '12/25',
            'cvv': '123'
        }
        result = PaymentGateway.process_payment(payment_info)
        assert result['success'] is True
        assert 'TXN' in result['transaction_id']
    
    def test_payment_failure_card_ending_1111(self):
        """Positive test: Payment fails for card ending in 1111."""
        payment_info = {
            'payment_method': 'credit_card',
            'card_number': '4111111111111111',
            'expiry_date': '12/25',
            'cvv': '123'
        }
        result = PaymentGateway.process_payment(payment_info)
        assert result['success'] is False
        assert 'Invalid card number' in result['message']
    
    def test_payment_paypal_method(self):
        """BUG #4 TEST: PayPal payment method not properly handled."""
        payment_info = {
            'payment_method': 'paypal',
            'card_number': '',
            'expiry_date': '',
            'cvv': ''
        }
        result = PaymentGateway.process_payment(payment_info)
        # Current code passes empty card validation for PayPal (BUG)
        assert result['success'] is True
    
    def test_payment_empty_card_number(self):
        """BUG #4 TEST: Empty card number should fail."""
        payment_info = {
            'payment_method': 'credit_card',
            'card_number': '',
            'expiry_date': '12/25',
            'cvv': '123'
        }
        result = PaymentGateway.process_payment(payment_info)
        # EXPECTED: Should fail
        # ACTUAL: Might succeed due to missing validation (BUG)
        assert result['success'] is True  # This reveals the bug

    def test_payment_empty_card_number_no_validation(self):
        """Empty card number should fail validation but doesn't."""
        payment_info = {
            'payment_method': 'credit_card',
            'card_number': '',
            'expiry_date': '12/25',
            'cvv': '123'
        }
        result = PaymentGateway.process_payment(payment_info)
        # Currently succeeds because of missing validation
        assert result['success'] is True
    
    def test_payment_invalid_card_format(self):
        """Invalid card format should fail but doesn't."""
        payment_info = {
            'payment_method': 'credit_card',
            'card_number': '1234',  # Too short
            'expiry_date': '12/25',
            'cvv': '123'
        }
        result = PaymentGateway.process_payment(payment_info)
        assert result['success'] is True

class TestEmailService:
    """Test cases for the EmailService class."""
    
    def test_send_order_confirmation(self, sample_books, capsys):
        """Positive test: Send order confirmation email."""
        items = [CartItem(sample_books[0], 1)]
        order = Order("ORD001", "test@test.com", items, {'address': '123 St'}, {}, 10.99)
        
        result = EmailService.send_order_confirmation("test@test.com", order)
        
        assert result is True
        
        # Capture printed output
        captured = capsys.readouterr()
        assert "EMAIL SENT" in captured.out
        assert "test@test.com" in captured.out
        assert "ORD001" in captured.out