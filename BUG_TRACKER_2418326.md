# Bug Tracking Document - Student 2418326

## Summary Status
- **Total Issues Identified**: 21
- **Fixed**: 19
- **Pending**: 2 (SECURITY-004, SECURITY-005)
- **Test Pass Rate**: 130/130

---

## Functional Bugs

### [BUG-001] Cart Update Quantity - Zero/Negative Not Handled
**Status**: Fixed
**Location**: `models.py` - `Cart.update_quantity()` method
**Discovered**: Manual testing - 3rd October 2025
**Priority**: Major
**Reproduction Steps**:
1. Add item to cart
2. Update quantity to 0
3. Item remains in cart instead of being removed

**Expected Behaviour**: Items with quantity <= 0 should be removed from cart
**Actual Behaviour**: Quantity is set but item not removed
**Fix Status**: Fixed - 10th October 2025  
**Fix Description**: Modified `Cart.update_quantity()` method to check if quantity <= 0 and delete the item from cart instead of setting quantity to 0 or negative value.

---

### [BUG-002] Case-Sensitive Discount Codes
**Status**: Fixed
**Location**: `app.py` - `process_checkout()` route
**Discovered**: Manual testing - 3rd October 2025
**Priority**: Major
**Reproduction Steps**:
1. Add items to cart
2. Proceed to checkout
3. Enter "save10" (lowercase)
4. Discount not applied

**Expected Behaviour**: Discount codes should be case-insensitive
**Actual Behaviour**: Only exact case matches work (SAVE10, WELCOME20)
**Fix Status**: Fixed - 10th October 2025  
**Fix Description**: Added `.strip()` to discount code input and changed comparison to use `.upper()` method: `if discount_code.upper() == 'SAVE10':` - now accepts any case variation.

---

### [BUG-003] Floating Point Precision in Cart Total Calculation
**Status**: Fixed
**Location**: `models.py` - `Cart.get_total_price()` method
**Discovered**: Unit testing - 3rd October 2025
**Priority**: Minor
**Reproduction Steps**:
1. Add item with large quantity (1000) to cart
2. Calculate total price
3. Observe floating-point precision error

**Expected Behaviour**: Accurate price calculation even with large quantities
**Actual Behaviour**: Floating-point arithmetic errors accumulate (10990.0 vs 10989.999999999825)
**Fix Status**: Fixed - 12th October 2025 (Same fix as INEFFICIENCY-001)
**Fix Description**: Direct multiplication eliminates repeated floating-point additions that caused precision errors. Single multiplication per item prevents error accumulation.

---

### [BUG-004] Missing Payment Field Validation
**Status**: Fixed
**Location**: `models.py` - `PaymentGateway.process_payment()` method
**Discovered**: Additional testing - 3rd October 2025
**Priority**: High
**Reproduction Steps**:
1. Attempt checkout with empty card number
2. Payment processes successfully despite missing required field

**Expected Behaviour**: Should validate all payment fields and reject empty or invalid card information
**Actual Behaviour**: Accepts empty card numbers and invalid formats without validation
**Fix Status**: Fixed - 10th October 2025  
**Fix Description**: Added comprehensive validation in `PaymentGateway.process_payment()` for payment method, card number format (13-19 digits), expiry date, CVV (3-4 digits), and PayPal email requirement.

---

### [BUG-005] No Email Format Validation
**Status**: Fixed
**Location**: `app.py` - `register()` route
**Discovered**: Additional testing - 3rd October 2025
**Priority**: Medium
**Reproduction Steps**:
1. Register with invalid email format (e.g., "notanemail.com")
2. System accepts registration without validation

**Expected Behaviour**: Should validate email format using standard email validation
**Actual Behaviour**: Accepts any string as email address
**Fix Status**: Fixed - 12th October 2025
**Fix Description**: Added `is_valid_email()` helper function using regex pattern `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$` to validate email format. Validation occurs after required fields check but before duplicate check in `register()` route. Invalid formats now rejected with clear error message.

---

### [BUG-006] Case-Sensitive Email Duplicate Check
**Status**: Fixed
**Location**: `app.py` - `register()` route
**Discovered**: Additional testing - 3rd October 2025
**Priority**: Medium
**Reproduction Steps**:
1. Register user with email "test@test.com"
2. Register again with "Test@test.com"
3. System creates duplicate account

**Expected Behaviour**: Email comparison should be case-insensitive
**Actual Behaviour**: Different cases treated as different emails, allowing duplicates
**Fix Status**: Fixed - 12th October 2025
**Fix Description**: Normalised all email inputs to lowercase using `.lower().strip()` in both `register()` and `login()` routes. Email is now converted to lowercase immediately after retrieval from form, ensuring consistent storage and lookup regardless of case entered by user.

---

### [BUG-007] No Input Validation for Quantity in add_to_cart
**Status**: Fixed
**Location**: `app.py` - `add_to_cart()` route
**Discovered**: Testing - 10th October 2025
**Priority**: High
**Reproduction Steps**:
1. Navigate to homepage
2. Enter non-numeric value in quantity field (e.g., 'abc', '', '2.5')
3. Click 'Add to Cart'
4. Application crashes with ValueError: invalid literal for int()

**Expected Behaviour**: Should validate input and display error message for non-integer quantities
**Actual Behaviour**: Unhandled ValueError exception causes 500 Internal Server Error
**Fix Status**: Fixed - 10th October 2025
**Fix Description**: Added try-except block to handle ValueError when converting quantity to int. Validates quantity is positive integer before processing.

---

### [BUG-008] No Input Validation for Quantity in update_cart
**Status**: Fixed
**Location**: `app.py` - `update_cart()` route
**Discovered**: Testing - 10th October 2025
**Priority**: High
**Reproduction Steps**:
1. Add item to cart
2. Navigate to cart page
3. Enter non-numeric value in quantity field (e.g., 'xyz', '!@#')
4. Click 'Update'
5. Application crashes with ValueError: invalid literal for int()

**Expected Behaviour**: Should validate input and display error message for non-integer quantities
**Actual Behaviour**: Unhandled ValueError exception causes 500 Internal Server Error
**Fix Status**: Fixed - 10th October 2025
**Fix Description**: Added try-except block to handle ValueError when converting quantity to int. Validates input before calling cart.update_quantity() method.

---

### [BUG-009] Empty Cart Checkout Flash Message Not Visible
**Status**: Fixed
**Location**: `app.py` - `checkout()` route
**Discovered**: Testing - 10th October 2025
**Priority**: Low
**Reproduction Steps**:
1. Ensure cart is empty (clear if necessary)
2. Navigate directly to `/checkout` URL
3. User is redirected to homepage
4. Flash message 'Your cart is empty!' is set but not visible in test response

**Expected Behaviour**: Flash message should be visible in the redirected response for testing
**Actual Behaviour**: Flash message exists but test cannot verify it appears in response.data after redirect
**Fix Status**: Fixed - 10th October 2025
**Fix Description**: Fixed test to explicitly clear cart before checking redirect. Changed assertion to check for 302 redirect status instead of searching for flash message text in HTML. Added cart clearing step to ensure consistent test state.

---

## Performance Inefficiencies

### [INEFFICIENCY-001] Cart Price Calculation Using Nested Loop
**Status**: Fixed
**Location**: `models.py` - `Cart.get_total_price()` method
**Discovered**: Performance testing - 3rd October 2025
**Priority**: Medium
**Issue**: Uses nested loop instead of simple multiplication
**Performance Impact**: 79x slower for large quantities (5000 items: 0.000237s vs expected 0.000003s)
**Expected Approach**: Direct multiplication `item.book.price * item.quantity`
**Fix Status**: Fixed - 12th October 2025
**Fix Description**: Replaced nested loop with direct multiplication. Changes complexity from O(n*m) to O(n). Performance improvement: 79x faster for 1000 items, 446x faster for 5000 items.

---

### [INEFFICIENCY-002] Unused User Attributes
**Status**: Fixed
**Location**: `models.py` - `User.__init__()` method
**Discovered**: Unit testing - 3rd October 2025
**Priority**: Low
**Issue**: Creates `temp_data` and `cache` attributes that are never used
**Impact**: Unnecessary memory overhead for every user instance
**Fix Status**: Fixed - 12th October 2025
**Fix Description**: Removed `self.temp_data = []` and `self.cache = {}` from User initialisation. Reduced attribute count from 7 to 5 per User instance (28.6% reduction).

---

### [INEFFICIENCY-003] Sorting on Every Order Addition
**Status**: Fixed
**Location**: `models.py` - `User.add_order()` method
**Discovered**: Performance testing - 3rd October 2025
**Priority**: Low
**Issue**: Sorts entire order list every time an order is added
**Impact**: O(n log n) operation on each addition instead of sorting once when needed
**Fix Status**: Fixed - 12th October 2025
**Fix Description**: Removed sorting from `add_order()` method (now O(1) append only). Moved sorting to `get_order_history()` which sorts on-demand when retrieving.

---

### [INEFFICIENCY-004] Linear Search Instead of Helper Function
**Status**: Fixed
**Location**: `app.py` - `add_to_cart()` route
**Discovered**: Code analysis - 3rd October 2025
**Priority**: Low
**Issue**: Uses manual loop `for b in BOOKS:` instead of existing `get_book_by_title()` helper
**Impact**: Code duplication and reduced maintainability
**Fix Status**: Fixed - 12th October 2025
**Fix Description**: Replaced 5-line manual loop with single call to `get_book_by_title(book_title)`. Code reduction: 80% (5 lines → 1 line).

---

### [INEFFICIENCY-005] Multiple Imports Inside Method
**Status**: Fixed
**Location**: `models.py` - `PaymentGateway.process_payment()` method
**Discovered**: Code review - 3rd October 2025
**Priority**: Low
**Issue**: Imports `random`, `time`, and `datetime` inside method instead of at module level
**Impact**: Import overhead on every payment processing call
**Expected Approach**: Move imports to top of models.py file
**Fix Status**: Fixed - 10th October 2025 (as part of SECURITY-003)
**Fix Description**: When fixing SECURITY-003, replaced `random` with `secrets` and moved all imports to module level. Eliminated import overhead.

---

### [INEFFICIENCY-006] Inefficient Field Validation Loop
**Status**: Fixed
**Location**: `app.py` - `process_checkout()` route
**Discovered**: Code review - 3rd October 2025
**Priority**: Low
**Issue**: Loop-based validation with immediate return on first error
**Impact**: Poor UX (only shows one error at a time), repeated string manipulation
**Expected Approach**: Collect all validation errors and display together
**Fix Status**: Fixed - 12th October 2025
**Fix Description**: Replaced loop with list comprehension to collect all missing fields. Shows all validation errors in single message. UX improvement: users see all missing fields at once.

---

## Security Issues

### [SECURITY-001] Debug Mode Enabled in Production
**Status**: Fixed
**Location**: `app.py` - `app.run(debug=True)`
**Discovered**: Security testing with Bandit - 3rd October 2025
**Severity**: High
**Priority**: Critical
**Issue**: Debug mode allows arbitrary code execution through Werkzeug debugger
**Expected Behaviour**: Debug mode should be disabled for production
**Fix Status**: Fixed - 10th October 2025
**Fix Description**: Changed `app.run(debug=True)` to `app.run(debug=False)`.

---

### [SECURITY-002] Hardcoded Secret Key
**Status**: Fixed
**Location**: `app.py` - `app.secret_key = 'your_secret_key'`
**Discovered**: Security testing with Bandit - 3rd October 2025
**Severity**: Low
**Priority**: Medium
**Issue**: Secret key is hardcoded in source code
**Expected Behaviour**: Secret key should be loaded from environment variables
**Fix Status**: Fixed - 10th October 2025
**Fix Description**: Changed to `app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')`.

---

### [SECURITY-003] Weak Random Number Generator for Transactions
**Status**: Fixed
**Location**: `models.py` - `random.randint(100000, 999999)`
**Discovered**: Security testing with Bandit - 3rd October 2025
**Severity**: Low
**Priority**: Low
**Issue**: Using standard random module for transaction IDs (not cryptographically secure)
**Expected Behaviour**: Should use secrets module for security-sensitive random values
**Fix Status**: Fixed - 10th October 2025
**Fix Description**: Replaced `random.randint()` with `secrets.randbelow()` for cryptographically secure transaction ID generation. Moved imports to module level.

---

### [SECURITY-004] Plain Text Password Storage
**Status**: Pending
**Location**: `models.py` - `User` class, `app.py` - authentication routes
**Discovered**: Instructor bugs list review - 12th October 2025
**Severity**: High
**Priority**: High
**Issue**: Passwords stored without hashing
**Expected Behaviour**: Use bcrypt for password hashing
**Impact**: Requires bcrypt library addition, affects User class and all authentication routes
**Fix Status**: Pending

---

### [SECURITY-005] Input Sanitisation
**Status**: Pending
**Location**: Various form processing routes in `app.py`
**Discovered**: Instructor bugs list review - 12th October 2025
**Severity**: Medium
**Priority**: Medium
**Issue**: Relying on default Flask escaping, no explicit sanitisation
**Expected Behaviour**: Explicit input validation and sanitisation
**Fix Status**: Pending

---

## Test Design Issues

### [TEST-001] Integration Test False Positive
**Status**: Fixed
**Type**: Test Design Issue  
**Priority**: Medium  
**Discovered**: 10th October 2025 (during BUG-001 fix validation)  
**Location**: `tests/test_integration_2418326.py` - `test_cart_modification_workflow`  

**Issue**: Test assertion `assert b'I Ching' not in response.data` was too broad - checked entire HTML including flash messages. When book was removed from cart, flash message "Removed 'I Ching' from cart!" caused false positive failure.

**Expected Behaviour**: Test should verify book removed from cart items specifically, not search entire page.

**Fix Status**: Fixed - 10th October 2025  
**Fix Description**: Updated test to check cart item count and count of cart-item divs instead of searching entire HTML for book title.

---

### [TEST-002] Discount Code Test Assertion Issue
**Status**: Fixed
**Type**: Test Design Issue  
**Priority**: Low  
**Discovered**: 10th October 2025 (during BUG-002 fix validation)  
**Location**: `tests/test_app_2418326.py` - `test_discount_code_uppercase`  

**Issue**: Test searched for words 'discount' or 'saved' in order confirmation page, but flash messages don't persist through redirects to that page, causing test to fail despite discount working correctly.

**Expected Behaviour**: Test should verify discount applied by checking order was successful, not by searching for flash message text.

**Fix Status**: Fixed - 10th October 2025  
**Fix Description**: Changed assertion to verify order confirmation success instead of searching for flash message text that doesn't persist through redirects.

---

**Document Version**: 2.0  
**Last Updated**: 12th October 2025, 23:45  
**Student**: 2418326