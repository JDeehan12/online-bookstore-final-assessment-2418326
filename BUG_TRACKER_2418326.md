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

## Security Issues

### [SECURITY-001] Debug Mode Enabled in Production
**Status**: Identified
**Location**: `app.py:330` - `app.run(debug=True)`
**Discovered**: Security testing with Bandit - 3rd October 2025
**Severity**: High
**Issue**: Debug mode allows arbitrary code execution through Werkzeug debugger
**Expected Behaviour**: Debug mode should be disabled for production
**Priority**: Critical
**Fix Status**: Pending

---

### [SECURITY-002] Hardcoded Secret Key
**Status**: Identified
**Location**: `app.py:6` - `app.secret_key = 'your_secret_key'`
**Discovered**: Security testing with Bandit - 3rd October 2025
**Severity**: Low
**Issue**: Secret key is hardcoded in source code
**Expected Behaviour**: Secret key should be loaded from environment variables
**Priority**: Medium
**Fix Status**: Pending

---

### [SECURITY-003] Weak Random Number Generator for Transactions
**Status**: Identified
**Location**: `models.py:141` - `random.randint(100000, 999999)`
**Discovered**: Security testing with Bandit - 3rd October 2025
**Severity**: Low
**Issue**: Using standard random module for transaction IDs (not cryptographically secure)
**Expected Behaviour**: Should use secrets module for security-sensitive random values
**Priority**: Low
**Fix Status**: Pending

---

*Additional bugs will be documented as discovered through systematic testing*