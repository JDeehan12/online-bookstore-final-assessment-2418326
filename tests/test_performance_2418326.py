"""
Student 2418326
test_performance_2418326.py
Performance and profiling tests for identifying code efficiency issues
"""

import pytest
import timeit
import cProfile
import pstats
import io
from models import Cart, Book, CartItem, User, Order


class TestCartPerformance:
    """Performance tests for Cart operations."""
    
    def test_cart_total_calculation_performance(self, sample_books):
        """Test cart total calculation speed with different quantities."""
        cart = Cart()
        
        # Small quantity - should be fast
        cart.add_book(sample_books[0], 10)
        start_time = timeit.default_timer()
        total = cart.get_total_price()
        small_time = timeit.default_timer() - start_time
        
        # Clear and test with larger quantity
        cart.clear()
        cart.add_book(sample_books[0], 1000)
        start_time = timeit.default_timer()
        total = cart.get_total_price()
        large_time = timeit.default_timer() - start_time
        
        # Document the performance difference
        print(f"\nSmall quantity (10): {small_time:.6f} seconds")
        print(f"Large quantity (1000): {large_time:.6f} seconds")
        print(f"Performance ratio: {large_time/small_time:.2f}x slower")
        
        # This reveals the inefficiency - should be linear but might be worse
        # With the current nested loop, large quantities are significantly slower
    
    def test_cart_multiple_items_performance(self, sample_books):
        """Test performance with multiple different books."""
        cart = Cart()
        
        # Add multiple books with various quantities
        for i, book in enumerate(sample_books):
            cart.add_book(book, (i + 1) * 100)
        
        # Time the total calculation
        execution_time = timeit.timeit(
            lambda: cart.get_total_price(),
            number=100
        )
        
        avg_time = execution_time / 100
        print(f"\nAverage time for multi-item cart: {avg_time:.6f} seconds")
    
    def test_profile_cart_operations(self, sample_books):
        """Profile cart operations to identify bottlenecks."""
        profiler = cProfile.Profile()
        cart = Cart()
        
        # Profile adding items and calculating total
        profiler.enable()
        
        for book in sample_books:
            cart.add_book(book, 500)
        
        for _ in range(10):
            total = cart.get_total_price()
        
        profiler.disable()
        
        # Output profiling results
        s = io.StringIO()
        ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
        ps.print_stats()
        
        print("\n" + "="*60)
        print("PROFILING RESULTS FOR CART OPERATIONS")
        print("="*60)
        print(s.getvalue())


class TestUserPerformance:
    """Performance tests for User operations."""
    
    def test_user_order_sorting_performance(self, test_user):
        """Test performance of order management with sorting."""
        # Add many orders to test sorting performance
        num_orders = 100
        
        start_time = timeit.default_timer()
        for i in range(num_orders):
            order = Order(f"ORD{i:03d}", test_user.email, [], {}, {}, 50.0)
            test_user.add_order(order)
        end_time = timeit.default_timer()
        
        total_time = end_time - start_time
        avg_time = total_time / num_orders
        
        print(f"\nAdding {num_orders} orders took: {total_time:.4f} seconds")
        print(f"Average time per order: {avg_time:.6f} seconds")
        print("Note: Each add_order() sorts the entire list - this is inefficient")
    
    def test_user_order_history_retrieval(self, test_user):
        """Test order history retrieval performance."""
        # Add some orders
        for i in range(50):
            order = Order(f"ORD{i:03d}", test_user.email, [], {}, {}, 50.0)
            test_user.add_order(order)
        
        # Time the retrieval
        execution_time = timeit.timeit(
            lambda: test_user.get_order_history(),
            number=1000
        )
        
        avg_time = execution_time / 1000
        print(f"\nAverage order history retrieval: {avg_time:.6f} seconds")
        print("Note: Creates new list each time instead of returning reference")


class TestComparisonBeforeOptimisation:
    """Baseline performance measurements before optimisation."""
    
    def test_baseline_cart_calculation(self):
        """Establish baseline for cart price calculation."""
        cart = Cart()
        book = Book("Test", "Test", 9.99, "/test.jpg")
        
        # Test with different quantities
        quantities = [10, 100, 500, 1000, 5000]
        
        print("\n" + "="*60)
        print("BASELINE PERFORMANCE - CART TOTAL CALCULATION")
        print("="*60)
        
        for qty in quantities:
            cart.clear()
            cart.add_book(book, qty)
            
            execution_time = timeit.timeit(
                lambda: cart.get_total_price(),
                number=100
            )
            
            avg_time = execution_time / 100
            print(f"Quantity {qty:5d}: {avg_time:.6f} seconds (100 iterations)")
        
        print("\nThese baseline times will be compared with post-optimisation results")

class TestMemoryEfficiency:
    """Test memory efficiency improvements."""
    
    def test_user_memory_footprint(self):
        """Measure memory usage of User objects after removing unused attributes."""
        import sys
        
        # Create a user
        user = User("test@test.com", "pass123", "Test User", "123 Test St")
        
        # Get size of user object
        user_size = sys.getsizeof(user.__dict__)
        
        print(f"\nUser object __dict__ size: {user_size} bytes")
        print(f"User attributes: {list(user.__dict__.keys())}")
        print(f"Number of attributes: {len(user.__dict__)}")
        
        # Before fix: 7 attributes (email, password, name, address, orders, temp_data, cache)
        # After fix: 5 attributes (email, password, name, address, orders)
        # Improvement: 2 fewer attributes per user instance
        
        assert len(user.__dict__) == 5  # Should have exactly 5 attributes now
        assert 'temp_data' not in user.__dict__
        assert 'cache' not in user.__dict__