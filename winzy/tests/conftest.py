"""Pytest configuration for winzy tests."""

import sys
import pytest


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up the test environment."""
    # Mark that we're running tests to prevent plugin loading
    sys._called_from_test = True
    yield
    # Clean up after tests
    if hasattr(sys, '_called_from_test'):
        delattr(sys, '_called_from_test')