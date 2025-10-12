# Testing Plan - Student 2418326

## Project Overview
Comprehensive testing, bug identification, performance optimisation, and CI/CD implementation for Online Bookstore Flask application.

## Testing Phases

### Phase 1: Test Infrastructure Setup
- [x] Unit tests for models.py
- [x] Unit tests for app.py routes
- [x] Integration tests for user workflows
- [x] Performance profiling setup
- **Status**: Complete - 130 tests across 5 test files

### Phase 2: Bug Discovery & Documentation
- [x] Systematic functional testing
- [x] Edge case identification
- [x] Security vulnerability assessment
- [x] Bug reproduction documentation
- **Status**: Complete - All bugs documented in BUG_TRACKER_2418326.md

### Phase 2.1: Security Fixes (10th October 2025)
- [x] SECURITY-001: Disable debug mode
- [x] SECURITY-002: Environment variable secret key
- [x] SECURITY-003: Secure random generator for transactions
- **Status**: Complete - 3/3 initial security issues resolved

### Phase 2.2: Test Quality Improvement (10th October 2025)
**Status**: Complete

**Test Issue Discovered**:
- **TEST-001**: Integration test `test_cart_modification_workflow` had overly broad assertion
- Test checked entire HTML for book title, including flash messages
- Caused false positive failure when book was correctly removed

**Solution**:
- Updated test to check specific cart metrics (item count, cart-item div count)
- Demonstrates importance of precise test assertions
- All integration tests now passing with more robust checks

### Phase 2.3: Major Bug Fixes (10th October 2025)
**Status**: Complete

**BUG-001**: Cart zero/negative quantity removal
- Fixed `Cart.update_quantity()` to remove items when quantity <= 0
- 3 related tests now passing

**BUG-002**: Case-sensitive discount codes  
- Made discount code comparison case-insensitive using `.upper()`
- Added `.strip()` for whitespace handling
- 1 test now passing (with improved assertion)

**TEST-002**: Discount code test assertion improved
- Changed from searching for flash message text to verifying order confirmation
- More reliable test that checks actual functionality

**Progress**: 130/130 tests passing

### Phase 2.4: Email Validation & Performance Fixes (12th October 2025)
**Status**: Complete

**BUG-005**: No email format validation
- Added `is_valid_email()` helper function with regex validation

**BUG-006**: Case-sensitive email duplicate check
- Normalised emails to lowercase in register() and login()

**INEFFICIENCY-001**: Nested loop in cart price calculation
- Replaced with direct multiplication
- Performance improvement: 79x-446x faster

**INEFFICIENCY-002**: Unused user attributes
- Removed temp_data and cache
- Memory reduction: 28.6%

**INEFFICIENCY-003**: Sorting on every order addition
- Moved sorting to retrieval only

**INEFFICIENCY-004**: Manual loop vs helper function
- Replaced with get_book_by_title() call
- Code reduction: 80%

**INEFFICIENCY-006**: Loop-based field validation
- List comprehension shows all errors at once
- Better UX

**Progress**: 130/130 tests passing

### Phase 2.5: Additional Security Fixes (12th October 2025)
**Status**: In Progress

**SECURITY-004**: Plain text password storage
- Add bcrypt to requirements.txt
- Implement password hashing in User class
- Update registration, login, profile update routes
- Fix affected authentication tests

**SECURITY-005**: Input sanitisation
- Review and enhance input validation
- Add explicit sanitisation where needed

**Progress**: 19/21 issues fixed (90% → 100% when complete)

### Phase 3: Bug Fixes & Optimisation
- [x] Fix critical bugs
- [x] Implement performance improvements
- [x] Before/after metrics collection
- [x] Code quality improvements
- **Status**: Complete - All functional bugs and inefficiencies fixed

### Phase 4: CI/CD Implementation
- [x] GitHub Actions workflow setup
- [x] Automated test execution
- [x] Test coverage reporting
- [x] Build status badges
- **Status**: Complete - Pipeline running successfully

### Phase 5: Final Report
- [ ] Testing strategy documentation
- [ ] Bug analysis and fixes
- [ ] Performance improvements
- [ ] CI/CD evaluation