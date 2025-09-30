# GitHub Actions CI/CD Pipeline

## Overview

This project uses GitHub Actions to automatically test, lint, and validate code quality on every push and pull request.

## Workflow File

Location: `.github/workflows/api-tests.yml`

## Workflow Jobs

### 1. Test Job (`test`)

**Purpose:** Run the complete test suite across multiple Python versions

**Strategy:**
- Matrix testing on Python 3.10, 3.11, and 3.12
- Ensures compatibility across different Python versions

**Steps:**
1. **Checkout code** - Pulls the latest code from the repository
2. **Set up Python** - Configures the specified Python version with pip caching
3. **Install dependencies** - Installs all required packages from `requirements.txt`
4. **Run linting** - Uses flake8 to check for syntax errors and code quality issues
5. **Run tests** - Executes pytest with coverage reporting
6. **Upload coverage** - Sends coverage data to Codecov (optional)
7. **Test summary** - Adds test results to GitHub Actions summary

**Coverage Report:**
- Generates XML and terminal coverage reports
- Can be integrated with Codecov for coverage tracking
- Minimum coverage thresholds can be configured

### 2. Lint and Format Job (`lint-and-format`)

**Purpose:** Ensure code follows consistent formatting and style guidelines

**Tools Used:**
- **Black** - Code formatter (checks for formatting compliance)
- **isort** - Import statement organizer
- **flake8** - Style guide enforcement

**Steps:**
1. Checkout code
2. Set up Python 3.12
3. Install linting tools
4. Check Black formatting (doesn't modify, just reports)
5. Check isort import sorting
6. Run flake8 for code quality

### 3. Security Job (`security`)

**Purpose:** Identify potential security vulnerabilities

**Tools Used:**
- **Bandit** - Security issue scanner for Python code
- **Safety** - Checks dependencies for known vulnerabilities

**Steps:**
1. Checkout code
2. Set up Python 3.12
3. Install security tools
4. Run Bandit security scan
5. Check dependencies with Safety

## Triggers

The workflow runs on:

1. **Push to main/develop branches** (only when `api_mcp/` files change)
2. **Pull requests to main/develop** (only when `api_mcp/` files change)
3. **Manual trigger** via workflow_dispatch

## Badges

Add these badges to your README:

```markdown
[![E-Commerce API Tests](https://github.com/anshajk/mcp_boilerplate/actions/workflows/api-tests.yml/badge.svg)](https://github.com/anshajk/mcp_boilerplate/actions/workflows/api-tests.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
```

## Setting Up Codecov (Optional)

To enable coverage reporting to Codecov:

1. Sign up at [codecov.io](https://codecov.io)
2. Connect your GitHub repository
3. Get your `CODECOV_TOKEN`
4. Add it to GitHub Secrets:
   - Go to repository Settings → Secrets → Actions
   - Add new secret: `CODECOV_TOKEN`
5. The workflow will automatically upload coverage reports

## Local Development

Run the same checks locally before pushing:

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Format code
black api_mcp/
isort api_mcp/

# Check formatting (without modifying)
black --check api_mcp/
isort --check-only api_mcp/

# Lint
cd api_mcp
flake8 . --max-line-length=127

# Security scan
bandit -r api_mcp/

# Run tests with coverage
cd api_mcp
pytest test_app.py --cov=app --cov-report=html --cov-report=term
```

## Viewing Results

### GitHub Actions UI

1. Go to your repository on GitHub
2. Click the "Actions" tab
3. Select a workflow run to see detailed results
4. Each job shows:
   - Step-by-step execution logs
   - Success/failure status
   - Test output and coverage

### Pull Request Checks

When you open a PR:
- All checks must pass before merging
- Failed checks block the merge
- You can see which specific tests failed
- Test summary appears in PR comments

## Customization

### Modify Python Versions

Edit the matrix in `.github/workflows/api-tests.yml`:

```yaml
strategy:
  matrix:
    python-version: ['3.10', '3.11', '3.12', '3.13']  # Add more versions
```

### Add More Checks

Add additional steps to any job:

```yaml
- name: Run custom check
  run: |
    cd api_mcp
    python custom_script.py
```

### Adjust Triggers

Modify when the workflow runs:

```yaml
on:
  push:
    branches: [ main, develop, feature/* ]  # Add more branches
    paths:
      - 'api_mcp/**'
      - 'tests/**'  # Add more paths
```

## Best Practices

1. **Keep workflows fast** - Currently ~1-2 minutes per run
2. **Use caching** - We cache pip packages to speed up installs
3. **Fail fast** - Syntax errors caught in linting before tests run
4. **Matrix testing** - Ensures compatibility across Python versions
5. **Security first** - Automatic vulnerability scanning on every push

## Troubleshooting

### Workflow Fails on Push

1. Check the Actions tab for detailed error logs
2. Run the same commands locally to reproduce
3. Fix the issue and push again

### Coverage Not Uploading

- Ensure `CODECOV_TOKEN` is set in repository secrets
- Check that `pytest-cov` is installed
- Verify the coverage.xml file is generated

### Security Scan False Positives

- Review Bandit output carefully
- Add exclusions in `.bandit` config file if needed
- Document why certain warnings are acceptable

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [Bandit Security Tool](https://bandit.readthedocs.io/)
- [Codecov](https://docs.codecov.com/)
