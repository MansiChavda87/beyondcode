# TDD Testing Guide for BeyondCode AI CMS

## Overview

This guide provides comprehensive instructions for implementing and using Test-Driven Development (TDD) with the BeyondCode AI CMS project. The testing suite follows strict TDD principles to ensure code quality, prevent bugs, and enable safe refactoring.

## Table of Contents

1. [TDD Principles](#tdd-principles)
2. [Test Suite Structure](#test-suite-structure)
3. [Running Tests](#running-tests)
4. [Writing Tests](#writing-tests)
5. [Test Categories](#test-categories)
6. [Performance Testing](#performance-testing)
7. [Security Testing](#security-testing)
8. [Integration Testing](#integration-testing)
9. [End-to-End Testing](#end-to-end-testing)
10. [Best Practices](#best-practices)
11. [Troubleshooting](#troubleshooting)

## TDD Principles

### The RED-GREEN-REFACTOR Cycle

1. **RED**: Write a failing test first
   - Write the test before implementing the feature
   - Verify the test fails (proves it's testing the right thing)
   - Never write production code without a failing test

2. **GREEN**: Write minimal code to pass the test
   - Implement only what's needed to make the test pass
   - Don't add extra features or optimizations
   - Keep the implementation simple

3. **REFACTOR**: Improve code quality
   - Clean up the code while keeping tests passing
   - Remove duplication, improve names, extract helpers
   - Never add new behavior during refactoring

### Iron Law of TDD

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

**Critical Rules:**
- If you wrote code before the test, DELETE IT and start over
- Don't keep "reference" code
- Don't "adapt" existing code while writing tests
- Always watch the test fail first

## Test Suite Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest configuration and fixtures
├── test_models.py           # Model tests (CRUD, validation, relationships)
├── test_views.py            # View tests (HTTP responses, templates, permissions)
├── test_integration.py      # Integration tests (end-to-end workflows)
├── test_performance.py      # Performance tests (response times, scalability)
├── test_security.py         # Security tests (auth, authorization, vulnerabilities)
├── test_urls.py             # URL pattern tests (routing, parameter validation)
├── test_e2e.py              # End-to-end tests (complete user scenarios)
├── test_fixtures.py         # Test data fixtures and factories
├── test_runner.py           # Custom test runner and reporting
└── test_results/            # Generated test reports and results
```

## Running Tests

### Using the Custom Test Runner

```bash
# Run all tests
python tests/test_runner.py

# Run specific test suite
python tests/test_runner.py --suite models
python tests/test_runner.py --suite views
python tests/test_runner.py --suite integration

# Run specific test categories
python tests/test_runner.py --performance
python tests/test_runner.py --security
python tests/test_runner.py --integration

# Run TDD cycle
python tests/test_runner.py --tdd-cycle
```

### Using Django's Test Runner

```bash
# Run all tests
python manage.py test tests

# Run specific test module
python manage.py test tests.test_models
python manage.py test tests.test_views

# Run specific test class
python manage.py test tests.test_models.TestMediaAssetModel

# Run specific test method
python manage.py test tests.test_models.TestMediaAssetModel.test_media_asset_creation

# Run with coverage
python manage.py test tests --coverage

# Run with verbose output
python manage.py test tests --verbosity=2
```

### Using Pytest

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_models.py

# Run tests with specific markers
pytest tests/ -m "performance"
pytest tests/ -m "security"
pytest tests/ -m "integration"

# Run slow tests only
pytest tests/ -m "slow"

# Run with coverage
pytest tests/ --cov=marketing --cov-report=html

# Run with detailed output
pytest tests/ -v
```

## Writing Tests

### Test Naming Conventions

```python
class TestPageModel(TestCase):
    """Test class for Page model"""
    
    def test_page_creation(self):
        """Test basic page creation"""
        # Test implementation
    
    def test_page_slug_uniqueness(self):
        """Test slug uniqueness constraint"""
        # Test implementation
    
    def test_page_is_published_property(self):
        """Test is_published property"""
        # Test implementation
```

### Test Structure

```python
def test_example(self):
    """Test description explaining what this test verifies"""
    # 1. Setup - Create test data and arrange conditions
    test_data = create_test_data()
    
    # 2. Action - Perform the action being tested
    result = perform_action(test_data)
    
    # 3. Assertion - Verify the expected outcome
    self.assertEqual(result.status, 'expected_status')
    self.assertTrue(result.is_valid)
```

### Using Fixtures

```python
def test_with_fixture(self, test_page):
    """Test using pytest fixture"""
    # test_page fixture provides a pre-created page
    self.assertEqual(test_page.status, 'published')

def test_with_factory(self, data_factory):
    """Test using data factory"""
    page = data_factory.create_page('Test Page', 'test-page')
    self.assertEqual(page.title, 'Test Page')
```

## Test Categories

### 1. Model Tests (`test_models.py`)

**Purpose**: Test model functionality, validation, and relationships

**Examples**:
- Model creation and validation
- Field constraints and uniqueness
- Model methods and properties
- Database relationships
- Custom model managers

```python
def test_page_creation(self):
    """Test basic page creation"""
    page = Page.objects.create(
        title="Test Page",
        slug="test-page",
        status="published"
    )
    
    self.assertEqual(page.title, "Test Page")
    self.assertEqual(page.slug, "test-page")
    self.assertEqual(page.status, "published")
    self.assertIsNotNone(page.created_at)
    self.assertIsNotNone(page.updated_at)
```

### 2. View Tests (`test_views.py`)

**Purpose**: Test HTTP endpoints, templates, and user interactions

**Examples**:
- HTTP response codes
- Template rendering
- Form submissions
- Authentication and permissions
- URL routing

```python
def test_home_view(self):
    """Test homepage view"""
    response = self.client.get(reverse('marketing:home'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Home")
    self.assertTemplateUsed(response, 'marketing/pages/home.html')
```

### 3. Integration Tests (`test_integration.py`)

**Purpose**: Test complete workflows and component interactions

**Examples**:
- End-to-end user workflows
- Multi-step processes
- Cross-component interactions
- Data consistency across operations

```python
def test_complete_page_workflow(self):
    """Test complete page creation and publishing workflow"""
    # Login as user
    self.client.login(username='testuser', password='testpass123')
    
    # Create page
    response = self.client.post(reverse('marketing:page_create'), {
        'title': 'Integration Test Page',
        'slug': 'integration-test-page',
        'status': 'draft',
    })
    self.assertEqual(response.status_code, 302)
    
    # Verify page was created
    page = Page.objects.get(slug='integration-test-page')
    self.assertEqual(page.status, 'draft')
    
    # Edit and publish page
    response = self.client.post(reverse('marketing:page_edit', kwargs={'pk': page.pk}), {
        'title': 'Updated Page',
        'status': 'published',
    })
    self.assertEqual(response.status_code, 302)
    
    # Verify page was updated
    page.refresh_from_db()
    self.assertEqual(page.status, 'published')
```

### 4. Performance Tests (`test_performance.py`)

**Purpose**: Test application performance and scalability

**Examples**:
- Response time thresholds
- Database query optimization
- Memory usage
- Concurrent user simulation

```python
def test_homepage_performance(self):
    """Test homepage response time"""
    response, response_time = self.measure_response_time(reverse('marketing:home'))
    
    self.assertEqual(response.status_code, 200)
    self.assertLess(response_time, 1.0, f"Homepage took {response_time:.2f}s, should be under 1.0s")
```

### 5. Security Tests (`test_security.py`)

**Purpose**: Test application security and vulnerability protection

**Examples**:
- Authentication and authorization
- CSRF protection
- XSS prevention
- SQL injection protection
- File upload security
- Session security

```python
def test_csrf_protection(self):
    """Test CSRF protection on forms"""
    self.client.login(username='testuser', password='testpass123')
    
    # Try to submit form without CSRF token
    response = self.client.post(reverse('marketing:page_create'), {
        'title': 'Test Page',
        'slug': 'test-page',
        'status': 'published'
    }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    # Should be rejected due to missing CSRF token
    self.assertNotEqual(response.status_code, 302)
```

### 6. URL Tests (`test_urls.py`)

**Purpose**: Test URL patterns and routing functionality

**Examples**:
- URL reversal
- Route resolution
- Parameter validation
- URL security

```python
def test_home_url(self):
    """Test home URL pattern"""
    url = reverse('marketing:home')
    self.assertEqual(url, '/')
    
    # Test that URL resolves to correct view
    resolved = resolve('/')
    self.assertEqual(resolved.view_name, 'marketing:home')
```

### 7. End-to-End Tests (`test_e2e.py`)

**Purpose**: Test complete user scenarios and workflows

**Examples**:
- User registration and login
- Content creation and management
- Navigation and footer management
- SEO optimization workflows

```python
def test_user_registration_and_login_workflow(self):
    """Test complete user registration and login workflow"""
    # 1. User visits homepage
    response = self.client.get(reverse('marketing:home'))
    self.assertEqual(response.status_code, 200)
    
    # 2. User clicks register link
    response = self.client.get(reverse('marketing:register'))
    self.assertEqual(response.status_code, 200)
    
    # 3. User fills registration form
    response = self.client.post(reverse('marketing:register'), {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password1': 'testpass123',
        'password2': 'testpass123'
    })
    self.assertEqual(response.status_code, 302)  # Redirect after successful registration
    
    # 4. User is created
    new_user = User.objects.get(username='newuser')
    self.assertEqual(new_user.email, 'newuser@example.com')
```

## Performance Testing

### Response Time Thresholds

- Homepage: < 1.0s
- Blog list: < 1.0s
- Page detail: < 1.0s
- CMS dashboard: < 2.0s
- API responses: < 0.5s

### Performance Test Categories

1. **Individual Page Performance**
   - Measure response times for key pages
   - Verify performance under load
   - Test with realistic data volumes

2. **Database Query Optimization**
   - Monitor query counts
   - Identify N+1 query problems
   - Test query performance with large datasets

3. **Concurrent User Simulation**
   - Simulate multiple concurrent users
   - Test session handling under load
   - Verify resource usage

4. **Memory Usage**
   - Monitor memory consumption
   - Test with large datasets
   - Verify proper cleanup

## Security Testing

### Security Test Categories

1. **Authentication & Authorization**
   - Login/logout functionality
   - Permission checks
   - Session security

2. **Input Validation**
   - XSS prevention
   - SQL injection protection
   - File upload security

3. **CSRF Protection**
   - Form submission security
   - Cross-site request forgery prevention

4. **Security Headers**
   - Content Security Policy
   - X-Frame-Options
   - X-XSS-Protection

5. **Error Handling**
   - Information disclosure prevention
   - Secure error messages
   - Debug mode security

## Integration Testing

### Integration Test Scenarios

1. **Content Management Workflow**
   - Page creation → editing → publishing → deletion
   - Blog post creation → categorization → tagging → publishing
   - Media asset upload → usage → management

2. **User Management**
   - User registration → authentication → authorization → account management
   - Admin user creation → permission assignment → content access

3. **SEO and Analytics**
   - Content creation → SEO optimization → sitemap generation → robots.txt
   - Analytics integration → tracking → reporting

4. **Navigation and Footer**
   - Navigation editing → menu item management → display
   - Footer editing → CTA management → legal text

## End-to-End Testing

### E2E Test Scenarios

1. **Visitor Journey**
   - Homepage visit → content exploration → contact form submission
   - Blog browsing → category filtering → post reading → sharing

2. **Content Editor Workflow**
   - Login → dashboard → content creation → editing → publishing
   - Media management → navigation editing → footer management

3. **Admin Workflow**
   - System overview → user management → content review → settings

4. **Performance Under Load**
   - Multiple concurrent users → content creation → navigation
   - Large content volumes → search functionality → pagination

## Best Practices

### TDD Best Practices

1. **Write Failing Tests First**
   - Always write the test before the implementation
   - Verify the test fails for the expected reason
   - Never skip the RED phase

2. **Keep Tests Focused**
   - One test per behavior
   - Clear, descriptive test names
   - Minimal test setup

3. **Use Descriptive Assertions**
   - Clear error messages
   - Specific assertions
   - Avoid generic assertions

4. **Test Edge Cases**
   - Invalid inputs
   - Boundary conditions
   - Error scenarios

5. **Maintain Test Independence**
   - No test dependencies
   - Clean setup and teardown
   - Isolated test data

### Code Organization

1. **Test File Structure**
   - Mirror the application structure
   - Group related tests together
   - Use clear naming conventions

2. **Test Data Management**
   - Use fixtures for common data
   - Create factories for complex objects
   - Clean up test data automatically

3. **Test Configuration**
   - Separate test settings
   - Use in-memory databases for speed
   - Configure appropriate timeouts

### Performance Considerations

1. **Test Speed**
   - Use lightweight test databases
   - Minimize external dependencies
   - Parallel test execution

2. **Resource Management**
   - Proper cleanup
   - Memory management
   - Database transaction handling

3. **Test Coverage**
   - Aim for 80%+ coverage
   - Focus on critical paths
   - Include integration coverage

## Troubleshooting

### Common Issues

1. **Tests Failing Randomly**
   - Check for test dependencies
   - Verify database state
   - Review timing issues

2. **Slow Test Execution**
   - Use in-memory databases
   - Minimize external calls
   - Parallel execution

3. **Database Issues**
   - Check migrations
   - Verify test database setup
   - Review transaction handling

4. **Import Errors**
   - Check Django settings
   - Verify module paths
   - Review dependencies

### Debugging Tips

1. **Use Verbose Output**
   ```bash
   python manage.py test tests --verbosity=2
   ```

2. **Run Single Tests**
   ```bash
   python manage.py test tests.test_models.TestPageModel.test_page_creation
   ```

3. **Check Test Database**
   ```bash
   python manage.py test tests --keepdb
   ```

4. **Use Debug Mode**
   ```python
   import pdb; pdb.set_trace()
   ```

### Performance Debugging

1. **Monitor Response Times**
   ```python
   import time
   start_time = time.time()
   # Test code
   duration = time.time() - start_time
   ```

2. **Database Query Analysis**
   ```python
   from django.test.utils import override_settings
   with self.assertNumQueries(3):
       # Test code
   ```

3. **Memory Usage Monitoring**
   ```python
   import psutil
   process = psutil.Process()
   memory_usage = process.memory_info().rss / 1024 / 1024
   ```

## Continuous Integration

### CI/CD Integration

1. **Automated Test Execution**
   - Run tests on every commit
   - Fail builds on test failures
   - Generate test reports

2. **Code Coverage Reporting**
   - Track coverage metrics
   - Set coverage thresholds
   - Generate coverage reports

3. **Performance Monitoring**
   - Track test execution times
   - Monitor performance regressions
   - Alert on performance issues

### Example CI Configuration

```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.10
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-django coverage
    
    - name: Run tests
      run: |
        python tests/test_runner.py --all
    
    - name: Generate coverage report
      run: |
        coverage run --source=marketing manage.py test
        coverage html
```

## Conclusion

This TDD testing suite provides comprehensive coverage for the BeyondCode AI CMS project. By following these guidelines and using the provided tools, you can ensure code quality, prevent regressions, and maintain a robust codebase.

Remember the core TDD principle: **NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST**. This discipline will lead to better code, fewer bugs, and more confidence in your implementations.