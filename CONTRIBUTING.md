# Contributing to E-Commerce API

Thank you for considering contributing to the E-Commerce API project! This document outlines the development workflow and guidelines.

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- pip

### Initial Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/anshajk/mcp_boilerplate.git
   cd mcp_boilerplate/api_mcp
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Install pre-commit hooks (optional but recommended):**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

- Write clean, readable code
- Follow PEP 8 style guidelines
- Add docstrings to functions and classes
- Keep functions small and focused

### 3. Write Tests

All new features must include tests:

```python
# In test_app.py
def test_your_new_feature():
    """Test description"""
    response = client.get("/your-endpoint")
    assert response.status_code == 200
    # More assertions...
```

### 4. Run Tests Locally

Before committing, ensure all tests pass:

```bash
# Run all tests
pytest test_app.py -v

# Run with coverage
pytest test_app.py --cov=app --cov-report=term

# Run specific test
pytest test_app.py::test_your_new_feature -v
```

### 5. Format Your Code

```bash
# Auto-format with Black (line length: 127)
black  .

# Sort imports
isort  .

# Check formatting (without modifying)
black --check --diff  .
isort --check-only --diff  .
```

### 6. Run Security Checks

```bash
# Run security check
bandit -r . -ll
```

### 7. Commit Your Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "feat: add new product search endpoint

- Add search by product name
- Include tests for search functionality
- Update documentation
"
```

**Commit Message Format:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Adding or updating tests
- `refactor:` - Code refactoring
- `style:` - Code style changes (formatting)
- `perf:` - Performance improvements

### 8. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Code Quality Standards

### Testing Requirements

- **Coverage:** Aim for >80% code coverage
- **Test types:** Include unit tests and integration tests
- **Edge cases:** Test error conditions and boundary values

### Code Style

- **Formatter:** Black (line length: 127)
- **Import sorting:** isort (profile: black, line length: 127)
- **Security:** Bandit for security scanning
- **Type hints:** Encouraged for function signatures

### Documentation

- Add docstrings to all public functions
- Update README.md if adding new features
- Include examples in docstrings
- Keep API documentation up to date

## Pull Request Guidelines

### Before Submitting

✅ All tests pass locally  
✅ Code is formatted with Black (line length: 127)  
✅ Imports are sorted with isort  
✅ Security scan passes (Bandit)  
✅ Coverage is maintained or improved  
✅ Documentation is updated  
✅ Commit messages are clear  

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Added unit tests
- [ ] Added integration tests
- [ ] All tests pass locally

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings generated
```

### Review Process

1. **Automated Checks:** GitHub Actions will run all tests
2. **Code Review:** Maintainer will review your code
3. **Feedback:** Address any requested changes
4. **Merge:** Once approved, your PR will be merged

## Running GitHub Actions Locally

You can test the CI pipeline locally using [act](https://github.com/nektos/act):

```bash
# Install act
brew install act  # macOS
# or
choco install act-cli  # Windows

# Run the workflow
act -W .github/workflows/api-tests.yml
```

## Common Issues and Solutions

### Tests Fail Locally But Pass in CI
- Ensure you're using the same Python version
- Check for platform-specific issues
- Verify all dependencies are installed

### Import Errors
- Make sure you're in the correct directory
- Activate virtual environment
- Reinstall dependencies

### Linting Failures
- Run `black .` to auto-fix formatting
- Run `isort .` to fix import order
- Check flake8 output for specific errors

## Getting Help

- **Issues:** Check existing [GitHub Issues](https://github.com/anshajk/mcp_boilerplate/issues)
- **Discussions:** Start a [GitHub Discussion](https://github.com/anshajk/mcp_boilerplate/discussions)
- **Documentation:** Read [CICD.md](../.github/CICD.md) for CI/CD details

## Project Structure

```
api_mcp/
├── app.py                 # Main FastAPI application
├── test_app.py           # Test suite
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
├── pytest.ini           # Pytest configuration
├── run_tests.py         # Test runner script
├── README.md            # User documentation
└── TEST_COVERAGE.md     # Test coverage details
```

## Code Review Checklist

When reviewing PRs, maintainers check for:

- [ ] Tests cover new functionality
- [ ] Code is well-documented
- [ ] No security vulnerabilities introduced
- [ ] Performance impact is acceptable
- [ ] Breaking changes are documented
- [ ] API changes are backwards compatible (or properly versioned)

## Release Process

1. All tests pass on `main` branch
2. Version is updated in relevant files
3. CHANGELOG.md is updated
4. Tag is created: `git tag v1.x.x`
5. GitHub Release is created

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in the README (for significant contributions)

Thank you for contributing! 🚀
