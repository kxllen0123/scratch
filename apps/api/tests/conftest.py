"""
Pytest configuration and shared fixtures for API tests
"""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """
    Create a FastAPI test client for making HTTP requests to the API.

    This fixture imports the app lazily to ensure proper test isolation.
    """
    from main import app

    return TestClient(app)
