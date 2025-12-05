"""Tests for file_ops module."""
import pytest
from file_ops import read_file, write_file, convert_format

def test_read_file_not_found():
    """Test read_file with non-existent file."""
    with pytest.raises(FileNotFoundError):
        read_file("nonexistent.txt")

def test_convert_format_json():
    """Test convert_format with JSON."""
    data = {"key": "value"}
    result = convert_format(data, "json")
    assert '"key"' in result
    assert '"value"' in result

def test_convert_format_txt():
    """Test convert_format with text."""
    data = "test data"
    result = convert_format(data, "txt")
    assert result == "test data"
