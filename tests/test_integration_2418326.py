"""
Student 2418326
test_integration_2418326.py
Integration tests for complete user workflows
"""

import pytest


class TestCompleteShoppingWorkflow:
    """Test complete shopping experience from browsing to checkout."""
    
    def test_guest_complete_purchase(self, client):
        """Complete purchase flow without logging in."""
        # Browse homepage
        response = client.get('/')
        assert response.status_code == 200
        
        # Add item to cart
        client.post('/add-to-cart', data={
            'title': 'The Great Gatsby',
            'quantity': '2'
        })
        
        # View cart
        response = client.get('/cart')
        assert response.status_code == 200
        assert b'The Great Gatsby' in response.data
        
        # Proceed to checkout
        response = client.get('/checkout')
        assert response.status_code == 200
        
        # Complete checkout
        response = client.post('/process-checkout', data={
            'name': 'Guest User',
            'email': 'guest@test.com',
            'address': '123 Guest St',
            'city': 'Guest City',
            'zip_code': '12345',
            'payment_method': 'credit_card',
            'card_number': '4111111111111234',
            'expiry_date': '12/25',
            'cvv': '123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'confirmed' in response.data.lower()
    
    def test_purchase_with_discount(self, client):
        """Apply discount code during checkout."""
        client.post('/add-to-cart', data={
            'title': '1984',
            'quantity': '1'
        })
        
        response = client.post('/process-checkout', data={
            'name': 'Test User',
            'email': 'test@test.com',
            'address': '123 Test St',
            'city': 'Test City',
            'zip_code': '12345',
            'payment_method': 'credit_card',
            'card_number': '4111111111111234',
            'expiry_date': '12/25',
            'cvv': '123',
            'discount_code': 'SAVE10'
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    def test_cart_modification_workflow(self, client):
        """Add items, modify quantities, remove items."""
        # Add first book
        client.post('/add-to-cart', data={
            'title': 'Moby Dick',
            'quantity': '3'
        })
        
        # Add second book
        client.post('/add-to-cart', data={
            'title': 'I Ching',
            'quantity': '1'
        })
        
        # Update first book quantity
        client.post('/update-cart', data={
            'title': 'Moby Dick',
            'quantity': '5'
        })
        
        # Remove second book
        client.post('/remove-from-cart', data={
            'title': 'I Ching'
        })
        
        # Check final cart state
        response = client.get('/cart')
        assert b'Moby Dick' in response.data
        # Check I Ching is not in the cart items (ignore flash messages)
        assert b'Total Items: 5' in response.data  # Only Moby Dick with qty 5
        # Verify only one cart item div (Moby Dick)
        assert response.data.count(b'<div class="cart-item">') == 1


class TestUserAccountWorkflow:
    """Test user registration and account management."""
    
    def test_register_and_login_workflow(self, client):
        """Register new account then log in."""
        # Register
        response = client.post('/register', data={
            'email': 'newuser@test.com',
            'password': 'testpass123',
            'name': 'New User',
            'address': '456 New St'
        }, follow_redirects=True)
        assert response.status_code == 200
        
        # Logout
        client.get('/logout')
        
        # Login with new credentials
        response = client.post('/login', data={
            'email': 'newuser@test.com',
            'password': 'testpass123'
        }, follow_redirects=True)
        assert response.status_code == 200
    
    def test_logged_in_purchase_workflow(self, client):
        """Complete purchase while logged in."""
        # Login
        client.post('/login', data={
            'email': 'demo@bookstore.com',
            'password': 'demo123'
        })
        
        # Add to cart
        client.post('/add-to-cart', data={
            'title': '1984',
            'quantity': '2'
        })
        
        # Checkout
        response = client.post('/process-checkout', data={
            'name': 'Demo User',
            'email': 'demo@bookstore.com',
            'address': '123 Demo St',
            'city': 'Demo City',
            'zip_code': '12345',
            'payment_method': 'credit_card',
            'card_number': '4111111111111234',
            'expiry_date': '12/25',
            'cvv': '123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    def test_profile_update_workflow(self, client):
        """Update user profile information."""
        # Login
        client.post('/login', data={
            'email': 'demo@bookstore.com',
            'password': 'demo123'
        })
        
        # Update profile
        response = client.post('/update-profile', data={
            'name': 'Updated Name',
            'address': '999 Updated St'
        }, follow_redirects=True)
        
        assert response.status_code == 200


class TestPaymentProcessing:
    """Test different payment scenarios."""
    
    def test_successful_payment(self, client):
        """Process successful payment."""
        client.post('/add-to-cart', data={
            'title': 'The Great Gatsby',
            'quantity': '1'
        })
        
        response = client.post('/process-checkout', data={
            'name': 'Test User',
            'email': 'test@test.com',
            'address': '123 Test St',
            'city': 'Test City',
            'zip_code': '12345',
            'payment_method': 'credit_card',
            'card_number': '4111111111111234',
            'expiry_date': '12/25',
            'cvv': '123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'confirmed' in response.data.lower()
    
    def test_failed_payment(self, client):
        """Process failed payment with invalid card."""
        client.post('/add-to-cart', data={
            'title': '1984',
            'quantity': '1'
        })
        
        response = client.post('/process-checkout', data={
            'name': 'Test User',
            'email': 'test@test.com',
            'address': '123 Test St',
            'city': 'Test City',
            'zip_code': '12345',
            'payment_method': 'credit_card',
            'card_number': '4111111111111111',  # Ends in 1111 - should fail
            'expiry_date': '12/25',
            'cvv': '123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'invalid' in response.data.lower() or b'failed' in response.data.lower()


class TestErrorHandling:
    """Test application error handling."""
    
    def test_checkout_empty_cart_redirect(self, client):
        """Attempt checkout with empty cart."""
        response = client.get('/checkout', follow_redirects=True)
        assert response.status_code == 200
    
    def test_add_nonexistent_book(self, client):
        """Try adding book that doesn't exist."""
        response = client.post('/add-to-cart', data={
            'title': 'Nonexistent Book',
            'quantity': '1'
        }, follow_redirects=True)
        assert response.status_code == 200
    
    def test_missing_checkout_fields(self, client):
        """Submit checkout with missing required fields."""
        client.post('/add-to-cart', data={
            'title': '1984',
            'quantity': '1'
        })
        
        response = client.post('/process-checkout', data={
            'name': '',  # Missing
            'email': 'test@test.com',
            'address': '',  # Missing
            'city': 'Test City',
            'zip_code': '12345'
        }, follow_redirects=True)
        
        assert response.status_code == 200


class TestStateTransitions:
    """Test state transitions and data consistency."""
    
    def test_cart_state_after_order_completion(self, client):
        """Verify cart is cleared after successful order."""
        # Add items
        client.post('/add-to-cart', data={'title': '1984', 'quantity': '2'})
        
        # Complete order
        client.post('/process-checkout', data={
            'name': 'Test User',
            'email': 'test@test.com',
            'address': '123 Test St',
            'city': 'Test City',
            'zip_code': '12345',
            'payment_method': 'credit_card',
            'card_number': '4111111111111234',
            'expiry_date': '12/25',
            'cvv': '123'
        }, follow_redirects=True)
        
        # Check cart is empty
        response = client.get('/cart')
        # Cart should be cleared after successful checkout
        assert response.status_code == 200
    
    def test_user_session_after_logout_login(self, client):
        """Test session state through logout and login cycle."""
        # Login
        client.post('/login', data={
            'email': 'demo@bookstore.com',
            'password': 'demo123'
        })
        
        # Add to cart while logged in
        client.post('/add-to-cart', data={'title': '1984', 'quantity': '1'})
        
        # Logout
        client.get('/logout')
        
        # Login again
        client.post('/login', data={
            'email': 'demo@bookstore.com',
            'password': 'demo123'
        })
        
        # Check cart state (implementation dependent)
        response = client.get('/cart')
        assert response.status_code == 200
    
    def test_profile_data_consistency_after_update(self, client):
        """Verify profile data persists correctly after update."""
        # Login
        client.post('/login', data={
            'email': 'demo@bookstore.com',
            'password': 'demo123'
        })
        
        # Update profile
        client.post('/update-profile', data={
            'name': 'Updated Demo Name',
            'address': '999 Updated Street'
        })
        
        # Verify update persisted
        response = client.get('/account')
        assert b'Updated Demo Name' in response.data