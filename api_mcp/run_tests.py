#!/usr/bin/env python
"""
Test runner script for the E-Commerce API
"""
import sys
import pytest

if __name__ == "__main__":
    # Run pytest with verbose output
    exit_code = pytest.main(["test_app.py", "-v", "--tb=short", "--color=yes"])

    sys.exit(exit_code)
