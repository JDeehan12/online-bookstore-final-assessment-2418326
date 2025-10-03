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

*Additional bugs will be documented as discovered through systematic testing*