import os
import sys
import copy
import pytest

# Ensure `src` is importable as top-level for tests
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from fastapi.testclient import TestClient
import app as app_module
from app import app


@pytest.fixture
def client():
    """Test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def activities_snapshot():
    """Snapshot the module-level `activities` dict and restore after each test."""
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(original)
