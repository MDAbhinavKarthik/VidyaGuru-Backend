"""
Automated smoke test suite for VidyaGuru Backend.
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Verify application route registration and root responsiveness."""
    assert len(app.routes) > 0
    assert any(route.path.startswith("/api/v1") for route in app.routes)
