# Testing Plan - Student 2418326

## Project Overview
Comprehensive testing, bug identification, performance optimisation, and CI/CD implementation for Online Bookstore Flask application.

## Testing Phases

### Phase 1: Test Infrastructure Setup
- [ ] Unit tests for models.py
- [ ] Unit tests for app.py routes
- [ ] Integration tests for user workflows
- [ ] Performance profiling setup

### Phase 2: Bug Discovery & Documentation
- [x] Systematic functional testing
- [x] Edge case identification
- [x] Security vulnerability assessment
- [x] Bug reproduction documentation
- **Status**: Complete - All bugs documented in BUG_TRACKER_2418326.md

### Phase 2.1: Security Fixes (Added 10th October 2025)
- [x] SECURITY-001: Disable debug mode
- [x] SECURITY-002: Environment variable secret key
- [x] SECURITY-003: Secure random generator for transactions
- **Status**: Complete - 3/3 security issues resolved

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

**Progress**: 126/130 tests passing (4 instructor bugs remaining to identify)

### Phase 3: Bug Fixes & Optimisation
- [ ] Fix critical bugs
- [ ] Implement performance improvements
- [ ] Before/after metrics collection
- [ ] Code quality improvements

### Phase 4: CI/CD Implementation
- [ ] GitHub Actions workflow setup
- [ ] Automated test execution
- [ ] Test coverage reporting
- [ ] Build status badges

### Phase 5: Final Report
- [ ] Testing strategy documentation
- [ ] Bug analysis and fixes
- [ ] Performance improvements
- [ ] CI/CD evaluation

## Timeline
Start Date: 3rd October 2025
Deadline: 20th October 2025 (14:00 UK Time)
Duration: 17 days

## Success Criteria
Target: 90%+ (80-100 band)
- Comprehensive test coverage
- All critical bugs fixed
- Measurable performance improvements
- Functioning CI/CD pipeline
- Professional 1500-word report