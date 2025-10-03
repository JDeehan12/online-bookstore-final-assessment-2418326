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

*Additional bugs will be documented as discovered through systematic testing*