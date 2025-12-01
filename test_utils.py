"""Tests for utils module."""
import pytest
from utils import format_output, validate_path, get_file_extension

def test_format_output():
    """Test format_output function."""
    assert format_output("test") == "[OUTPUT] test"
    assert format_output(None) == "[OUTPUT] (empty)"

def test_validate_path():
    """Test validate_path function."""
    assert validate_path("test_utils.py") == True
    assert validate_path("nonexistent.txt") == False

def test_get_file_extension():
    """Test get_file_extension function."""
    assert get_file_extension("test.txt") == ".txt"
    assert get_file_extension("file.py") == ".py"
    assert get_file_extension("noext") == ""
