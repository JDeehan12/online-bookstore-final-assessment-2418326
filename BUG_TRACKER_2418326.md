# Bug Tracking Document - Student 2418326

## Bugs Discovered

---

## Functional Bugs

### [BUG-001] Cart Update Quantity - Zero/Negative Not Handled
**Status**: Identified
**Location**: `models.py` - `Cart.update_quantity()` method
**Discovered**: Manual testing - 3rd October 2025
**Reproduction Steps**:
1. Add item to cart
2. Update quantity to 0
3. Item remains in cart instead of being removed

**Expected Behaviour**: Items with quantity <= 0 should be removed from cart
**Actual Behaviour**: Quantity is set but item not removed
**Priority**: Major
**Fix Status**: Pending

---

### [BUG-002] Case-Sensitive Discount Codes
**Status**: Identified
**Location**: `app.py` - `process_checkout()` route
**Discovered**: Manual testing - 3rd October 2025
**Reproduction Steps**:
1. Add items to cart
2. Proceed to checkout
3. Enter "save10" (lowercase)
4. Discount not applied

**Expected Behaviour**: Discount codes should be case-insensitive
**Actual Behaviour**: Only exact case matches work (SAVE10, WELCOME20)
**Priority**: Major
**Fix Status**: Pending

---

### [BUG-003] Floating Point Precision in Cart Total Calculation
**Status**: Identified
**Location**: `models.py` - `Cart.get_total_price()` method
**Discovered**: Unit testing - 3rd October 2025
**Reproduction Steps**:
1. Add item with large quantity (1000) to cart
2. Calculate total price
3. Observe floating-point precision error

**Expected Behaviour**: Accurate price calculation even with large quantities
**Actual Behaviour**: Floating-point arithmetic errors accumulate (10990.0 vs 10989.999999999825)
**Priority**: Minor (cosmetic, but indicates deeper inefficiency issue)
**Fix Status**: Pending
**Related**: INEFFICIENCY #1 - nested loop amplifies precision errors

---

### [BUG-004] Missing Payment Field Validation
**Status**: Identified
**Location**: `models.py` - `PaymentGateway.process_payment()` method
**Discovered**: Additional testing - 3rd October 2025
**Reproduction Steps**:
1. Attempt checkout with empty card number
2. Payment processes successfully despite missing required field

**Expected Behaviour**: Should validate all payment fields and reject empty or invalid card information
**Actual Behaviour**: Accepts empty card numbers and invalid formats without validation
**Priority**: High
**Fix Status**: Pending

---

### [BUG-005] No Email Format Validation
**Status**: Identified
**Location**: `app.py` - `register()` route
**Discovered**: Additional testing - 3rd October 2025
**Reproduction Steps**:
1. Register with invalid email format (e.g., "notanemail.com")
2. System accepts registration without validation

**Expected Behaviour**: Should validate email format using standard email validation
**Actual Behaviour**: Accepts any string as email address
**Priority**: Medium
**Fix Status**: Pending

---

### [BUG-006] Case-Sensitive Email Duplicate Check
**Status**: Identified
**Location**: `app.py` - `register()` route
**Discovered**: Additional testing - 3rd October 2025
**Reproduction Steps**:
1. Register user with email "test@test.com"
2. Register again with "Test@test.com"
3. System creates duplicate account

**Expected Behaviour**: Email comparison should be case-insensitive
**Actual Behaviour**: Different cases treated as different emails, allowing duplicates
**Priority**: Medium
**Fix Status**: Pending

---

## Performance Inefficiencies

### [INEFFICIENCY-001] Cart Price Calculation Using Nested Loop
**Status**: Identified
**Location**: `models.py` - `Cart.get_total_price()` method
**Discovered**: Performance testing - 3rd October 2025
**Issue**: Uses nested loop instead of simple multiplication
**Performance Impact**: 79x slower for large quantities (5000 items: 0.000237s vs expected 0.000003s)
**Expected Approach**: Direct multiplication `item.book.price * item.quantity`
**Priority**: Medium
**Fix Status**: Pending

---

### [INEFFICIENCY-002] Unused User Attributes
**Status**: Identified
**Location**: `models.py` - `User.__init__()` method
**Discovered**: Unit testing - 3rd October 2025
**Issue**: Creates `temp_data` and `cache` attributes that are never used
**Impact**: Unnecessary memory overhead for every user instance
**Priority**: Low
**Fix Status**: Pending

---

### [INEFFICIENCY-003] Sorting on Every Order Addition
**Status**: Identified
**Location**: `models.py` - `User.add_order()` method
**Discovered**: Performance testing - 3rd October 2025
**Issue**: Sorts entire order list every time an order is added
**Impact**: O(n log n) operation on each addition instead of sorting once when needed
**Priority**: Low
**Fix Status**: Pending

---

### [INEFFICIENCY-004] Linear Search Instead of Helper Function
**Status**: Identified
**Location**: `app.py` - `add_to_cart()` route
**Discovered**: Code analysis - 3rd October 2025
**Issue**: Uses manual loop `for b in BOOKS:` instead of existing `get_book_by_title()` helper
**Impact**: Code duplication and reduced maintainability
**Priority**: Low
**Fix Status**: Pending

---

### [INEFFICIENCY-005] Multiple Imports Inside Method
**Status**: Identified
**Location**: `models.py` - `PaymentGateway.process_payment()` method
**Discovered**: Code review - 3rd October 2025
**Issue**: Imports `random`, `time`, and `datetime` inside method instead of at module level
**Impact**: Import overhead on every payment processing call
**Expected Approach**: Move imports to top of models.py file
**Priority**: Low
**Fix Status**: Pending

---

### [INEFFICIENCY-006] Inefficient Field Validation Loop
**Status**: Identified
**Location**: `app.py` - `process_checkout()` route
**Discovered**: Code review - 3rd October 2025
**Issue**: Uses loop-based validation instead of more efficient validation pattern
**Impact**: Reduced code readability and maintainability
**Expected Approach**: Refactor to cleaner validation pattern (e.g., dictionary comprehension or validation library)
**Priority**: Low
**Fix Status**: Pending

---

## Security Issues

### [SECURITY-001] Debug Mode Enabled in Production
**Status**: Identified
**Location**: `app.py:330` - `app.run(debug=True)`
**Discovered**: Security testing with Bandit - 3rd October 2025
**Severity**: High
**Issue**: Debug mode allows arbitrary code execution through Werkzeug debugger
**Expected Behaviour**: Debug mode should be disabled for production
**Priority**: Critical
**Fix Status**: Fixed - 10th October 2025
**Fix Description**: Changed `app.run(debug=True)` to `app.run(debug=False)` to disable debug mode in production

---

### [SECURITY-002] Hardcoded Secret Key
**Status**: Identified
**Location**: `app.py:6` - `app.secret_key = 'your_secret_key'`
**Discovered**: Security testing with Bandit - 3rd October 2025
**Severity**: Low
**Issue**: Secret key is hardcoded in source code
**Expected Behaviour**: Secret key should be loaded from environment variables
**Priority**: Medium
**Fix Status**: Fixed - 10th October 2025
**Fix Description**: Changed hardcoded secret key to `app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')` to load from environment variables
---

### [SECURITY-003] Weak Random Number Generator for Transactions
**Status**: Identified
**Location**: `models.py:141` - `random.randint(100000, 999999)`
**Discovered**: Security testing with Bandit - 3rd October 2025
**Severity**: Low
**Issue**: Using standard random module for transaction IDs (not cryptographically secure)
**Expected Behaviour**: Should use secrets module for security-sensitive random values
**Priority**: Low
**Fix Status**: Fixed - 10th October 2025
**Fix Description**: Replaced `random.randint()` with `secrets.randbelow()` for cryptographically secure transaction ID generation. Moved imports to module level.

---

### TEST-001: Integration Test False Positive (Test Design Issue)
**Type**: Test Design Issue  
**Priority**: Medium  
**Discovered**: 10th October 2025 (during BUG-001 fix validation)  
**File**: `tests/test_integration_2418326.py`  
**Function**: `test_cart_modification_workflow`  

#### Description
Test was checking if book title appeared anywhere in HTML response, including flash messages. When a book was removed from cart, the flash message "Removed 'I Ching' from cart!" caused test to fail even though removal worked correctly.

#### Issue
```python
# Original assertion - too broad
assert b'I Ching' not in response.data
```

This checks the ENTIRE HTML page, including flash messages, navigation, etc.

#### Expected Behaviour
Test should verify book is removed from cart items, not just absent from entire page.

#### Reproduction Steps
1. Add items to cart
2. Remove an item
3. Check cart view
4. Test fails despite item being correctly removed (appears in flash message)

#### Evidence
- Cart showed "Total Items: 5" (only Moby Dick qty 5)
- Only 1 cart-item div present (Moby Dick)
- "I Ching" appeared in flash message: "Removed 'I Ching' from cart!"

#### Fix Applied
```python
# Fixed assertions - specific checks
assert b'Moby Dick' in response.data
assert b'Total Items: 5' in response.data  # Only Moby Dick with qty 5
# Verify only one cart item div (Moby Dick)
assert response.data.count(b'<div class="cart-item">') == 1
```

**Fix Status**: Fixed - 10th October 2025  
**Fix Description**: Updated test to check cart item count and number of cart-item divs instead of searching entire HTML. This correctly verifies removal without false positives from flash messages.

**Test Result After Fix**: PASS ✓

---

*Additional bugs will be documented as discovered through systematic testing*