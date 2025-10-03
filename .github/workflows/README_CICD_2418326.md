# CI/CD Pipeline Documentation - Student 2418326

## Overview
Automated testing pipeline using GitHub Actions for the Online Bookstore application.

## Pipeline Stages

### 1. Unit Tests (models.py)
- Tests all model classes: Book, Cart, CartItem, User, Order
- Validates business logic and data handling
- **Current Status**: 64 tests (61 passing, 3 expected failures)

### 2. Route Tests (app.py)
- Tests Flask application routes
- Validates HTTP responses and form handling
- **Current Status**: 45 tests (41 passing, 4 expected failures)

### 3. Integration Tests
- Tests complete user workflows
- Validates end-to-end functionality
- **Current Status**: 14 tests (13 passing, 1 expected failure)

### 4. Performance Tests
- Profiles code execution times
- Establishes performance baselines
- **Current Status**: 6 tests (all passing)

### 5. Security Scan
- Runs Bandit static analysis
- Identifies security vulnerabilities
- **Current Status**: 1 test (passing, 3 issues identified)

### 6. Coverage Report
- Generates code coverage metrics
- Produces HTML coverage report
- Available as downloadable artefact

## Expected Test Failures

The following test failures are **intentional bugs** documented in BUG_TRACKER_2418326.md:

- Cart quantity update (zero/negative not removed)
- Input validation crashes on invalid input
- Floating point precision errors

These will be fixed in the bug fix phase.

## Viewing Results

1. Go to the repository's Actions tab
2. Click on the latest workflow run
3. View test results for each stage
4. Download coverage report artefact

## Running Locally
```bash
# Run all tests
pytest -v

# Run specific test file
pytest tests/test_models_2418326.py -v

# Run with coverage
pytest --cov=. --cov-report=html