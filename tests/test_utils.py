"""
Tests for the rewe.utils module
"""

import pytest
from rewe.utils import get_project_root, get_data_path


def test_get_project_root():
    """Test getting project root"""
    root = get_project_root()
    assert root.exists()
    assert (root / "src" / "rewe").exists()


def test_get_data_path():
    """Test getting data paths"""
    for data_type in ["raw", "processed", "interim", "external"]:
        path = get_data_path(data_type)
        assert path.exists()
        assert data_type in str(path)


def test_get_data_path_invalid():
    """Test getting data path with invalid type"""
    with pytest.raises(ValueError):
        get_data_path("invalid")
